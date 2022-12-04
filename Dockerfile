FROM python:3.10-slim

ENV APP_HOME /code
ENV PYTHONPATH $APP_HOME
ENV PYTHONUNBUFFERED 1
ENV ENV_CONFIG 1
WORKDIR $APP_HOME

COPY ./requirements.txt $APP_HOME/requirements.txt

RUN apt update && apt upgrade -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . $APP_HOME

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
