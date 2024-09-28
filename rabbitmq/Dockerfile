FROM rabbitmq:3.13-management

COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf

COPY enable_plugins.sh /docker-entrypoint-initdb.d/enable_plugins.sh

RUN chmod +x /docker-entrypoint-initdb.d/enable_plugins.sh

ENV RABBITMQ_DEFAULT_USER=guest
ENV RABBITMQ_DEFAULT_PASS=guest
