Fetching the lesson plan
========================

You can use ``lesson_plan()`` method to fetch the lesson plan for a specific day. If no arguments, gives the lesson plan for today.

.. code::

    from datetime import date

    plan = client.lesson_plan(date.today())

``lesson_plan()`` returns a list of dicts.

.. code:: python

    >> plan[0]

    {
        'Dzien': 1544655600,
        'DzienTekst': '2018-12-13',
        'NumerLekcji': 1,
        'IdPoraLekcji': 36,
        'IdPrzedmiot': 172,
        'PrzedmiotNazwa': 'Matematyka',
        'PodzialSkrot': None,
        'Sala': None,
        'IdPracownik': 92,
        'IdPracownikWspomagajacy': None,
        'IdPracownikOld': None,
        'IdPracownikWspomagajacyOld': None,
        'IdPlanLekcji': 4,
        'AdnotacjaOZmianie': '',
        'PrzekreslonaNazwa': False,
        'PogrubionaNazwa': False,
        'PlanUcznia': True,
        'DzienObjekt': datetime.date(2018, 12, 13),
        'PoraLekcji': {
            'Id': 36,
            'Numer': 1,
            'Poczatek': 26100,
            'PoczatekTekst': '08:15',
            'Koniec': 28800,
            'KoniecTekst': '09:00'
        },
        'Przedmiot': {
            'Id': 172,
            'Nazwa': 'Matematyka',
            'Kod': 'matematyka',
            'Aktywny': True,
            'Pozycja': 8
        },
        'Pracownik': {
            'Id': 92,
            'Imie': 'Jan',
            'Nazwisko': 'Kowalski',
            'Kod': 'JK',
            'Aktywny': True,
            'Nauczyciel': False,
            'LoginId': 493
        },
        'PracownikWspomagajacy': None
    }
