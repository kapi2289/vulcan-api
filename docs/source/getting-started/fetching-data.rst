Fetching data
^^^^^^^^^^^^^

Now you can fetch any data from your account, for example grades

.. warning::
    Remember that functions return *async_generators*, **NOT** *lists*.
    If you want to get a list, you need to use `async for` and *lists comprehension*.
    Also, in some cases you can use `await async_gen.__anext__()`.
    e.g. *grade_list = [_ async for _ in await client.get_grades()]*
    You can find alias of this in `from vulcan._utils import alist` coroutine.

.. code:: python

    from vulcan._utils import alist

    for grade in await alist(client.get_grades()):
        print(grade.content)
        print(grade.subject.name)
        print(grade.teacher.name)
