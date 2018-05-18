from flask import Flask, Response, request
import json
import sys
sys.path.append('..')
import marker

MARKER_NAME = 'em-text-similarities'
SETUP_URL = '/%s/setup' % MARKER_NAME
MARKUP_URL = '/%s/markup' % MARKER_NAME

application = Flask(__name__)

@application.route(SETUP_URL, methods=['GET'])
def handle_setup_request():
    data = marker.get_setup()
    return create_response(data)

@application.route(MARKUP_URL, methods=['POST'])
def handle_markup_request(): 
    data = marker.get_markup(request.json)
    return create_response(data)

def create_response(response_data):
    resp = Response() 
    resp.data = json.dumps(response_data)
    resp.headers['Content-Type'] = 'application/json'
    return resp

if __name__ == '__main__':
	application.run(host='127.0.0.1', port=8080, debug=True)