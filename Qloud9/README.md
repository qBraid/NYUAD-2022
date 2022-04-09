# NYUAD Hackathon for Social Good in the Arab World: Focusing on Quantum Computing (QC)

https://nyuad.nyu.edu/en/events/2022/march/nyuad-hackathon-event.html

March 30 - April 1, 2022
## Qloud9
## About our project
28% of the world’s produced food ends up in a trash bin.
Many organizations aim to collect usable food that would have otherwise gone to waste to feed people in need. Currently, food collection routes are not currently optimized and result in inefficient resource management. <br>
Our response: a Quantum solution for optimizing logistic allocations.
## How to run the code
Run the flask server using:
```
python app.py
```
Send a POST request to `localhost:5000/run` in the following json format:
```json
{
    "location": [
        {
            "lat": 24.50836693075162,
            "lng": 54.40520005022369
        },
        {
            "lat": 24.462770104509687,
            "lng": 54.38993715541294
        },
        {
            "lat": 24.494844691128918,
            "lng": 54.369475192138644
        },
        {
            "lat": 24.48727875202071,
            "lng": 54.3804539106812
        },
        {
            "lat": 24.466642137604556,
            "lng": 54.32795364405558
        }
    ]
}
```
The output will be in the following format:
```json
{
    "Truck0": [
        {
            "lat": 24.50836693075162,
            "lng": 54.40520005022369
        },
        {
            "lat": 24.494844691128918,
            "lng": 54.369475192138644
        },
        {
            "lat": 24.48727875202071,
            "lng": 54.3804539106812
        },
        {
            "lat": 24.50836693075162,
            "lng": 54.40520005022369
        }
    ],
    "Truck1": [
        {
            "lat": 24.50836693075162,
            "lng": 54.40520005022369
        },
        {
            "lat": 24.462770104509687,
            "lng": 54.38993715541294
        },
        {
            "lat": 24.466642137604556,
            "lng": 54.32795364405558
        },
        {
            "lat": 24.50836693075162,
            "lng": 54.40520005022369
        }
    ]
}
```
## tech used
Quantum: <br>
* QUBO
* D-wave
Back-end: <br>
* Flask
* Google API
* Python
Front-end: <br>
* Web app employing
*  HTML, CSS, JavaScript
## Our Team:
**Amir Ebrahimi (Mentor)** - Principal Software Engineer, Austin/Unity Technologies, USA <br>
**Shaun Radgowski (Mentor)** - Financial Analyst, Morgan Stanley, USA <br>
**Saeed Motamed (Mentor)** - Cloud Solution Architect, Microsoft, UAE <br>
**Hadeel Ehmouda (Student)** - Master's Student, Birzeit University, Jordan & Palestine <br>
**Phil Wee (Student)** - Undergraduate, NYUAD, Philippines & UAE <br>
**Soyuj Jung Basnet (Student)** - Undergraduate, NYUAD, Nepal & United Arab Emirates <br>
**Nouran Sheta (Student)** - Undergraduate, AUS, Egypt & UAE <br>
**Belal Malabeh (Student)** - Undergraduate, Applied Science University, Jordan <br>
**Majd Maree (Student)** - Undergraduate, Birzeit University, Palestine <br>
**Nouf Alababsi (Student)** - Undergraduate, NYUAD, Junior, UAE <br>
**Nghia Nim (Student)** - Undergraduate, NYUAD, Vietnam & UAE <br>
