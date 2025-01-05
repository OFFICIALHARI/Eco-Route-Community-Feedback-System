import tkinter as tk
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tkinter import messagebox, ttk
from dotenv import load_dotenv
import os

class EcoRouteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Eco-Route Community Feedback System")
        self.root.geometry("600x700")  # Set window size
        self.user_points = 0  # Initialize points
        
        # Load environment variables from .env file
        load_dotenv()

        # Get the API key from environment variables
        self.api_key = os.getenv("API_KEY", "your_default_key")

        # Apply style
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=5)
        style.configure("TLabel", font=("Helvetica", 12))

        # Create widgets for the main window
        self.title_label = ttk.Label(self.root, text="Eco-Route Feedback", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=10)

        self.points_label = ttk.Label(self.root, text=f"Your Points: {self.user_points}", font=("Helvetica", 14))
        self.points_label.pack(pady=10)

        self.issue_label = ttk.Label(self.root, text="Report Traffic/Environmental Issue:")
        self.issue_label.pack(pady=5)

        self.issue_text = tk.Text(self.root, height=4, width=50, font=("Helvetica", 12))
        self.issue_text.pack(pady=5)

        self.submit_button = ttk.Button(self.root, text="Submit Report", command=self.submit_report)
        self.submit_button.pack(pady=5)

        self.show_traffic_button = ttk.Button(self.root, text="Show Traffic Data", command=self.show_traffic_data)
        self.show_traffic_button.pack(pady=5)

        self.show_emission_button = ttk.Button(self.root, text="Show Emission Impact", command=self.plot_emission_impact)
        self.show_emission_button.pack(pady=5)

        self.green_route_button = ttk.Button(self.root, text="Join Green Route Week", command=self.green_route_challenge)
        self.green_route_button.pack(pady=5)

        self.leaderboard_button = ttk.Button(self.root, text="View Leaderboard", command=self.show_leaderboard)
        self.leaderboard_button.pack(pady=5)

        self.reset_button = ttk.Button(self.root, text="Reset Points", command=self.reset_points)
        self.reset_button.pack(pady=5)

        self.about_button = ttk.Button(self.root, text="About App", command=self.show_about_info)
        self.about_button.pack(pady=5)

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
            messagebox.showwarning("Warning", "No issue reported")

    def show_traffic_data(self):
        start_location = "80.2707,13.0827"  # Chennai
        end_location = "77.5946,12.9716"    # Bangalore
        traffic_data = self.get_traffic_data(start_location, end_location)
        messagebox.showinfo("Traffic Data", traffic_data)

    def get_traffic_data(self, start_location, end_location):
        url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={self.api_key}&start={start_location}&end={end_location}'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            route = data['routes'][0]
            distance = route['summary']['distance'] / 1000  # Convert meters to kilometers
            duration = route['summary']['duration'] / 60    # Convert seconds to minutes
            return f"Distance: {distance:.2f} km, Duration: {duration:.2f} minutes"
        except requests.RequestException as e:
            return f"Error fetching data: {str(e)}"
        except (KeyError, IndexError):
            return "Invalid route data received."

    def plot_emission_impact(self):
        data = {
            "Route": ["Route 1", "Route 2", "Route 3"],
            "Emissions (g CO2)": [100, 80, 120]
        }
        df = pd.DataFrame(data)

        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(8, 5))
        sns.barplot(x="Route", y="Emissions (g CO2)", data=df, palette="Greens_d")
        plt.title("Emissions Impact of Different Routes")
        plt.show()

    def green_route_challenge(self):
        messagebox.showinfo("Green Route Week", "Join us in the Green Route Week and earn bonus points!")

    def show_leaderboard(self):
        leaderboard = f"Leaderboard:\n1. User A - 120 points\n2. User B - 100 points\n3. You - {self.user_points} points"
        messagebox.showinfo("Leaderboard", leaderboard)

    def reset_points(self):
        self.user_points = 0
        self.points_label.config(text=f"Your Points: {self.user_points}")
        messagebox.showinfo("Reset Points", "Your points have been reset.")

    def show_about_info(self):
        about_text = (
            "Eco-Route Community Feedback System\n\n"
            "This application allows users to report traffic and environmental issues, view traffic data, "
            "and explore the environmental impact of different routes. Participate in our Green Route Week "
            "and earn bonus points for contributing to eco-friendly initiatives!"
        )
        messagebox.showinfo("About", about_text)

# Initialize Tkinter window
root = tk.Tk()
app = EcoRouteApp(root)
root.mainloop()
