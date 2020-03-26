API registration
^^^^^^^^^^^^^^^^

To register the API as a mobile device, login to your e-register
page (https://uonetplus.vulcan.net.pl/<symbol>) and go to the mobile
access page.

.. image:: /_static/registration1.png

.. image:: /_static/registration2.png

Then use the :func:`vulcan.Vulcan.register` function

.. code:: python

    from vulcan import Vulcan
    import json

    certificate = Vulcan.register('<token>', '<symbol>', '<pin>')


And then save the generated certificate to a file

.. code:: python

    with open('cert.json', 'w') as f: # You can use other filename
        json.dump(certificate.json, f)
