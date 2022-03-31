from flask import Flask, make_response
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=["POST"])
def foo():
    req = request.get_json()

    f = open('code.py', 'w')

    f.write(req['code'])

    # subprocess.run(["code.py"])

    response_body = {
        "dlgCircSrc": "",
        "bsgCircSrc": "",
        "equivalent": 0
    }

    response = jsonify(response_body)

    return response
