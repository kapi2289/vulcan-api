# Vulcan API

## Description
Python API for Vulcan e-journal system. It's based on the mobile app, so you need to register it as a mobile device on the site.

![image](https://i.imgur.com/AKBkOJq.png)

## Installation
You can install `vulcan-api` by `pip`
```bash
pip install vulcan-api
```

Or manually
```bash
pip install flit
git clone https://bitbucket.org/kapi2289/vulcan-api.git
cd vulcan-api
flit install
```

## Usage
First, you need to register API as a mobile device on https://uonetplus.vulcan.net.pl/symbol

![image](https://i.imgur.com/x03Aykd.png)

![image](https://i.imgur.com/OVr5Px4.png)

```python
from vulcan import Vulcan
import json

# Vulcan.create(token, symbol, pin)
cert = Vulcan.create('3S1GFG0P', 'gminaglogow', '059671')

# Save certificate to a file
with open('cert.json') as f:
    f.write(json.dumps(cert))
```

When you have API already registered, you can now use it

```python
from vulcan import Vulcan
import json

# Load certificate from a file
with open('cert.json') as f:
    cert = json.loads(f.read())

# Create a client
client = Vulcan(cert)
```

API automatically selects first pupil, if you have more than one pupil you can get all of them, and set the default

```python
users = client.users()
user = users[0]

client.change_user(user)
```

For further instructions go to the [documentation](https://vulcan-api.readthedocs.io/).
