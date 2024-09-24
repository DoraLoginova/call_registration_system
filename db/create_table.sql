CREATE TABLE appeals (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(100),
    first_name VARCHAR(100),
    patronymic VARCHAR(100),
    phone VARCHAR(15),
    message TEXT
);

# Эта команда создаёт новую таблицу в базе данных с именем appeals
# SERIAL означает, что PostgreSQL автоматически создаст последовательность 
# и сгенерирует уникальные значения для этого поля