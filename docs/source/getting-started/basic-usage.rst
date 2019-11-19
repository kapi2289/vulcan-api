Basic usage
^^^^^^^^^^^

After registering API, now you can use it!

First of all, you need to load a certificate from a file

.. code:: python

    from vulcan import Vulcan
    import json

    with open('cert.json') as f:
        certificate = json.loads(f.read())


and then, you need to create a client using the loaded certificate

.. code:: python

    client = Vulcan(certificate)


API automatically sets the first available student as default.
If your account has more than one student, you can fetch all students
using :func:`vulcan.Vulcan.get_students` and set one of them as default

.. code:: python

    for student in client.get_students():
        if student.name == "Jan Kowalski":
            client.set_student(student)
            break
