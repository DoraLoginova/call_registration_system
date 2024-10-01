import time
import pika
import psycopg2
import psycopg2.pool
import json

# Пул соединений для PostgreSQL
db_pool = None


def init_db_pool(minconn, maxconn):
    global db_pool
    db_pool = psycopg2.pool.SimpleConnectionPool(
        minconn,
        maxconn,
        dbname='mydb',
        user='user',
        password='password',
        host='db'
    )


def connect_to_db():
    return db_pool.getconn()


def insert_appeal(data):
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO appeals (last_name, first_name,
                patronymic, phone, message)
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
        db_pool.putconn(conn)


def callback(ch, method, properties, body):
    data = json.loads(body)
    insert_appeal(data)


def setup_rabbitmq():
    for _ in range(5):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='rabbitmq',
                    credentials=pika.PlainCredentials('guest', 'guest')
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue='appeals')
            return channel
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Ошибка подключения к RabbitMQ: {e}")
            time.sleep(2)

    print("Не удалось подключиться к RabbitMQ после нескольких попыток.")
    exit(1)


if __name__ == "__main__":
    init_db_pool(minconn=1, maxconn=30)
    channel = setup_rabbitmq()
    channel.basic_consume(
        queue='appeals',
        on_message_callback=callback,
        auto_ack=True
    )

    print('Ожидание сообщений. Для выхода нажмите CTRL+C')
    channel.start_consuming()
