#!/bin/bash

echo "Проверка состояния RabbitMQ..."
rabbitmqctl status

echo "Включение плагина rabbitmq_management..."
rabbitmq-plugins enable rabbitmq_management


echo "Список включенных плагинов:"
rabbitmq-plugins list

echo "Плагин rabbitmq_management включен."
