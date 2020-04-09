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
    import asyncio
    import json

    async def main():
        certificate = async Vulcan.register('<token>', '<symbol>', '<pin>')


Then save the generated certificate to a file

.. code:: python

    async def main():
        certificate = async Vulcan.register('<token>', '<symbol>', '<pin>')
        with open('cert.json', 'w') as f: # You can use other filename
            json.dump(certificate.json, f)

And finally run your code

.. code:: python

    if __name__ == '__main__':
        asyncio.run(main())
