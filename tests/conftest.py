# -*- coding: utf-8 -*-

from hashlib import md5

import pytest

from vulcan import Vulcan


@pytest.mark.online
@pytest.fixture(scope="module")
def client():
    cert = Vulcan.register("FK100000", "powiatwulkanowy", "123456")
    assert (
        md5(cert.pfx.encode("utf-8")).hexdigest() == "4c168702befb4c6ef356c77fd23fedaa"
    )
    assert cert.key == "7EBA57E1DDBA1C249D097A9FF1C9CCDD45351A6A"
    assert (
        cert.key_formatted
        == "7E-BA-57-E1-DD-BA-1C-24-9D-09-7A-9F-F1-C9-CC-DD-45-35-1A-6A"
    )
    assert cert.base_url == "http://api.fakelog.cf/powiatwulkanowy/"
    yield Vulcan(cert)
