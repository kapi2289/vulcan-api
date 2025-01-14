# -*- coding: utf-8 -*-

import base64
import hashlib
import json
import re
import urllib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import load_der_private_key


def get_encoded_path(full_url):
    path = re.search(r"(api/mobile/.+)", full_url)
    if path is None:
        raise ValueError(
            "The URL does not seem correct (does not match `(api/mobile/.+)` regex)"
        )
    return urllib.parse.quote(path[1], safe="").lower()


def get_digest(body):
    if not body:
        return None

    m = hashlib.sha256()
    m.update(bytes(body, "utf-8"))
    return base64.b64encode(m.digest()).decode("utf-8")


def get_headers_list(body, digest, canonical_url, timestamp):
    sign_data = [
        ["vCanonicalUrl", canonical_url],
        ["Digest", digest] if body else None,
        ["vDate", timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT")],
    ]

    return (
        " ".join(item[0] for item in sign_data if item),
        "".join(item[1] for item in sign_data if item),
    )


def get_signature(data, private_key):
    data_str = json.dumps(data) if isinstance(data, (dict, list)) else str(data)
    private_key = load_der_private_key(
        base64.b64decode(private_key), password=None, backend=default_backend()
    )
    signature = private_key.sign(
        bytes(data_str, "utf-8"), padding.PKCS1v15(), hashes.SHA256()
    )
    return base64.b64encode(signature).decode("utf-8")


def get_signature_values(fingerprint, private_key, body, full_url, timestamp):
    canonical_url = get_encoded_path(full_url)
    digest = get_digest(body)
    headers, values = get_headers_list(body, digest, canonical_url, timestamp)
    signature = get_signature(values, private_key)

    return (
        f"SHA-256={digest}" if digest else None,
        canonical_url,
        f'keyId="{fingerprint}",headers="{headers}",algorithm="sha256withrsa",signature=Base64(SHA256withRSA({signature}))',
    )


def pem_getraw(pem):
    return pem.decode("utf-8").replace("\n", "").split("-----")[2]


def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    # Compute fingerprint
    fingerprint = hashes.Hash(hashes.SHA1(), backend=default_backend())
    fingerprint.update(public_pem)
    fingerprint_hex = fingerprint.finalize().hex()

    return pem_getraw(public_pem), fingerprint_hex, pem_getraw(private_pem)
