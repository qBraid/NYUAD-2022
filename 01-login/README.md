# MediQal (Team22)

Our solution applies uses quantum annealing to solve Traveling Salesperson Problems to efficiently route mobile healthcare vehicles. We utilize both classical and quantum solvers for this task. Our quantum solutions are obtained by submitting QUBO problems to the DWave quantum annealers via Amazon Braket.


## Team Members
![Team Photo](./../photo/team22.JPG)

## Mentors
Alexandar Degner,  Media University of Applied Sciences Munich, Germany

Pawel Gora , Quantum AI Foundation, Poland

Mohammad Aamir Sohail , University of Michigan, USA
## Hackers
Chaimae Abouzahir, New York University Abu Dhabi, UAE

Fatima Alzahra Maaroouf, Lebanese American University, Lebanon

Hamza Boudouche, Mohammed 5 University, Morocco

Malak Mansour, New York University Abu Dhabi, UAE

Mariam Alsafi, Khalifa University, UAE

Sashank Neupane, New York University Abu Dhabi, UAE

Tasnim Ahmed, New York University Abu Dhabi, UAE

Teague Tomesh, Princeton University, USA

Tiemar Semere Berhe, Khalifa University, UAE

Yaphet Elias Weldegebriel, Khalifa University, UAE

Ziad Mohamed Hassan, New York University Abu Dhabi, UAE



# Getting Started

Clone this repository: https://github.com/hamza-boudouche/NYUAD-2022

Install all the requirements for quantum algorithm:

`pip install -r requirements.txt`

Go to NYUAD-2022/team22 folder

`cd NYUAD-2022/team22`

Install nodejs

Install all the requirements with

`npm install`

Run it on your machine

`npm start`

After starting the website on a localhost server, you can find a website where you can interactively call for mediQal request, and a new node in your location will be created and the path will be adapted in real time with quantum annealing.


## Explanation of Quantum Algorithm

The code for constructing the problem QUBO and finding a solution via classical or quantum annealing is contained in `vrp_qubo.py`. All that is needed as input is an `edge_list` which is passed into the `wrapper()` function.

As an example, a simple input graph may be represented by the edge list:

```python
edge_list = [(0,1,{'weight':4.7}), (1,2,{'weight':10.9}), ...]
```

Calling this function will 
1. Construct the problem QUBO
2. Find a solution via classical or quantum annealing
3. Return the shortest found path and the cost of traversing that path:

```python
[2,1,5,2,...], 32
```
are the order of coordinates and the total cost of the path, which will be the output of the `wrapper()` function.

## Resources
Our QUBO formulation of the problem was adapted from:
> Borowski, M. et al. (2020). [New Hybrid Quantum Annealing Algorithms for Solving Vehicle Routing Problem](https://link.springer.com/chapter/10.1007/978-3-030-50433-5_42#citeas). In: Computational Science – ICCS 2020. ICCS 2020. Lecture Notes in Computer Science, vol 12142. Springer, Cham. https://doi.org/10.1007/978-3-030-50433-5_42

We utilized the following APIs:
- [OpenStreetMap](https://www.openstreetmap.org/copyright): OpenStreetMap® is open data, licensed under the Open Data Commons Open Database License (ODbL) by the OpenStreetMap Foundation (OSMF).
- [Leaflet](https://leafletjs.com)
- [Auth0](https://auth0.com)
