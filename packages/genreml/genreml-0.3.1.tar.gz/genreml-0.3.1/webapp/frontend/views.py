import os
import sys

from flask import request, render_template
from werkzeug.utils import secure_filename

from frontend import app
from frontend.processing import feature_extraction, genre_prediction


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """ Route for uploading audio files to the site """
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(filepath)
        features, visual_features = feature_extraction.process_audio_file(filepath)
        print(features)
        return render_template('index.html')


@app.route('/')
def index():
    """ Server route for the app's landing page """
    return render_template('index.html')


if __name__ == "__main__":
    environment = "production"
    if len(sys.argv) > 1:
        environment = sys.argv[1]
    if environment == "production":
        from gevent.pywsgi import WSGIServer
        app.debug = True
        http_server = WSGIServer(('', 8000), app)
        http_server.serve_forever()
    elif environment == "development":
        app.run(debug=True, host='127.0.0.1', port=8000)
