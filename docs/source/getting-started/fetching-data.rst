Fetching data
^^^^^^^^^^^^^

Now you can fetch any data from your account, for example grades

.. warning::
    Remember that functions return *generators*, **NOT** *lists*.
    If you want to get a list, you need to pass the *generator* to the *list* function.
    e.g. *grade_list = list(client.get_grades())*

.. code:: python

    for grade in client.get_grades():
        print(grade.content)
        print(grade.subject.name)
        print(grade.teacher.name)
