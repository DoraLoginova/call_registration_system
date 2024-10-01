from locust import HttpUser, TaskSet, task, between

class UserBehavior(TaskSet):

    @task(1)  # вес задачи
    def create_appeal(self):
        # Данные для обращения
        appeal_data = {
            "last_name": "Логинова",
            "first_name": "Дора",
            "patronymic": "Константиновна",
            "phone": "1234567890",
            "message": "Тестовое обращение"
        }
        self.client.post("/api/appeal", json=appeal_data)

    @task(2)  # вес задачи
    def get_appeals(self):
        self.client.get("/api/appeal")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(0.5, 1.5)  # время ожидания между запросами
