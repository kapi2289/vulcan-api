Technical info
^^^^^^^^^^^^^^

The ``hebe`` API is asynchronous (using ``asyncio``) and works using
coroutines. All the code presented in this documentation needs to be placed
inside a coroutine block (except imports, obviously).

A sample coroutine block looks as follows:

.. code-block:: python

    import asyncio

    async def main():
        # asynchronous code goes here

    if __name__ == "__main__":
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

As all the requests are also async, the API uses ``aiohttp``'s sessions,
which need to be opened and closed when needed.

Upon creation, the :class:`~vulcan.VulcanHebe` object creates a session,
which needs to be closed before the program terminates.

.. code-block:: python

    client = VulcanHebe(keystore, account)
    # use the client here
    await client.close()

It is also possible to use a context manager to handle session opening
and closing automatically.

.. code-block:: python

    client = VulcanHebe(keystore, account)
    async with client:
        # use the client here

.. warning:: Be aware that every ``with`` block creates and closes a new session.
    As per the ``aiohttp`` docs, it is recommended to group multiple requests
    to use with a single session, so it's best not to use a separate ``with`` block
    for every single request.
