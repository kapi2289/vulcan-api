# -*- coding: utf-8 -*-

import pytest
from vulcan import Vulcan
from utils import *

@pytest.mark.private
@pytest.mark.online
@pytest.fixture
def client():
    cert = {k: load_variable(k) for k in [
        'CertyfikatPfx',
        'CertyfikatKluczSformatowanyTekst',
        'CertyfikatKlucz',
        'AdresBazowyRestApi']}
    yield Vulcan(cert)
