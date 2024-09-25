# Используем образ RabbitMQ с плагином управления
FROM astralinux/rabbitmq:latest

# Устанавливаем рабочую директорию
WORKDIR /etc/rabbitmq

# Копируем конфигурационный файл rabbitmq.conf в контейнер
COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

# Копируем скрипт для включения плагинов
COPY enable_plugins.sh /usr/local/bin/enable_plugins.sh

# Делаем скрипт исполняемым
RUN chmod +x /usr/local/bin/enable_plugins.sh

# Запускаем RabbitMQ и включаем плагин
CMD ["sh", "-c", "/usr/local/bin/enable_plugins.sh && rabbitmq-server"]
