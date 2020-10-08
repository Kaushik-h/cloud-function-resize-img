import os
import requests
from PIL import Image
from google.cloud import storage
from google.cloud import firestore
from os import path

if os.path.exists("/tmp/sample.png"):
  os.remove("/tmp/sample.png")
if os.path.exists("/tmp/resize.png"):
  os.remove("/tmp/resize.png")

def hello_gcs(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    url='https://storage.googleapis.com/favicon/'+event['name']
    response = requests.get(url)
    file=open("/tmp/sample.png", "wb")
    file.write(response.content)
    file.close()

    im = Image.open("/tmp/sample.png")
    image = im.resize((60,60), resample=Image.HAMMING)
    image.save("/tmp/resize.png")
    image=image.close()

    storage_client = storage.Client()
    bucket = storage_client.bucket('resize-favicon')
    blob = bucket.blob(event['name'])
    blob.upload_from_filename("/tmp/resize.png")

    db=firestore.Client()
    dom=db.collection('domain').document(event['name'])
    imgurl='https://storage.googleapis.com/resize-favicon/'+event['name']
    dom.update({"imageurl":imgurl})

