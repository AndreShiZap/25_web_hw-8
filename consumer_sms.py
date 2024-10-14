import os
import sys

import pika

from model_contact import Contact


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='sms_queue', durable=True)

    channel.basic_qos(prefetch_count=1)


# Функция-заглушка
    def send_sms(contact):
        print(f'Sending sms to number {contact.phone}...')
        return True


    def callback(ch, method, properties, body):
        contact_id = body.decode('utf-8')
        print(f'Received message with contact ID (sms): {contact_id}')

        try:
            contact = Contact.objects.get(id=contact_id)

            if send_sms(contact):
                contact.message_sent = True
                contact.save()
                print(f'The message has been successfully sent to contact: {contact.fullname}')
        except Contact.DoesNotExist:
            print(f'Contact with ID {contact_id} not found')

        ch.basic_ack(delivery_tag=method.delivery_tag)


    channel.basic_consume(queue='sms_queue', on_message_callback=callback)

    print(' [*] Waiting for sms messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)