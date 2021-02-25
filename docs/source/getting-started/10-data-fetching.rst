All data getting methods are asynchronous.

There are three return types of those methods:

- object - applies to methods returning a single object (e.g. the currently
  selected student, the today's lucky number, the server date-time)
- list - applies to :func:`~vulcan.Vulcan.get_students`. The list is either
  read from the server or the in-memory cache.
- `AsyncIterator` - applies to all other data fetching methods. The returned
  iterator may be used like this:

  .. code-block:: python

      grades = await client.data.get_grades()

      # with a for loop
      async for grade in grades:
          print(grade)

      # convert to a list
      grades = [grade async for grade in grades]
      print(grades[0])
      for grade in grades:
          print(grade)

.. note:: You cannot re-use the AsyncIterator (once iterated through). As it is
    asynchronous, you also cannot use the next() method on it.
