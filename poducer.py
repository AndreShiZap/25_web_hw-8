import pika

from faker import Faker
from random import choice
from model_contact import Contact


fake = Faker()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)
channel.queue_declare(queue='sms_queue', durable=True)


def create_contacts(count=10):
    contacts = []
    for _ in range(count):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            best_way=choice(["email", "sms"])
        )
        contact.save()
        contacts.append(contact)
        print(f'contact created: {contact}')
    return contacts


def send_to_queue(contacts):
    for contact in contacts:
        if contact.best_way == 'email':
            queue_name = 'email_queue'
        else:
            queue_name = 'sms_queue'
        contact_id = str(contact.id)
        channel.basic_publish(exchange='', routing_key=queue_name, body=contact_id)
        print(f'Contact ID sent to queue {queue_name}: {contact_id}')


if __name__ == '__main__':
    contacts = create_contacts(10)
    send_to_queue(contacts)
    connection.close()
