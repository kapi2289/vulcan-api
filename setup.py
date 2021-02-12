# -*- coding: utf-8 -*-

import io
import re
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with io.open(path.join(here, "README.md"), "rt", encoding="utf8") as f:
    long_description = f.read()

with io.open(path.join(here, "vulcan/__init__.py"), "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \"(.*?)\"", str(f.read())).group(1)

setup(
    name="vulcan-api",
    version=version,
    packages=find_packages(),
    author="Kacper Ziubryniewicz",
    author_email="kapi2289@gmail.com",
    description="Nieoficjalne API do dzienniczka elektronicznego UONET+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["Vulcan", "UONET+", "Dzienniczek+", "API", "e-dziennik", "hebe"],
    license="MIT",
    url="https://github.com/kapi2289/vulcan-api",
    project_urls={"Documentation": "https://vulcan-api.readthedocs.io/"},
    python_requires=">=3.6,<4.0",
    install_requires=[
        "requests",
        "pyopenssl",
        "uonet-request-signer-hebe",
        "pytz",
        "aenum",
        "related",
        "aiohttp",
        "cchardet",
        "aiodns",
        "yarl",
    ],
    extras_require={"testing": ["pytest", "python-dotenv"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Polish",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
