from mongoengine import connect, Document, StringField, BooleanField

connect(db="hw", host="mongodb+srv://andreshizap:567234@cluster0.pqxcf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")


class Contact(Document):
    fullname = StringField(required=True, unique=True)
    email = StringField(required=True, max_length=150)
    message_sent = BooleanField(default=False)
    phone = StringField(max_length=30)
    best_way = StringField(max_length=5)
    meta = {"collection": "contacts"}
