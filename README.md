<h1 align="center">Vulcan API</h1>
<p align="center">
    <a href="https://github.com/kapi2289/vulcan-api/blob/master/LICENSE"><img src="https://img.shields.io/pypi/l/vulcan-api.svg" alt="License"></a>
    <a href="https://pypi.org/project/vulcan-api/"><img src="https://img.shields.io/pypi/v/vulcan-api.svg" alt="Version"></a>
    <a href="https://pypi.org/project/vulcan-api/"><img src="https://img.shields.io/pypi/pyversions/vulcan-api.svg" alt="Supported Python versions"></a>
    <a href="https://discord.gg/sTHCrXB"><img src="https://img.shields.io/discord/619178050562686988?color=7289DA&label=discord" alt="Discord"></a>
</p>
<p align="center">
    <a href="https://github.com/kapi2289/vulcan-api/actions/workflows/test.yml"><img src="https://img.shields.io/github/workflow/status/kapi2289/vulcan-api/Run%20tests/master" alt="Tests status"></a>
    <a href="https://vulcan-api.readthedocs.io/en/latest/?badge=latest"><img src="https://img.shields.io/readthedocs/vulcan-api.svg" alt="Documentation status"></a>
</p>
<p align="center">
    <a href="https://pypi.org/project/vulcan-api/"><img src="https://img.shields.io/pypi/dd/vulcan-api.svg" alt="Daily downloads"></a>
    <a href="https://pypi.org/project/vulcan-api/"><img src="https://img.shields.io/pypi/dw/vulcan-api.svg" alt="Weekly downloads"></a>
    <a href="https://pypi.org/project/vulcan-api/"><img src="https://img.shields.io/pypi/dm/vulcan-api.svg" alt="Monthly downloads"></a>
</p>

## Important information

After February 21st the old mobile app "Dzienniczek+" was shutdown by Vulcan, along with its API.
This library provides compatibility with the new app's API (starting with v2.0.0), but because
of the incompatibility between both APIs' signing mechanisms, a manual migration is required.

A device using the system must be registered again (using the token, symbol and PIN). Additionally,
data models and synchronisation method differ, and the API is now asynchronous.

For the details, refer to the [Documentation](https://vulcan-api.readthedocs.io/).

## Description

Unofficial API for UONET+ e-register from [Vulcan](https://vulcan.edu.pl/). It's using the mobile API, so you can register it as a mobile device.

![](https://raw.githubusercontent.com/kapi2289/vulcan-api/master/docs/source/_static/registered.png)

## Installation

You can install `vulcan-api` using `pip`

```console
$ python -m pip install vulcan-api
```

or you can build yourself the latest version

```console
$ git clone https://github.com/kapi2289/vulcan-api.git
$ cd vulcan-api
$ python -m pip install .
```

## Documentation

You can find the documentation at https://vulcan-api.readthedocs.io/.
