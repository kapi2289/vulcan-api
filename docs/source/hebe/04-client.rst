Basic client usage
^^^^^^^^^^^^^^^^^^

To create the API client:

.. code-block:: python

    from vulcan import VulcanHebe

    client = VulcanHebe(keystore, account)

To select a student:

.. code-block:: python

    await client.select_student()  # select the first available student
    print(client.student)  # print the selected student

    students = await client.get_students()
    client.student = students[1]  # select the second student


Simple data fetching
````````````````````

All data is fetched from the :class:`~vulcan._hebe_data.VulcanHebeData` class,
available as ``client.data`` variable.

.. note:: Read the :class:`~vulcan._hebe_data.VulcanHebeData` docs to see
    all public data fetching methods.

.. code-block:: python

    lucky_number = await client.data.get_lucky_number()
    print(lucky_number)


Data fetching - technical info
``````````````````````````````

.. include:: 10-data-fetching.rst
