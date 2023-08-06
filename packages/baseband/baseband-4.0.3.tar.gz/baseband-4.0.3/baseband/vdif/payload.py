# Licensed under the GPLv3 - see LICENSE
"""
Definitions for VLBI VDIF payloads.

Implements a VDIFPayload class used to store payload words, and decode to
or encode from a data array.

See the `VDIF specification page <https://www.vlbi.org/vdif>`_ for payload
specifications.
"""
from collections import namedtuple

import numpy as np

from ..base.payload import PayloadBase
from ..base.encoding import (
    encode_1bit_base, encode_2bit_base, encode_4bit_base,
    decoder_levels, decode_8bit, encode_8bit)


__all__ = ['init_luts', 'decode_1bit', 'decode_2bit', 'decode_4bit',
           'encode_1bit', 'encode_2bit', 'encode_4bit', 'VDIFPayload']


def init_luts():
    """Sets up the look-up tables for levels as a function of input byte.

    Returns
    -------
    lut1bit, lut2bit, lut4but : `~numpy.ndarray`
        Look-up table for decoding bytes to samples of 1, 2, and 4 bits, resp.

    Notes
    -----

    Look-up tables are two-dimensional arrays whose first axis is indexed
    by byte value (in uint8 form) and whose second axis represents sample
    temporal order.  Table values are decoded sample values.  Sec. 10 in
    the `VDIF Specification
    <https://vlbi.org/wp-content/uploads/2019/03/VDIF_specification_Release_1.1.1.pdf>`_
    states that samples are encoded by offset-binary, such that all 0
    bits is lowest and all 1 bits is highest.  I.e., for 2-bit sampling,
    the order is 00, 01, 10, 11.  These are decoded using
    `~baseband.base.encoding.decoder_levels`.

    For example, the 2-bit sample sequence ``-1, -1, 1, 1`` is encoded
    as ``0b10100101`` (or ``165`` in uint8 form).  To translate this back
    to sample values, access ``lut2bit`` using the byte as the key::

        >>> lut2bit[0b10100101]
        array([-1., -1.,  1.,  1.], dtype=float32)
    """
    b = np.arange(256)[:, np.newaxis]
    # 1-bit mode
    i = np.arange(8)
    lut1bit = decoder_levels[1][(b >> i) & 1]
    # 2-bit mode
    i = np.arange(0, 8, 2)
    lut2bit = decoder_levels[2][(b >> i) & 3]
    # 4-bit mode
    i = np.arange(0, 8, 4)
    lut4bit = decoder_levels[4][(b >> i) & 0xf]
    return lut1bit, lut2bit, lut4bit


lut1bit, lut2bit, lut4bit = init_luts()


def decode_1bit(words):
    b = words.view(np.uint8)
    return lut1bit.take(b, axis=0)


shift1bit = np.arange(0, 8).astype(np.uint8)


def encode_1bit(values):
    """Encodes values using 1 bit per sample, packing the result into bytes."""
    bitvalues = encode_1bit_base(values.reshape(-1, 8))
    return np.packbits(bitvalues[:, ::-1])


def decode_2bit(words):
    """Decodes data stored using 2 bits per sample."""
    b = words.view(np.uint8)
    return lut2bit.take(b, axis=0)


shift2bit = np.arange(0, 8, 2).astype(np.uint8)


def encode_2bit(values):
    """Encodes values using 2 bits per sample, packing the result into bytes.
    """
    bitvalues = encode_2bit_base(values.reshape(-1, 4))
    bitvalues <<= shift2bit
    return np.bitwise_or.reduce(bitvalues, axis=-1)


def decode_4bit(words):
    """Decodes data stored using 4 bits per sample."""
    b = words.view(np.uint8)
    return lut4bit.take(b, axis=0)


shift04 = np.array([0, 4], np.uint8)


def encode_4bit(values):
    """Encodes values using 4 bits per sample, packing the result into bytes.
    """
    b = encode_4bit_base(values).reshape(-1, 2)
    b <<= shift04
    return b[:, 0] | b[:, 1]


class VDIFPayload(PayloadBase):
    """Container for decoding and encoding VDIF payloads.

    Parameters
    ----------
    words : `~numpy.ndarray`
        Array containg LSB unsigned words (with the right size) that
        encode the payload.
    header : `~baseband.vdif.VDIFHeader`
        If given, used to infer the number of channels, bps, and whether
        the data are complex.
    sample_shape : tuple
        Shape of the samples (e.g., (nchan,)).  Default: (1,).
    bps : int, optional
        Bits per elementary sample, used if ``header`` is not given.
        Default: 2.
    complex_data : bool, optional
        Whether the data are complex, used if ``header`` is not given.
        Default: `False`.
    """
    _decoders = {1: decode_1bit,
                 2: decode_2bit,
                 4: decode_4bit,
                 8: decode_8bit}

    _encoders = {1: encode_1bit,
                 2: encode_2bit,
                 4: encode_4bit,
                 8: encode_8bit}

    _sample_shape_maker = namedtuple('SampleShape', 'nchan')

    def __init__(self, words, header=None, sample_shape=(1,), bps=2,
                 complex_data=False):
        if header is not None and header.edv == 0xab:  # Mark5B payload
            from ..mark5b import Mark5BPayload
            self._decoders = Mark5BPayload._decoders
            self._encoders = Mark5BPayload._encoders

        super().__init__(words, header=header, sample_shape=sample_shape,
                         bps=bps, complex_data=complex_data)
        # Recalculate bpfs: samples do not cross word boundaries.
        if (self.bps & (self.bps - 1)) != 0:
            if self.sample_shape != (1,):
                raise ValueError("multi-channel VDIF data requires "
                                 "bits per sample that is a power of two.")
            spw = 32 // self._bpfs
            if (spw & (spw - 1)) == 0:
                self._bpfs = 32 // spw
            else:
                raise ValueError(
                    "cannot yet sensibly handle {} data with bps={}"
                    .format('complex' if self.complex_data else 'real', bps))

    @classmethod
    def fromdata(cls, data, header=None, bps=2, edv=None):
        """Encode data as payload, using header information.

        Parameters
        ----------
        data : `~numpy.ndarray`
            Values to be encoded.
        header : `~baseband.vdif.VDIFHeader`, optional
            If given, used to infer the encoding, and to verify the number of
            channels and whether the data are complex.
        bps : int, optional
            Bits per elementary sample, used if ``header`` is not given.
            Default: 2.
        edv : int, optional
            Should be given if ``header`` is not given and the payload is
            encoded as Mark 5B data (i.e., ``edv=0xab``).
        """
        if (edv if header is None else header.edv) == 0xab:
            # Mark5B payload
            from ..mark5b import Mark5BPayload
            bps = bps if header is None else header.bps
            m5pl = Mark5BPayload.fromdata(data, bps=bps)
            return cls(m5pl.words, header, sample_shape=data.shape[1:],
                       bps=bps, complex_data=False)

        else:
            return super().fromdata(data, header=header, bps=bps)
