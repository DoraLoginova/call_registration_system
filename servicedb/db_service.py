import pika
import psycopg2
import json


def callback(ch, method, properties, body):
    data = json.loads(body)
    conn = psycopg2.connect(
      "dbname='mydb' user='user' password='password' host='db'"
    )
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO appeals (last_name, first_name, patronymic, phone, message)
        VALUES (%s, %s, %s, %s, %s)""",
        (data['last_name'], data['first_name'], data['patronymic'], data['phone'], data['message']))
    conn.commit()
    cur.close()
    conn.close()


connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='appeals')
channel.basic_consume(
  queue='appeals',
  on_message_callback=callback,
  auto_ack=True
)

print('Ожидание сообщений. Для выхода нажмите CTRL+C')
channel.start_consuming()
