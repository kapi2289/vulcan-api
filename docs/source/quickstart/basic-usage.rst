Basic usage
===========

When you have API already registered, you can now use it

.. code:: python

    from vulcan import Vulcan
    import json

    # Load certificate from a file
    with open('cert.json') as f:
        cert = json.loads(f.read())

    # Create a client
    client = Vulcan(cert)

API automatically selects the first available pupil, if you have more than one pupil you can get all of them, and set the default one

.. code:: python

    users = client.users()
    user = users[0]

    client.change_user(user)
