import os
import asyncio
import tornado.ioloop
import tornado.web
import json
from servicedb.db_service import (
    init_db_pool,
    insert_appeal,
    get_appeals,
    setup_rabbitmq,
    wait_for_db,
)


class MainHandler(tornado.web.RequestHandler):
    async def options(self):
        self.set_status(204)
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS, GET")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.finish()

    async def post(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        try:
            data = json.loads(self.request.body)
            await insert_appeal(data)
            self.set_status(201)
            self.finish("Обращение получено.")
        except json.JSONDecodeError:
            self.set_status(400)
            self.finish("Ошибка декодирования JSON: неверный формат.")
        except Exception as e:
            self.set_status(500)
            self.finish(f"Ошибка: {str(e)}")

    async def get(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        try:
            appeals_list = await get_appeals()
            self.set_status(200)
            self.finish(json.dumps(appeals_list, ensure_ascii=False))
        except Exception as e:
            self.set_status(500)
            self.finish(f"Ошибка: {str(e)}")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        print("IndexHandler был вызван!")
        self.set_header("Content-Type", "text/html")
        self.render("index.html")


def make_app():
    # frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))
    # static_path = os.path.join(os.path.dirname(__file__), '.')
    return tornado.web.Application([
        (r"/api/", MainHandler),
        (r"/", IndexHandler),
    ])
    # template_path=frontend_path
    # static_path=static_path


async def init_app():
    await asyncio.gather(
        wait_for_db(),
        init_db_pool(minconn=5, maxconn=100),
        setup_rabbitmq(),
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().add_callback(init_app)
    tornado.ioloop.IOLoop.current().start()
