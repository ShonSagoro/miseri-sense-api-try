from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from utilities import pdf_generator
import json

app = Flask(__name__, static_folder="public", static_url_path="/public", template_folder="view")

CORS(app)

conf = None

with open('./config.json') as file:
    conf = json.load(file)

print(conf)

@app.route('/pdf/all', methods=["GET","POST"])
def get_pdf_quality():
    global conf
    print(f'AAAAAAAAAAAA {conf}')
    quality=pdf_generator.make_petitions(pdf_generator.type.QUALITY.value) 
    light=pdf_generator.make_petitions(pdf_generator.type.LIGHT.value) 
    temperature=pdf_generator.make_petitions(pdf_generator.type.TEMPERATURE.value) 
    humidity=pdf_generator.make_petitions(pdf_generator.type.HUMIDITY.value)

    name={
        'quality': f'{conf["protocol"]}://{conf["host"]}:{conf["port"]}/{quality}',
        'light': f'{conf["protocol"]}://{conf["host"]}:{conf["port"]}/{light}',
        'temperature': f'{conf["protocol"]}://{conf["host"]}:{conf["port"]}/{temperature}',
        'humidity': f'{conf["protocol"]}://{conf["host"]}:{conf["port"]}/{humidity}'
    }

    return jsonify(name)

