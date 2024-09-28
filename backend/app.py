import tornado.ioloop
import tornado.web
import pika
import psycopg2
import json


class MainHandler(tornado.web.RequestHandler):

    def options(self):
        print("Получен OPTIONS запрос.")
        self.set_status(204)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS, GET")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.finish()

    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        try:
            data = json.loads(self.request.body)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='rabbitmq',
                    credentials=pika.PlainCredentials('guest', 'guest')
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue='appeals')
            channel.basic_publish(
                exchange='',
                routing_key='appeals',
                body=json.dumps(data)
            )
            connection.close()

            self.set_status(201)
            self.finish("Обращение получено.")
        except json.JSONDecodeError:
            self.set_status(400)
            self.finish("Ошибка декодирования JSON: неверный формат.")
        except pika.exceptions.AMQPConnectionError:
            self.set_status(503)
            self.finish("Ошибка подключения к RabbitMQ.")
        except Exception as e:
            self.set_status(500)
            self.finish(f"Ошибка: {str(e)}")

    def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        try:
            connection = psycopg2.connect(
                dbname='mydb',
                user='user',
                password='password',
                host='db'
            )
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM appeals;")
            appeals = cursor.fetchall()
            appeals_list = []
            for appeal in appeals:
                appeals_list.append({
                    'id': appeal[0],
                    'last_name': appeal[1],
                    'first_name': appeal[2],
                    'patronymic': appeal[3],
                    'phone': appeal[4],
                    'message': appeal[5],
                })
            connection.close()
            self.set_status(200)
            self.finish(json.dumps(appeals_list, ensure_ascii=False))
        except Exception as e:
            self.set_status(500)
            self.finish(f"Ошибка: {str(e)}")


def make_app():
    return tornado.web.Application([
        (r"/api/appeal", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
