FROM python:3

LABEL maintainer="aayush"

WORKDIR /app

COPY . /app/

RUN pip install Django
WORKDIR /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "localhost:8000"]