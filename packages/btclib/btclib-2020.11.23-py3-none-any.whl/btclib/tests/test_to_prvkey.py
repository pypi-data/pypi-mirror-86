#!/usr/bin/env python3

# Copyright (C) 2017-2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

"Tests for `btclib.to_prvkey` module."

import pytest

from btclib.curve import CURVES
from btclib.exceptions import BTClibValueError
from btclib.tests.test_to_key import (
    INF,
    INF_xpub_data,
    Q,
    compressed_prv_keys,
    compressed_pub_keys,
    invalid_prv_keys,
    net_aware_prv_keys,
    net_unaware_prv_keys,
    not_a_prv_keys,
    plain_prv_keys,
    plain_pub_keys,
    q,
    q0,
    qn,
    uncompressed_prv_keys,
    uncompressed_pub_keys,
    xprv0_data,
    xprv_data,
    xprvn_data,
    xpub_data,
)
from btclib.to_prvkey import int_from_prvkey, prvkeyinfo_from_prvkey

# FIXME: fix error messages


def test_from_prvkey() -> None:

    secp256r1 = CURVES["secp256r1"]
    m_c = (q, "mainnet", True)
    m_unc = (q, "mainnet", False)
    t_c = (q, "testnet", True)
    t_unc = (q, "testnet", False)
    for prv_key in [q] + plain_prv_keys:
        assert q == int_from_prvkey(prv_key)
        assert q == int_from_prvkey(prv_key, secp256r1)
        assert m_c == prvkeyinfo_from_prvkey(prv_key)
        assert m_c == prvkeyinfo_from_prvkey(prv_key, "mainnet")
        assert m_c == prvkeyinfo_from_prvkey(prv_key, "mainnet", compressed=True)
        assert m_c == prvkeyinfo_from_prvkey(prv_key, compressed=True)
        assert m_unc == prvkeyinfo_from_prvkey(prv_key, "mainnet", compressed=False)
        assert m_unc == prvkeyinfo_from_prvkey(prv_key, compressed=False)
        assert t_c == prvkeyinfo_from_prvkey(prv_key, "testnet")
        assert t_c == prvkeyinfo_from_prvkey(prv_key, "testnet", compressed=True)
        assert t_unc == prvkeyinfo_from_prvkey(prv_key, "testnet", compressed=False)

    for prv_key in [xprv_data] + compressed_prv_keys:
        assert q == int_from_prvkey(prv_key)
        with pytest.raises(BTClibValueError):
            int_from_prvkey(prv_key, secp256r1)
        assert m_c == prvkeyinfo_from_prvkey(prv_key)
        assert m_c == prvkeyinfo_from_prvkey(prv_key, "mainnet")
        assert m_c == prvkeyinfo_from_prvkey(prv_key, "mainnet", compressed=True)
        assert m_c == prvkeyinfo_from_prvkey(prv_key, compressed=True)
        with pytest.raises(BTClibValueError):
            prvkeyinfo_from_prvkey(prv_key, "mainnet", compressed=False)
        with pytest.raises(BTClibValueError):
            prvkeyinfo_from_prvkey(prv_key, compressed=False)
        with pytest.raises(BTClibValueError):
            prvkeyinfo_from_prvkey(prv_key, "testnet")
        with pytest.raises(BTClibValueError):
            prvkeyinfo_from_prvkey(prv_key, "testnet", compressed=True)
        with pytest.raises(BTClibValueError):
            prvkeyinfo_from_prvkey(prv_key, "testnet", compressed=False)

    for prv_key in uncompressed_prv_keys:
        assert q == int_from_prvkey(prv_key)
        with pytest.raises(BTClibValueError):
            int_from_prvkey(prv_key, secp256r1)
        assert m_unc == prvkeyinfo_from_prvkey(prv_key)
        assert m_unc == prvkeyinfo_from_prvkey(prv_key, "mainnet")
        with pytest.raises(BTClibValueError):
            prvkeyinfo_from_prvkey(prv_key, "mainnet", compressed=True)
        with pytest.raises(BTClibValueError):
            prvkeyinfo_from_prvkey(prv_key, compressed=True)
        assert m_unc == prvkeyinfo_from_prvkey(prv_key, "mainnet", compressed=False)
        assert m_unc == prvkeyinfo_from_prvkey(prv_key, compressed=False)
        with pytest.raises(BTClibValueError):
            prvkeyinfo_from_prvkey(prv_key, "testnet")
        with pytest.raises(BTClibValueError):
            prvkeyinfo_from_prvkey(prv_key, "testnet", compressed=True)
        with pytest.raises(BTClibValueError):
            prvkeyinfo_from_prvkey(prv_key, "testnet", compressed=False)

    for prv_key in [xprv_data] + net_aware_prv_keys:
        assert q == int_from_prvkey(prv_key)
        with pytest.raises(BTClibValueError):
            int_from_prvkey(prv_key, secp256r1)
        assert prvkeyinfo_from_prvkey(prv_key) in (m_c, m_unc)
        assert prvkeyinfo_from_prvkey(prv_key, "mainnet") in (m_c, m_unc)
        with pytest.raises(BTClibValueError):
            prvkeyinfo_from_prvkey(prv_key, "testnet")

    for prv_key in [q] + net_unaware_prv_keys:
        assert q == int_from_prvkey(prv_key)
        assert q == int_from_prvkey(prv_key, secp256r1)
        assert prvkeyinfo_from_prvkey(prv_key) in (m_c, m_unc)
        assert prvkeyinfo_from_prvkey(prv_key, "mainnet") in (m_c, m_unc)
        assert prvkeyinfo_from_prvkey(prv_key, "testnet") in (t_c, t_unc)

    for invalid_prv_key in [q0, qn, xprv0_data, xprvn_data] + invalid_prv_keys:
        with pytest.raises(BTClibValueError):
            int_from_prvkey(invalid_prv_key)
        with pytest.raises(BTClibValueError):
            prvkeyinfo_from_prvkey(invalid_prv_key)

    for not_a_prv_key in (
        [q0, qn, xprv0_data, xprvn_data]
        + [INF, INF_xpub_data]
        + not_a_prv_keys
        + [Q]
        + plain_pub_keys
        + [xpub_data]
        + compressed_pub_keys
        + uncompressed_pub_keys
    ):
        with pytest.raises(BTClibValueError):
            int_from_prvkey(not_a_prv_key)
        with pytest.raises(BTClibValueError):
            prvkeyinfo_from_prvkey(not_a_prv_key)
