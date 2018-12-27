# -*- coding: utf-8 -*-

from setuptools import setup

from os import path
import re
import io


here = path.abspath(path.dirname(__file__))

with io.open(path.join(here, "README.rst"), 'rt', encoding='utf8') as f:
    long_description = f.read()

with io.open(path.join(here, "vulcan/__init__.py"), 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name="vulcan-api",
    version=version,
    packages=['vulcan'],
    author="Kacper Ziubryniewicz",
    author_email="kapi2289@gmail.com",
    description="Nieoficjalne API do dzienniczka elektronicznego UONET+",
    long_description=long_description,
    long_description_content_type='text/x-rst',
    keywords=["Vulcan", "UONET+", "Dzienniczek+", "API", "e-dziennik"],
    license="MIT",
    url="https://github.com/kapi2289/vulcan-api",
    project_urls={
        "Documentation": "https://vulcan-api.readthedocs.io/"
    },
    python_requires=">2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,<4.0",
    install_requires=[
        'requests',
        'pyopenssl',
    ],
    extra_requires={
        "test": [
            'pytest',
        ],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Polish",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)