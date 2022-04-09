# Running the python backend

In the backend folder:
```
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip install -U pip setuptools wheel
(venv) $ pip install qiskit-optimization qiskit
(venv) $ flask run
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
[...]
```
Then accessing `http://127.0.0.1:5000/qubo?size=<SIZE>&x=<X>&y=<Y>`  (e.g. `http://127.0.0.1:5000/qubo?size=20&x=0&y=5`) will return the json response.

```
{
    "status": "SUCCESS",
    "ships": [
        "ship1",
        "ship2",
        "ship3"
    ]
}
```