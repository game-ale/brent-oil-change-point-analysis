from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import json
from pathlib import Path
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_FILE = DATA_DIR / "raw" / "BrentOilPrices.csv"
EVENTS_FILE = DATA_DIR / "processed" / "events.csv"
RESULTS_FILE = DATA_DIR / "processed" / "change_point_results.json"

@app.route('/api/prices', methods=['GET'])
def get_prices():
    try:
        # Fallback if raw data file not found
        file_path = RAW_DATA_FILE
        if not file_path.exists():
            file_path = PROJECT_ROOT / "Data" / "BrentOilPrices.csv"
            
        df = pd.read_csv(file_path)
        # Simplify data for transport (React charts like list of objects)
        data = df.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        df = pd.read_csv(EVENTS_FILE)
        data = df.to_dict(orient='records')
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/results', methods=['GET'])
def get_results():
    try:
        if not RESULTS_FILE.exists():
            return jsonify({"error": "Results not found yet"}), 404
            
        with open(RESULTS_FILE, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
