import asyncio
import aio_pika
import psycopg2
import psycopg2.pool
import json

from .constants import MIN_CONNECT, MAX_CONNECT

# Пул соединений для PostgreSQL
db_pool = None


def init_db_pool(minconn, maxconn):
    """Функция инициализации пула соединений."""
    global db_pool
    db_pool = psycopg2.pool.SimpleConnectionPool(
        minconn,
        maxconn,
        dbname='mydb',
        user='user',
        password='password',
        host='db'
    )


async def connect_to_db():
    """Асинхронная функция получения соединения из пула."""
    return db_pool.getconn()


async def insert_appeal(data):
    """Асинхронная функция вставки обращения."""
    conn = await connect_to_db()
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


async def get_appeals():
    """Асинхронная функция получения всех обращений."""
    conn = await connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM appeals;")
            records = cur.fetchall()
            appeals = []
            for record in records:
                appeals.append({
                    'id': record[0],
                    'last_name': record[1],
                    'first_name': record[2],
                    'patronymic': record[3],
                    'phone': record[4],
                    'message': record[5]
                })
            return appeals
    finally:
        db_pool.putconn(conn)


async def message_handler(message: aio_pika.IncomingMessage):
    """Функция асинхронной обработки входящих сообщений из очереди RabbitMQ"""
    async with message.process():
        data = json.loads(message.body)
        await insert_appeal(data)


async def setup_rabbitmq():
    """Асинхрон. подключ. к серверу RabbitMQ с данными (user/password/host)."""
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@rabbitmq/"
    )
    async with connection:
        channel = await connection.channel()
        await channel.set_queue('appeals')
        await channel.consume(message_handler, queue='appeals')
        print('Ожидание сообщений. Для выхода нажмите CTRL+C')
        return connection


async def main():
    init_db_pool(minconn=MIN_CONNECT, maxconn=MAX_CONNECT)
    await setup_rabbitmq()

if __name__ == "__main__":
    asyncio.run(main())
