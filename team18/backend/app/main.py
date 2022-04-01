import os

import matplotlib
matplotlib.use('Agg')
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=["POST"])
def foo():
    req = request.get_json()

    with open('app/code.py', 'w') as f:
        f.write(req['code'])

    from .code import generate_circuit
    from .compile_and_verify import compile_and_verify

    circ = generate_circuit()

    # compile and check the equivalence
    circ_comp, equivalent = compile_and_verify(circ)
    print('Compiled circuit is equivalent to original circuit:', equivalent)

    circ.draw(fold=-1, filename="images/original_pic.png", output='mpl')
    circ_comp.draw(fold=-1, filename="images/compiled_pic.png", output='mpl')

    os.remove('app/code.py')

    response_body = {
        "dlgCircSrc": "localhost:5000/images/original_pic.png",
        "bsgCircSrc": "localhost:5000/images/compiled_pic.png",
        "equivalent": equivalent
    }

    response = jsonify(response_body)

    return response
