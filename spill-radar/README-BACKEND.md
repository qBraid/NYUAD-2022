# Running the python backend

```
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip install -U pip setuptools wheel
(venv) $ pip install qiskit-optimization[cplex] qiskit
(venv) $ python3 qubo.py -h
usage: qubo.py [-h] [--quantum] size x y

positional arguments:
  size        Size of the oil spill
  x           x coordinates of the oil spill
  y           y coordinates of the oil spill

optional arguments:
  -h, --help  show this help message and exit
  --quantum   use quantum to solve
(venv) $ python3 qubo.py 20 0 5
{
    "status": "SUCCESS",
    "ships": [
        "ship1",
        "ship2",
        "ship3"
    ]
}
```