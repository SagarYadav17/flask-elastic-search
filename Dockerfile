FROM python:3.10-alpine

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8080

CMD ["python3", "/app/app.py"]
