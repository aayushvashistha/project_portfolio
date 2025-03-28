FROM python:3

LABEL maintainer="aayush"

# RUN apt-get update && apt-get install -y python3-distutils

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt || True
RUN pip install Django

WORKDIR /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "localhost:8000"]