import os

import matplotlib
matplotlib.use('Agg')
from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=["POST"])
def foo():
    req = request.get_json()

    with open('app/code.py', 'w') as f:
        f.write(req['code'])
        f.close()

    introduce_error = req['introduceError']

    from .code import generate_circuit
    from .compile_and_verify import compile_and_verify
    circ = generate_circuit()

    # compile and check the equivalence
    circ_comp, equivalent = compile_and_verify(circ, introduce_error=introduce_error)
    print('Compiled circuit is equivalent to original circuit:', equivalent)

    now = datetime.now()

    dt_string = now.strftime("%H_%M_%S")

    circ.draw(fold=-1, filename="../frontend/public/original_pic_" + dt_string + ".png", output='mpl')
    circ_comp.draw(fold=-1, filename="../frontend/public/compiled_pic_" + dt_string + ".png", output='mpl')

    os.remove('app/code.py')

    response_body = {
        "dlgCircSrc": "original_pic_" + dt_string + ".png",
        "bsgCircSrc": "compiled_pic_" + dt_string + ".png",
        "equivalent": equivalent
    }

    response = jsonify(response_body)

    return response
