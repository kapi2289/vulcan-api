Fetching the tests
==================

To fetch the tests for a specific day, you can use ``tests`` method. If no arguments, returnes the tests for today.

.. code:: python

    from datetime import date

    tests = client.tests(date.today())

``tests`` returs a list of dicts

.. code:: python

    >> tests[0]

    {
        'Id': 1221,
        'IdPrzedmiot': 173,
        'IdPracownik': 99,
        'IdOddzial': 55,
        'IdPodzial': None,
        'PodzialNazwa': None,
        'PodzialSkrot': None,
        'Rodzaj': True,
        'RodzajNumer': 1,
        'Opis': '',
        'Data': 1544742000,
        'DataTekst': '2018-12-14',
        'Przedmiot': {
            'Id': 173,
            'Nazwa': 'Fizyka',
            'Kod': 'fizyka',
            'Aktywny': True,
            'Pozycja': 9
        },
        'Pracownik': {
            'Id': 99,
            'Imie': 'Jan',
            'Nazwisko': 'Kowalski',
            'Kod': 'JK',
            'Aktywny': True,
            'Nauczyciel': False,
            'LoginId': 496
        },
        'DataObjekt': datetime.date(2018, 12, 14)
    }
