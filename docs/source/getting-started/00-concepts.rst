Core concepts and definitions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to use the API, it's important to understand some concepts
and naming conventions in the API.

* ``symbol`` - sometimes referred to as "partition symbol".
  This is a textual grouping symbol representing a group of
  e-register instances: a town, a county or a part of them.
  The symbol is present in the e-register website URL:

    ``https://uonetplus.vulcan.net.pl/<symbol>``

* ``code`` - or "school code" - a code representing a single school
  or few grouped (in an unit) school buildings. Often in the form
  of ``001234``, sometimes also containing alphabet characters.
  Present in the URL:

    ``https://uonetplus.vulcan.net.pl/<symbol>/<code>``


* :class:`~vulcan.model.Unit` - a group of schools, sharing a similar name. May contain
  only one school.
* :class:`~vulcan.model.School` - a part of a ``unit``.


* :class:`~vulcan.Keystore` - login data for an instance of the API. **Might
  be tied (registered) to multiple accounts.**
* :class:`~vulcan.Account` - an account from a single ``symbol``, containing
  one or more ``students``, accessed using a corresponding ``keystore``.
* :class:`~vulcan.model.Student` - a person, school attendant.
