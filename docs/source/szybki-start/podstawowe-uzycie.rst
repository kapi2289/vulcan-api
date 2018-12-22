Podstawowe użycie
^^^^^^^^^^^^^^^^^

Po zarejestrowaniu API możesz już go używać!

Najpierw wczytujemy certyfikat z pliku,

.. code:: python

    from vulcan import Vulcan
    import json

    with open('cert.json') as f:
        certyfikat = json.loads(f.read())


a następnie tworzymy klienta przy użyciu tego certyfikatu

.. code:: python

    klient = Vulcan(certyfikat)


API automatycznie ustawia pierwszego dostępnego ucznia jako domyślnego.
Jeżeli twoje konto posiada więcej niż jednego ucznia, możesz pobrać wszystkich uczniów
przy użyciu :func:`vulcan.Vulcan.uczniowie`,

.. code:: python

    uczniowie = klient.uczniowie()


a następnie ustawić domyślnego za pomocą :func:`vulcan.Vulcan.ustaw_ucznia`

.. code:: python

    uczeń = uczniowie[0]
    klient.ustaw_ucznia(uczeń)
