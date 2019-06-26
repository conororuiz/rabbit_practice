import pika
import random
from time import sleep

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='test')


def callback(ch, method, properties, body):
    num = random.randint(1, 10)
    print(f'[X] recived {body}', num, 'seg')
    sleep(num)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='test', on_message_callback=callback)

print('Waiting for a message...')
channel.start_consuming()
