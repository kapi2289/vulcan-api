Fetching the homeworks
======================

For fetching the homeworks for a specific day you can use ``homeworks()`` method. If no arguments, returns the tests for today.

.. code:: python

    from datetime import date

    homeworks = client.homeworks(date.today())

``homeworks()`` returns a list of dicts.

.. code:: python

    >> homeworks[0]

    {
        'Id': 447,
        'IdUczen': 756,
        'Data': 1544655600,
        'DataTekst': '2018-12-13',
        'IdPracownik': 85,
        'IdPrzedmiot': 185,
        'Opis': 'Zadanie 8, 9 strona 74',
        'DataObjekt': datetime.date(2018, 12, 13),
        'Pracownik': {
            'Id': 85,
            'Imie': 'Jan',
            'Nazwisko': 'Kowalski',
            'Kod': 'JK',
            'Aktywny': True,
            'Nauczyciel': False,
            'LoginId': 477
        },
        'Przedmiot': {
            'Id': 185,
            'Nazwa': 'Informatyka',
            'Kod': 'informatyka',
            'Aktywny': True,
            'Pozycja': 17
        }
    }
