"""
A sample Hello World server.
"""
import os

from flask import Flask, render_template,send_from_directory
from flask_cors import CORS

# pylint: disable=C0103
app = Flask(__name__)
CORS(app) ## To allow direct AJAX calls

DOWNLOAD_DIRECTORY = "output"

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)


@app.route('/wordcloud', methods=['GET', 'POST'])
def getWordcloud():
    print('get wordcloud' )
    try:
        return send_from_directory(DOWNLOAD_DIRECTORY,'VTT wordcloud.png', as_attachment=True)
    except FileNotFoundError:
        os.abort(404)

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
