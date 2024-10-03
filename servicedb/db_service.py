import asyncio
import aiopg
import aio_pika
import psycopg2
import psycopg2.pool
import json

# Пул соединений для PostgreSQL
db_pool = None


async def init_db_pool(minconn, maxconn):
    """Функция инициализации пула соединений."""
    global db_pool
    for _ in range(5):
        try:
            db_pool = psycopg2.pool.SimpleConnectionPool(
                minconn,
                maxconn,
                dbname='mydb',
                user='user',
                password='password',
                host='db'
            )
            print("Пул соединений успешно инициирован.")
            return
        except psycopg2.OperationalError as e:
            print(f"Нет соединения с БД: {e}")
            await asyncio.sleep(5)
    print("Не получилось после всех попыток.")
    raise Exception("Could not connect to the database after several attempts.")


async def connect_to_db():
    """Асинхронная функция получения соединения из пула."""
    if db_pool is None:
        raise Exception("Пул соединений не был инициирован.")
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


async def wait_for_rabbitmq():
    for i in range(5):
        try:
            connection = await aio_pika.connect_robust(
                "amqp://guest:guest@rabbitmq/"
            )
            await connection.close()
            print("RabbitMQ is available")
            return
        except Exception as e:
            print(f"Не удалось подключиться к RabbitMQ: {e}")
            await asyncio.sleep(5)

    raise Exception("RabbitMQ недоступен.")


async def setup_rabbitmq():
    await wait_for_rabbitmq()
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)
        queue = await channel.declare_queue('appeals')
        await queue.consume(message_handler)
        print('Ожидание сообщений. Для выхода нажмите CTRL+C')
        return connection


async def wait_for_db():
    for _ in range(5):
        try:
            conn = await asyncio.wait_for(aiopg.connect(
                dbname='mydb',
                user='user',
                password='password',
                host='db',
                port='5432'
            ), timeout=10)
            await conn.close()
            print("БД готова")
            return
        except Exception as e:
            print(f"Не удалось подключиться к БД: {e}")
            await asyncio.sleep(5)

    raise Exception("PostgreSQL не доступен.")


async def main():
    await wait_for_db()
    await init_db_pool(minconn=1, maxconn=20)
    await wait_for_rabbitmq()
    await setup_rabbitmq()
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
