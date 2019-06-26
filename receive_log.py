import pika
import sys
from functions import create_or_open_txt, send_email , types

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

result_queue = channel.queue_declare(queue='', exclusive=True)

queue_name = result_queue.method.queue

channel.queue_bind(exchange='logs',queue=result_queue.method.queue)

def callback(ch, method, propieties, body):
    body_inf = eval(body.decode())
    type_message = "".join(sys.argv[1:]).lower()
    if type_message=='debug':
        create_or_open_txt(body_inf['type_message'],body_inf['message'])
        send_email(body_inf['type_message'],body_inf['message'])

    elif type_message == 'info' and body_inf['type_message'] in ['debug', 'info','warning']:
        create_or_open_txt(body_inf['type_message'], body_inf['message'])
        send_email(body_inf['type_message'], body_inf['message'])

    elif type_message == 'warning' and body_inf['type_message'] in ['warning', 'error']:
        create_or_open_txt(body_inf['type_message'], body_inf['message'])
        send_email(body_inf['type_message'], body_inf['message'])

    elif type_message == 'error' and body_inf['type_message'] in ['error']:
        create_or_open_txt(body_inf['type_message'], body_inf['message'])
        send_email(body_inf['type_message'], body_inf['message'])

    print(f'[X] received {body}')


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
type_message="".join(sys.argv[1:]).lower()
print(f"Waiting for a {type_message}")
channel.start_consuming()
