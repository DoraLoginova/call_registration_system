import asyncio
import aiopg
import aio_pika
import json

db_pool = None


async def init_db_pool(minconn, maxconn):
    """Инициализация пула соединений."""
    global db_pool
    for _ in range(5):
        try:
            db_pool = await aiopg.create_pool(
                dsn='dbname=mydb user=user password=password host=db',
                minsize=minconn,
                maxsize=maxconn
            )
            print("Пул соединений успешно инициирован.")
            return
        except Exception as e:
            print(f"Нет соединения с БД: {e}")
            await asyncio.sleep(5)
    raise Exception("Не удалось подключиться к базе данных.")


async def connect_to_db():
    """Получение соединения из пула."""
    if db_pool is None:
        raise Exception("Пул соединений не был инициирован.")
    return await db_pool.acquire()


async def insert_appeal(data):
    """Вставка обращения в базу данных."""
    conn = await connect_to_db()  # Получаем соединение
    try:
        async with conn.cursor() as cur:
            await cur.execute("""
                INSERT INTO appeals (last_name, first_name, patronymic, phone, message)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                data['last_name'],
                data['first_name'],
                data['patronymic'],
                data['phone'],
                data['message'],
            ))
    finally:
        db_pool.release(conn)  # Безопасный возврат соединения в пул


async def get_appeals():
    """Получение всех обращений из базы данных."""
    conn = await connect_to_db()
    try:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM appeals;")
            records = await cur.fetchall()
            return [{
                'id': record[0],
                'last_name': record[1],
                'first_name': record[2],
                'patronymic': record[3],
                'phone': record[4],
                'message': record[5]
            } for record in records]
    finally:
        db_pool.release(conn)


async def message_handler(message: aio_pika.IncomingMessage):
    """Обработка входящих сообщений из очереди RabbitMQ."""
    async with message.process():
        data = json.loads(message.body)
        await insert_appeal(data)


async def setup_rabbitmq():
    for _ in range(5):  # Попробуйте несколько раз
        try:
            connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
            print("Успешное подключение к RabbitMQ!")
            async with connection:
                channel = await connection.channel()
                await channel.set_qos(prefetch_count=10)
                queue = await channel.declare_queue('appeals')
                await queue.consume(message_handler)
                print('Ожидание сообщений. Для выхода нажмите CTRL+C')
            return  # Успешное подключение
        except Exception as e:
            print(f"Ошибка подключения к RabbitMQ: {e}")
            await asyncio.sleep(2)  # Ждем перед новой попыткой



async def wait_for_db():
    for _ in range(5):
        try:
            async with aiopg.connect(
                dbname='mydb',
                user='user',
                password='password',
                host='db',
                port='5432'
            ):
                print("БД готова")
                return
        except Exception as e:
            print(f"Не удалось подключиться к БД: {e}")
            await asyncio.sleep(5)
    raise Exception("PostgreSQL не доступен.")


async def main():
    await asyncio.gather(
        wait_for_db(),
        init_db_pool(minconn=5, maxconn=100),
        setup_rabbitmq(),
    )
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
