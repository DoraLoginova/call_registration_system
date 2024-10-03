FROM python:latest

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ../servicedb /app/servicedb 

COPY . .

EXPOSE 8000

CMD ["python", "-m", "apps"]

