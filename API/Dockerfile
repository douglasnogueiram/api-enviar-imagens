FROM python:3.8-slim-buster

# We copy just the requirements.txt first to leverage Docker cache

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

RUN pip install jsonschema
RUN pip install -U flask-cors
RUN pip install confluent-kafka

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]