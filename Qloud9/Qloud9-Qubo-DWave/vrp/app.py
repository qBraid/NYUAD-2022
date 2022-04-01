import json
import flask
from flask import Response
from flask import request, jsonify
import googlemaps
from main_solver import MainSolver

# ASSUMPTIONS
fuel_efficiency = 1
price_weight = 1
fuel_price = 1
mode = "driving"


app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=["GET"])
def rootdir():
    return '''
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
    '''

@app.route('/run', methods=['POST'])
def main():
    if request.method == "POST":
        dictdata = request.get_json().get('location')
        destinations = []
        for i in range(len(dictdata)):
            cur_lat = str(dictdata[i]['lat'])
            cur_long = str(dictdata[i]['lng'])
            destinations.append(cur_lat + "," + cur_long)

        num_dest = len(destinations)

        # Enter Google Maps API Key
        API_key = "AIzaSyCqeAPYq7aUWmy3CZWPEqLKYJF4iaZ-YPw"
        gmaps = googlemaps.Client(key=API_key)

        all_time = []
        all_dist = []
        for origin in destinations:
            for destination in destinations:
                dist_time = gmaps.distance_matrix(origin, destination, mode=mode)
                dist_time = dist_time["rows"][0]["elements"][0]
                dist = dist_time['distance']['value']
                time = dist_time['duration']['value']
                all_time.append(time)
                all_dist.append(dist)

        total_cost = []
        for i in range(num_dest ** 2):
            ac = price_weight * all_dist[i] * fuel_efficiency * fuel_price
            # Optional time component:
            # ac += (1 - price_weight) * all_time[i]
            total_cost.append(ac)
        
        final=[]
        final1=[]
        final2=[]
        for i in range(1, num_dest+1):
            for j in range(1, num_dest+1):
                final1.append(i)
                final2.append(j)
        
        graph_text = "\n"
        final.extend([final1, final2, total_cost])
        for i in range(num_dest ** 2):
            if final[0][i] != final[1][i]:
                graph_text += f"{final[0][i]},{final[1][i]},{final[2][i]}\n"
        
        scenario_text = f"1\n1\n\n{num_dest - 1}\n"

        for i in range(2, num_dest + 1):
            scenario_text += f"{i} 0 0 10\n"
        
        scenario_text += "\n2\n20\n20"
        solver =  MainSolver(scenario_text = scenario_text, graph_text=graph_text)
        solution = solver.return_value()

        final_answer = {}
        for i in range(len(solution)):
            final_answer[f"Truck{i}"] = [dictdata[x] for x in solution[i]]

        print(final_answer)
        return jsonify(final_answer)

if __name__ == "__main__":
    app.run()
