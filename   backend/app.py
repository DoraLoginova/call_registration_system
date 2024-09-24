import tornado.ioloop
import tornado.web
import pika
import json


class MainHandler(tornado.web.RequestHandler): 
    def post(self):
        data = json.loads(self.request.body)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('rabbitmq')
        )                        # создает новое соединение с сервером RabbitMQ
        channel = connection.channel()  # oткрывает канал для взаимодействия с RabbitMQ
        channel.queue_declare(queue='appeals')  # Объявляет очередь с именем appeals
        channel.basic_publish(
            exchange='',
            routing_key='appeals',
            body=json.dumps(data)
        )                       # Отправляет сообщение в очередь appeals
        connection.close()     # Закрывает соединение с RabbitMQ
        self.set_status(201)  # Устанавливает статус ответа HTTP на 201 Created
        self.finish("Обращение получено.")

#  Маршрутизация в Tornado настраивается с помощью класса Application,
# который связывает URL-шаблоны с соответствующими обработчиками


def make_app():
    return tornado.web.Application([  
        (r"/api/appeal", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
