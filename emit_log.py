import pika
import sys
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = " ".join(sys.argv[2:])
type_message = sys.argv[1].lower()

body = {
    'message':message,
    'type_message':type_message
}

channel.basic_publish(exchange='logs', routing_key='', body=json.dumps(body))

print('[X] sent')

connection.close()
