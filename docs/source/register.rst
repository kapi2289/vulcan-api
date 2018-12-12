Registering API
===============

First, you need to register API as a mobile device on https://uonetplus.vulcan.net.pl/symbol

.. image:: https://i.imgur.com/x03Aykd.png

.. image:: https://i.imgur.com/OVr5Px4.png

.. code:: python

    from vulcan import Vulcan
    import json

    # Vulcan.create(token, symbol, pin)
    cert = Vulcan.create('3S1GFG0P', 'gminaglogow', '059671')

    # Save certificate to a file
    with open('cert.json') as f:
        f.write(json.dumps(cert))
