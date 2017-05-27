#!flask/bin/python
import sys
import logging
import os
import base64
import uuid
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/healthz', methods=['GET'])
def healthz():
  response = {
    "status": "ok",
    "hostname": "ignored me"#os.environ["HOSTNAME"]
  }

  return jsonify(response)

@app.route('/question', methods=['POST'])
def question():
  """equest.get_json()
  Recibe una pregunta
  crea un nuevo elemento en el API firebase
  utiliza el resultado anterior y envia al API language
  """
  response = {}
  try:
      json_data = request.get_json()
      response['status'] = 'succesful'
      response['message'] = 'The file is writed to filesystem'
  except Exception as e:
      response['status'] = 'succesful'
      response['message'] = 'The file is writed to filesystem'

  return jsonify(json_data)

@app.route('/upload', methods=['POST'])
def upload():
  """json_datae del archivo anterior para subir al firebase
  utiliza el resultado anterio y lo envia al API vision
  debe retornar un json con el contenido del firebase
  """
  response = {}
  try:
      json_data = request.get_json()
      filename = '{}.jpg'.format(str(uuid.uuid4()))
      image = base64.b64decode(json_data['file'])
      with open(os.path.join(os.environ['DOWNLOADS_LOCATION'], filename), 'wb') as f:
         f.write(image)
      response['status'] = 'succesful'
      response['message'] = 'The file is writed to filesystem'
  except Exception as e:
      response['status'] = 'failed'
      response['message'] = e

  return jsonify(response)

@app.route('/message', methods=['POST'])
def message():
  """
  Recibe un message
  crea un nuevo elemento en el API firebase
  utiliza el resultado anterior y envia al API language
  """
  params = request.get_json()
  print("parametros: ")
  print(params)
  hostinfo = {
    'sisname': os.uname()[0],
    'dirMAC': os.uname()[1],
    'release': os.uname()[2],
    'version': os.uname()[3],
    'maquina': os.uname()[4]
  }
  params['server'] = hostinfo
  params['remote_addr'] = request.remote_addr
  return jsonify(params)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port="8080")
