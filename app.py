#!flask/bin/python
import sys
import logging
import os
import base64
import uuid
import requests
from flask import Flask, render_template, request, jsonify
from helper import watermark
app = Flask(__name__)

@app.route('/', methods=['GET'])
def root_path():
  response = {
    "status": "ok",
    "info": "root_path"
  }
  return jsonify(response)

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
  question_payload = {}
  try:
      json_data = request.get_json()
      question_payload['path'] = '/question'
      question_payload['method'] = 'push'
      question_payload['data'] = json_data
      firebase_url = "%s/publish" % os.environ['FIREBASE']
      post_question_request = requests.post(firebase_url, json = question_payload)
      if post_question_request.status_code == '201':
        post_request_payload = post_question_request.json()
        language_question_url = "%s/question" % os.environ['LANGUAGE']
        post_language_request = requests.post(language_question_url, json = post_request_payload)
        if post_language_request.status_code == '200':
           response = post_language_request

  except Exception as e:
      print('Error: {}'.format(e))

  return jsonify(response)

@app.route('/upload', methods=['POST'])
def upload():
  """json_datae del archivo anterior para subir al firebase
  utiliza el resultado anterio y lo envia al API vision
  debe retornar un json con el contenido del firebase
  """
  firebase_publish_url = "%s/publish" % os.environ['FIREBASE']
  firebase_upload_url = "%s/upload" % os.environ['FIREBASE']
  vision_url = "%s/detect" % os.environ['VISION']
  response = {}
  try:
      json_data = request.get_json()
      fileUUID = str(uuid.uuid4())
      filename = '{}.jpg'.format(fileUUID)
      filename_watermark = '{}_watermark.jpg'.format(fileUUID)
      filepath = os.path.join(os.environ['DOWNLOADS_LOCATION'], filename)
      filepath_watermark = os.path.join(os.environ['DOWNLOADS_LOCATION'], filename_watermark)
      image = base64.b64decode(json_data['file'])
      image_watermark = watermark(image, 'GDG-CDE-HACKATON-DATAPAR', font_path='OpenSans-Bold.ttf', opacity=0.4, font_scale=0.1, color=(255,255,255))
      image_watermark.save('{0}/{1}'.format(filepath_watermark, filename_watermark))
      with open(filepath, 'wb') as f:
         f.write(image)

      # Upload image to storage and push to firebase /images/
      upload_payload = {
        'filename': filename_watermark
      }
      firebase_up_r = requests.post(firebase_upload_url, json = upload_payload)
      response['firebase_up_r'] = firebase_up_r.json()

      # Get Labels
      vision_payload = {
        'original_file': filename
      }
      vision_r = requests.post(vision_url, json = vision_payload)
      response['vision_r'] = vision_r.json()

      # Update labels on firebase /images/{key}
      image_path = "/images/%s" % response['firebase_p_r']["key"]
      firebase_payload = {
        'path': image_path,
        'method': 'update',
        'data': response['vision_r']
      }
      firebase_pub_r = requests.post(firebase_publish_url, json = firebase_payload)
      response['firebase_pub_r'] = firebase_pub_r.json()

  except Exception as e:
      response['error'] = 'Error: {}'.format(e)
      print('Error: {}'.format(e))

  return jsonify(response)

@app.route('/message', methods=['POST'])
def message():
  """
  Recibe un message
  crea un nuevo elemento en el API firebase
  utiliza el resultado anterior y envia al API language
  """
  response = {}
  message_payload = {}
  try:
      json_data = request.get_json()
      message_payload['path'] = '/message'
      message_payload['method'] = 'push'
      message_payload['data'] = json_data
      firebase_url = "%s/publish" % os.environ['FIREBASE']
      post_message_request = requests.post(firebase_url, json = message_payload)
      if post_message_request.status_code == '201':
        post_request_payload = post_message_request.json()
        language_message_url = "%s/message" % os.environ['LANGUAGE']
        post_language_request = requests.post(os.path.join(language_message_url, 'message'), json = post_request_payload)
        if post_language_request.status_code == '200':
          response = post_language_request

  except Exception as e:
      print('Error: {}'.format(e))

  return jsonify(response)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port="8080")
