#base64 $IMAGE_PATL:

import json

f = open('image.txt')
f_json = open('upload.json', 'w')
upload = {}
upload['file'] =  f.read()
f_json.write(json.dumps(upload))
f_json.close()


