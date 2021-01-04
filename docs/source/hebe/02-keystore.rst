Keystore creation
^^^^^^^^^^^^^^^^^

The first step is to create a :class:`~vulcan.Keystore`, which will be used to access
any account to which it's registered:

.. code-block:: python

    from vulcan import Keystore

    keystore = Keystore.create()
    # or with an explicitly passed device model
    keystore = Keystore.create(device_model="Vulcan hebe API")

The keystore is now ready to be registered in exchange for an :class:`~vulcan.Account`,
but it's best to save it for later use:

.. code-block:: python

    with open("keystore.json", "w") as f:
        # use one of the options below:
        # write a formatted JSON representation
        f.write(keystore.as_json)
        # dump a dictionary as JSON to file (needs `json` import)
        json.dump(keystore.as_dict, f)

A once-saved keystore may be simply loaded back into an API-usable object:

.. code-block:: python

    with open("keystore.json") as f:
        # use one of the options below:
        # load from a file-like object
        keystore = Keystore.load(f)
        # load from a JSON string
        keystore = Keystore.load(f.read())
        # load from a dictionary (needs `json` import)
        keystore = Keystore.load(json.load(f))

The keystore is now ready for further usage.
