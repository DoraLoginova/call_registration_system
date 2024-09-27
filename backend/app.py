import tornado.ioloop
import tornado.web
import pika
import json

class MainHandler(tornado.web.RequestHandler):

    def options(self):
        self.set_status(204)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.finish()

    def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        # Проверяем, есть ли тело запроса
        try:
            if not self.request.body:
                raise ValueError("Пустое тело запроса")
            data = json.loads(self.request.body)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='rabbitmq',  # имя сервиса в docker-compose
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
