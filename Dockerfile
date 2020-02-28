FROM python:3.6-alpine

# DockerHub refused to install Postgresql packages without it:
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY ./www/ /app/
COPY ./requirements.txt /app/requirements.txt
# "-p" - create all chain with parent dirs, if any
RUN mkdir -p /cache
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w 4", "-b 0.0.0.0:18000", "index:app"]
