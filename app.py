from flask import Flask, render_template, request, jsonify
import requests
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY", "your_default_key")

user_points = 0  # Initialize user points

# Route for the homepage
@app.route("/")
def index():
    global user_points
    return render_template("index.html", user_points=user_points)

# Route to handle feedback submission
@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    global user_points
    feedback = request.form.get("feedback")
    if feedback:
        user_points += 10  # Reward points for feedback
        with open("user_feedback.txt", "a") as f:
            f.write(f"Reported Issue: {feedback}\n")
        return jsonify({"status": "success", "message": "Feedback submitted!", "points": user_points})
    return jsonify({"status": "error", "message": "No feedback provided."})

# Route to fetch traffic data
@app.route("/traffic_data", methods=["GET"])
def traffic_data():
    start_location = "80.2707,13.0827"  # Chennai
    end_location = "77.5946,12.9716"    # Bangalore
    url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={API_KEY}&start={start_location}&end={end_location}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        route = data['routes'][0]
        distance = route['summary']['distance'] / 1000  # Convert meters to kilometers
        duration = route['summary']['duration'] / 60    # Convert seconds to minutes
        return jsonify({"distance": f"{distance:.2f} km", "duration": f"{duration:.2f} minutes"})
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to show emissions impact (returns a plot)
@app.route("/emission_impact")
def emission_impact():
    data = {
        "Route": ["Route 1", "Route 2", "Route 3"],
        "Emissions (g CO2)": [100, 80, 120]
    }
    df = pd.DataFrame(data)

    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(8, 5))
    sns.barplot(x="Route", y="Emissions (g CO2)", data=df, palette="Greens_d")
    plt.title("Emissions Impact of Different Routes")
    plot_path = "static/emission_plot.png"
    plt.savefig(plot_path)
    plt.close()
    return jsonify({"plot_url": plot_path})

# Route to reset points
@app.route("/reset_points", methods=["POST"])
def reset_points():
    global user_points
    user_points = 0
    return jsonify({"status": "success", "message": "Points reset.", "points": user_points})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
