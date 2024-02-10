FROM python:3

LABEL maintainer="aayush"

WORKDIR /Users/Aayus/project_portfolio

COPY project_portfolio /portfolio/

RUN pip install Django
WORKDIR /portfolio

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "localhost:8000"]