from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Load data from a file (to store progress permanently)
DATA_FILE = "water_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"water_intake": 0, "streak": 0, "last_logged": ""}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@app.route('/')
def index():
    data = load_data()
    remaining_water = 128 - data["water_intake"]
    return render_template("index.html", water_intake=data["water_intake"], remaining_water=remaining_water, streak=data["streak"])

@app.route('/add_water', methods=['POST'])
def add_water():
    data = load_data()
    amount = int(request.form.get('amount', 0))
    
    # Update water intake
    data["water_intake"] += amount
    remaining_water = max(0, 128 - data["water_intake"])

    # Check streak (if logged on a new day)
    today = datetime.now().strftime("%Y-%m-%d")
    if data["last_logged"] != today:
        data["streak"] += 1
        data["last_logged"] = today

    save_data(data)

    return jsonify({"water_intake": data["water_intake"], "remaining_water": remaining_water, "streak": data["streak"]})

@app.route('/water_history')
def water_history():
    data = load_data()
    return jsonify({
        "dates": [data["last_logged"]],
        "amounts": [data["water_intake"]]
    })

if __name__ == '__main__':
    app.run(debug=True)
