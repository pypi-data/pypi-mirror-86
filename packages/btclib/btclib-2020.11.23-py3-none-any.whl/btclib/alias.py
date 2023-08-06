#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

"""Aliases

mypy aliases, documenting also coding imput conventions.
"""

from io import BytesIO
from typing import Any, Callable, List, Tuple, Union

# Octets are a sequence of eight-bit bytes or a hex-string (not text string)
#
# hex-strings are strings that can be converted to bytes using bytes.fromhex,
# e.g.:
# "deadbeef"
# "dead beef"
# "04 cc71eb30d653c0c3163990c47b976f3fb3f37cccdcbedb169a1dfef58bbfbfaf f7d8a473e7e2e6d317b87bafe8bde97e3cf8f065dec022b51d11fcdd0d348ac4"
# "02 cc71eb30d653c0c3163990c47b976f3fb3f37cccdcbedb169a1dfef58bbfbfaf"
# "02cc71eb30d653c0c3163990c47b976f3fb3f37cccdcbedb169a1dfef58bbfbfaf"
#
# use btclib.utils.bytes_from_octets to convert Octets to bytes
#
# Octets are used for serialized script, h160 (20 bytes), h256 (32 bytes),
# BIP32 version (4 bytes), sighash (1 byte),
# DSASig (DER serialization of ECDSA signature),
# BMSig (Bitcoin message compact signature serialization, 65 bytes),
# etc.
Octets = Union[bytes, str]

# bytes or text string (not hex-string)
#
# this is for string that can be
# converted to bytes using encode()
# e.g. a message to be signed
#    if isinstance(msg, str):
#        msg = msg.encode()
#
# or 'ascii' strings like addresses (base58 or bech32),
# WIFs, or BIP32 keys:
# "37k7toV1Nv4DfmQbmZ8KuZDQCYK9x5KpzP"
# "KyLk7s6Z1FtgYEVp3bPckPVnXvLUWNCcVL6wNt3gaT96EmzTKZwP"
# "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi"
# "bc1qg9stkxrszkdqsuj92lm4c7akvk36zvhqw7p6ck"
#
# In almost all cases (but messages to be signed)
# leading/trailing blanks should always be stripped
#     if isinstance(b58addr, str):
#         b58addr = b58addr.strip()
#
# In those cases often there is no need to encode() to bytes
# as b58decode/b32decode/etc. will take care of that
String = Union[bytes, str]

# binary data, usually to be cosumed as byte stream,
# but possibily provided as Octets too
BinaryData = Union[BytesIO, Octets]

# hex-string or bytes representation of an int
# Integer = Union[Octets, int]
Integer = Union[bytes, str, int]

# Hash digest constructor: it may be any name suitable to hashlib.new()
HashF = Callable[[], Any]
# HashF = Callable[[Any], Any]

# Elliptic curve point in affine coordinates.
# Warning: to make Point a NamedTuple would slow down the code
Point = Tuple[int, int]

# Note that the infinity point in affine coordinates is INF = (int, 0)
# (no affine point has y=0 coordinate in a group of prime order n).
# It can be checked with 'INF[1] == 0'
# The x-coordinate is arbitrary: 7 is preferred
# because it is not a field element in secp256k1
INF = 7, 0

# Elliptic curve point in Jacobian coordinates.
JacPoint = Tuple[int, int, int]

# Infinity point in Jacobian coordinates is INF = (int, int, 0).
# It can be checked with 'INF[2] == 0'
# The default x and y coordinates are arbitrary:
# 7, 0 are used because those are what one would obtain
# from the generic affine to Jacobian transformation
# of the INF Point
# QJ = Q[0], Q[1], 1 if Q[1] else 0
INFJ = 7, 0, 0

# the main internal representation of entropy is binary 0/1 string
BinStr = str
# but int or bytes are fine too
Entropy = Union[BinStr, int, bytes]

# ECDSA signature
# (r, s)
# both r and s are scalar: 0 < r < ec.n, 0 < s < ec.n
DSASigTuple = Tuple[int, int]
# DSASigTuple or DER serialization (bytes or hex-string, no sighash)
DSASig = Union[DSASigTuple, Octets]

# BIP340-Schnorr signature
# (r, s)
# r is a _field_element_, 0 <= r < ec.p
# s is a scalar, 0 <= s < ec.n (yes, for BIP340-Schnorr it can be zero)
# (p is the field prime, n is the curve order)
SSASigTuple = Tuple[int, int]
# SSASigTuple or BIP340-Schnorr 64-bytes serialization (bytes or hex-string)
SSASig = Union[SSASigTuple, Octets]

# the integers [0-16] are shorcuts for 'OP_0'-'OP_16'
# the integer -1 is a shorcut for 'OP_1NEGATE'
# other integers are bytes encoded (require push operation)
# ascii str are for opcodes (e.g. 'OP_HASH160')
# Octets are for data to be pushed
ScriptToken = Union[int, str, bytes]

# Bitcoin script expressed as List[ScriptToken]
# e.g. [OP_HASH160, script_h160, OP_EQUAL]
# or Octets of its byte-encoded representation
Script = Union[Octets, List[ScriptToken]]

# Object that can be textually saved without any conversion
Printable = Union[int, str]
