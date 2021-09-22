import flask
from flask import request, jsonify
from flask import Response

import os
import json
import jsonschema
from jsonschema import validate
from flask_cors import CORS
from confluent_kafka import Producer
import socket
import uuid
from datetime import datetime

import base64



TOPIC_NAME = "images"


conf = {'bootstrap.servers': 'localhost:9092',
        'client.id': socket.gethostname()}

producer = Producer(conf)


checkImageSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "image": {"type": "string"}
    },
}


#validate if Json from request is valid
def validateJson(jsonData):
    try:
        validate(instance=jsonData, schema=checkImageSchema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True



app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello world'


@app.route('/api/v1/images', methods=['POST'])
def api_all():
    input_json = request.get_json(force=True)

    #validate json from request
    isValid = validateJson(input_json)
    #isValid = True
    if isValid:
        print("Given JSON data is valid")
        uuidOne = uuid.uuid1()
        
        json_payload = json.dumps(
                                    {
                                        'id' : str(uuidOne),
                                        'name': input_json['name'],
                                        'image' : input_json['image'],
                                        'timestamp' : str(datetime.now())

                                    }
                                )
        json_payload = str.encode(json_payload)
		
        # push data into images topic
        app.logger.info('%s Iniciar envio da mensagem', conf['bootstrap.servers'])
        producer.produce(topic=TOPIC_NAME, key=str(uuidOne), value=json_payload)
        producer.flush()
        print("Sent to consumer")
        
        return jsonify({
        "id": uuidOne,
        "message": "Message sent ok", 
        "status": "Pass"})

    else:
        print("Given JSON data is not valid")
        return Response(
        '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">'
        + '<title>400 Bad Request</title><h1>Bad Request</h1>'
        + '<p>Failed to decode JSON object:' + str(input_json) + '</p>',
        status=400,
    )

app.run(host='0.0.0.0')
