# -*- coding: UTF-8 -*-

import pytest
from vulcan import Vulcan
from utils import *

@pytest.fixture
def client():
    cert = {k: load_variable(k) for k in [
        'CertyfikatPfx',
        'CertyfikatKluczSformatowanyTekst',
        'CertyfikatKlucz',
        'AdresBazowyRestApi']}
    yield Vulcan(cert)
