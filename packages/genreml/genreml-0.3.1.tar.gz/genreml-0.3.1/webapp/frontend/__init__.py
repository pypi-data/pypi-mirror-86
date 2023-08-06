import json

from flask_cors import CORS
from flask import Flask

app = Flask(__name__)
CORS(app)

with open('config.json') as config_file:
    config = json.load(config_file)

app.config["FILE_UPLOAD_LOCATION"] = config.get("FILE_UPLOAD_LOCATION")

