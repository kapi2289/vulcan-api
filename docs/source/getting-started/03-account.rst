Account registration
^^^^^^^^^^^^^^^^^^^^

It is now necessary to register the previously created :class:`~vulcan.Keystore`
in the e-register, in order to get access to the :class:`~vulcan.Account`'s data.

The Token, Symbol and PIN need to be obtained from the Vulcan e-register student/parent
panel (in the "Mobile access/Dostęp mobilny" tab):

.. code-block:: python

    from vulcan import Account

    account = Account.register(keystore, token, symbol, pin)

Just as for the keystore, it's recommended to save the account credentials
for later usage:

.. code-block:: python

    with open("account.json", "w") as f:
        # use one of the options below:
        # write a formatted JSON representation
        f.write(account.as_json)
        # dump a dictionary as JSON to file (needs `json` import)
        json.dump(account.as_dict, f)

An account may be loaded back as follows:

.. code-block:: python

    with open("account.json") as f:
        # use one of the options below:
        # load from a file-like object
        account = Account.load(f)
        # load from a JSON string
        account = Account.load(f.read())
        # load from a dictionary (needs `json` import)
        account = Account.load(json.load(f))

You are now ready to use the API. The keystore and account registration is a one-time step.
