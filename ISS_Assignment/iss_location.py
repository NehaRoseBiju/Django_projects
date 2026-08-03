import requests
import pandas as pd
import time
from datetime import datetime
import matplotlib.pyplot as plt

# Lists to store data
timestamps = []
latitudes = []
longitudes = []

print("Collecting ISS location data...\n")

count = 0

while count < 100:
    try:
        # Fetch ISS location from Open Notify API
        response = requests.get(
            "http://api.open-notify.org/iss-now.json",
            timeout=10
        )

        # Check for HTTP errors
        response.raise_for_status()

        # Convert response to JSON
        data = response.json()

        # Verify API response
        if data["message"] != "success":
            print("API did not return success. Retrying...")
            time.sleep(5)
            continue

        # Current time
        timestamp = datetime.now()

        # Extract latitude and longitude
        latitude = float(data["iss_position"]["latitude"])
        longitude = float(data["iss_position"]["longitude"])

        # Store data
        timestamps.append(timestamp)
        latitudes.append(latitude)
        longitudes.append(longitude)

        count += 1

        print(f"{count:03d} | {timestamp} | Latitude: {latitude:.4f} | Longitude: {longitude:.4f}")

        # Wait 5 seconds
        time.sleep(5)

    except requests.exceptions.RequestException as e:
        print("Connection Error:", e)
        print("Retrying in 5 seconds...\n")
        time.sleep(5)

    except ValueError:
        print("Invalid data received. Retrying...\n")
        time.sleep(5)

# Create DataFrame
df = pd.DataFrame({
    "Timestamp": timestamps,
    "Latitude": latitudes,
    "Longitude": longitudes
})

# Save CSV
df.to_csv("iss_data.csv", index=False)

print("\nData saved to iss_data.csv")

# Statistics
print("\n========== Latitude Statistics ==========")
print("Maximum Latitude :", df["Latitude"].max())
print("Minimum Latitude :", df["Latitude"].min())
print("Average Latitude :", df["Latitude"].mean())

print("\n========== Longitude Statistics ==========")
print("Maximum Longitude:", df["Longitude"].max())
print("Minimum Longitude:", df["Longitude"].min())
print("Average Longitude:", df["Longitude"].mean())

# Latitude Graph
plt.figure(figsize=(12, 5))
plt.plot(df["Timestamp"], df["Latitude"], marker="o")
plt.title("Latitude vs Time")
plt.xlabel("Time")
plt.ylabel("Latitude")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("Latitude_Graph.png")
plt.show()

# Longitude Graph
plt.figure(figsize=(12, 5))
plt.plot(df["Timestamp"], df["Longitude"], marker="o")
plt.title("Longitude vs Time")
plt.xlabel("Time")
plt.ylabel("Longitude")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig("Longitude_Graph.png")
plt.show()

print("\nAssignment completed successfully!")