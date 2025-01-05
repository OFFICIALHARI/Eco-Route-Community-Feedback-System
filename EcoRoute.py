import tkinter as tk
import requests
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import messagebox

class EcoRouteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Eco-Route Community Feedback System")
        self.user_points = 0  # Initialize points

        # Create widgets for the main window
        self.title_label = tk.Label(self.root, text="Eco-Route Feedback", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.points_label = tk.Label(self.root, text=f"Your Points: {self.user_points}", font=("Helvetica", 14))
        self.points_label.pack(pady=10)

        self.issue_label = tk.Label(self.root, text="Report Traffic/Environmental Issue:")
        self.issue_label.pack(pady=5)

        self.issue_text = tk.Text(self.root, height=4, width=40)
        self.issue_text.pack(pady=5)

        self.submit_button = tk.Button(self.root, text="Submit Report", command=self.submit_report)
        self.submit_button.pack(pady=5)

        self.show_traffic_button = tk.Button(self.root, text="Show Traffic Data", command=self.show_traffic_data)
        self.show_traffic_button.pack(pady=5)

        self.show_emission_button = tk.Button(self.root, text="Show Emission Impact", command=self.plot_emission_impact)
        self.show_emission_button.pack(pady=5)

        self.green_route_button = tk.Button(self.root, text="Join Green Route Week", command=self.green_route_challenge)
        self.green_route_button.pack(pady=5)

    def submit_report(self):
        issue = self.issue_text.get("1.0", "end-1c")
        if issue:
            self.user_points += 10  # Reward points for submitting a report
            self.points_label.config(text=f"Your Points: {self.user_points}")
            self.issue_text.delete("1.0", "end")
            with open("user_feedback.txt", "a") as f:
                f.write(f"Reported Issue: {issue}\n")
            print(f"Reported Issue: {issue}")
        else:
            print("No issue reported")

    def show_traffic_data(self):
        start_location = "Chennai"
        end_location = "Bangalore"
        traffic_data = self.get_traffic_data(start_location, end_location)
        messagebox.showinfo("Traffic Data", traffic_data)

    def get_traffic_data(self, start_location, end_location):
        API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'
        url = f'https://maps.googleapis.com/maps/api/directions/json?origin={start_location}&destination={end_location}&key={API_KEY}'

        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            routes = data['routes']
            if routes:
                route = routes[0]
                legs = route['legs'][0]
                distance = legs['distance']['text']
                duration = legs['duration']['text']
                return f"Distance: {distance}, Duration: {duration}"
            else:
                return "No route found."
        else:
            return "Error fetching data."

    def plot_emission_impact(self):
        # Example emission data for different routes
        data = {
            "Route": ["Route 1", "Route 2", "Route 3"],
            "Emissions (g CO2)": [100, 80, 120]
        }
        df = pd.DataFrame(data)

        plt.bar(df["Route"], df["Emissions (g CO2)"], color="green")
        plt.xlabel("Route")
        plt.ylabel("Emissions (g CO2)")
        plt.title("Emissions Impact of Different Routes")
        plt.show()

    def green_route_challenge(self):
        messagebox.showinfo("Green Route Week", "Join us in the Green Route Week and earn bonus points!")

# Initialize Tkinter window
root = tk.Tk()
app = EcoRouteApp(root)
root.mainloop()
