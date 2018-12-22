Rejestracja API
^^^^^^^^^^^^^^^

Aby zarejestrować API jako urządzenie mobilne, udaj się na stronę
swojego dziennika (https://uonetplus.vulcan.net.pl/symbol) i wejdź
w zakładkę *Dostęp mobilny*.

.. image:: /_static/rejestracja1.png

.. image:: /_static/rejestracja2.png

Do rejestracji API użyj funkcji :func:`vulcan.Vulcan.zarejestruj`

.. code:: python

    from vulcan import Vulcan
    import json

    # Vulcan.zarejestruj(token, symbol, pin)
    certyfikat = Vulcan.zarejestruj('3S1GFG0P', 'gminaglogow', '059671')


A następnie zapisz certyfikat do pliku

.. code:: python

    with open('cert.json') as f:
        f.write(json.dumps(certyfikat))
