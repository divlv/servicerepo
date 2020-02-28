FROM python:3.6-alpine

COPY ./www/ /app/
COPY ./requirements.txt /app/requirements.txt
# "-p" - create all chain with parent dirs, if any
RUN mkdir -p /cache
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w 4", "-b 0.0.0.0:18000", "index:app"]
