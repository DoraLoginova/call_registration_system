import pika
import psycopg2
import json


def connect_to_db():
    return psycopg2.connect(
        dbname='mydb',
        user='user',
        password='password',
        host='db'
    )

# Функция для вставки данных в таблицу
def insert_appeal(data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO appeals (last_name, first_name, patronymic, phone, message)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                data['last_name'],
                data['first_name'],
                data['patronymic'],
                data['phone'],
                data['message']
            ))
            conn.commit()
    finally:
        conn.close()  # Гарантированно закрываем соединение даже в случае ошибки

# Обратный вызов для обработки сообщений
def callback(ch, method, properties, body):
    data = json.loads(body)
    insert_appeal(data)


def setup_rabbitmq():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='rabbitmq',  # имя сервиса в docker-compose
                credentials=pika.PlainCredentials('guest', 'guest')
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue='appeals')
        return channel
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Ошибка подключения к RabbitMQ: {e}")
        exit(1)




if __name__ == "__main__":
    channel = setup_rabbitmq()
    channel.basic_consume(
        queue='appeals',
        on_message_callback=callback,
        auto_ack=True
    )

    print('Ожидание сообщений. Для выхода нажмите CTRL+C')
    channel.start_consuming()
