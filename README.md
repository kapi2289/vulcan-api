<h1 align="center">Vulcan API</h1>
<p align="center">
    <a href="https://github.com/kapi2289/vulcan-api/blob/master/LICENSE"><img src="https://img.shields.io/pypi/l/vulcan-api.svg" alt="License"></a>
    <a href="https://pypi.org/project/vulcan-api/"><img src="https://img.shields.io/pypi/v/vulcan-api.svg" alt="Version"></a>
    <a href="https://pypi.org/project/vulcan-api/"><img src="https://img.shields.io/pypi/pyversions/vulcan-api.svg" alt="Supported Python versions"></a>
    <a href="https://discord.gg/sTHCrXB"><img src="https://img.shields.io/discord/619178050562686988?color=7289DA&label=discord" alt="Discord"></a>
</p>
<p align="center">
    <a href="https://travis-ci.com/kapi2289/vulcan-api"><img src="https://travis-ci.com/kapi2289/vulcan-api.svg?branch=master" alt="Tests status"></a>
    <a href="https://vulcan-api.readthedocs.io/pl/latest/?badge=latest"><img src="https://img.shields.io/readthedocs/vulcan-api.svg" alt="Documentation status"></a>
</p>
<p align="center">
    <a href="https://pypi.org/project/vulcan-api/"><img src="https://img.shields.io/pypi/dd/vulcan-api.svg" alt="Daily downloads"></a>
    <a href="https://pypi.org/project/vulcan-api/"><img src="https://img.shields.io/pypi/dw/vulcan-api.svg" alt="Weekly downloads"></a>
    <a href="https://pypi.org/project/vulcan-api/"><img src="https://img.shields.io/pypi/dm/vulcan-api.svg" alt="Monthly downloads"></a>
</p>

## Description

Unofficial API for UONET+ e-register from [Vulcan](https://vulcan.edu.pl/). It's using the mobile API so you can register it as a mobile devide.

![](https://raw.githubusercontent.com/kapi2289/vulcan-api/master/docs/source/_static/registered.png)

## Installation

You can install `vulcan-api` using pip and git

## Changes of fork

All networking is handled by aiohttp library which solves GIL problem. This means better performance in Concurrent usage
(like discord bots, small async http servers etc.)

### Windows
```console
python -m pip install git+https://github.com/kpostekk/vulcan-api.git
```

### Linux and MacOS
```console
pip3 install git+https://github.com/kpostekk/vulcan-api.git
```

## Documentation

You can find the documentation at https://vulcan-api.readthedocs.io/pl/async.
