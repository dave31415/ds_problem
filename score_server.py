from flask import Flask, Response, request, jsonify
from score_server_validators import is_request_valid
from validate import validate_ledger

PORT = 5005

app = Flask(__name__)


@app.route('/ping', methods=['POST', 'GET'])
def ping():
    return Response("I'm alive", 200)


@app.route('/', methods=['POST', 'GET'])
def index():
    valid, reason = is_request_valid(request)

    if not valid:
        return reason

    request_data = request.get_json()

    try:
        return_data = validate_ledger(request_data)
        return jsonify(**return_data)
    except:
        # somehow failed, send a 500 error code
        return Response("Error: forecast calculation failed", 500)


if __name__ == '__main__':
    # debug=True allows the server to listen for changes in the code and
    # updates in realtime, use only in development
    app.run(debug=True, host='0.0.0.0', port=PORT)
