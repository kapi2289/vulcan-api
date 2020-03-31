from vulcan import Vulcan
import json
with open('cert.json') as f:
    certificate = json.load(f)
client = Vulcan(certificate)
for student in client.get_students():
	student_id=student.id
	print(student_id)
for teacher in client.get_teachers(student_id):
	print(teacher)
"""
name="Luszowski Tobiasz"
title="Test2"
recipients="Arkadiusz Waliczek"
content="Adresat: "+recipients
recipients="Arkadiusz Waliczek"
client.send_message(name, title, content, recipients)
print("Wysłano")
"""