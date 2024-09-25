FROM postgres:13

WORKDIR /docker-entrypoint-initdb.d

COPY create_table.sql .

RUN chmod 644 create_table.sql
