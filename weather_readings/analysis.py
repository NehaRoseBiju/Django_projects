import os
from dotenv import load_dotenv
from supabase import create_client
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load Supabase Credentials
# -----------------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# Fetch Data from Supabase
# -----------------------------
response = supabase.table("weather_readings").select("*").execute()

if len(response.data) == 0:
    print("No weather data found.")
    exit()

df = pd.DataFrame(response.data)

# Convert timestamp column
df["recorded_at"] = pd.to_datetime(df["recorded_at"])

# Keep only today's readings
today = pd.Timestamp.now().date()
df = df[df["recorded_at"].dt.date == today]

if len(df) == 0:
    print("No readings available for today.")
    exit()

temperature = df["temperature"]

print("=" * 60)
print("KOCHI WEATHER ANALYSIS")
print("=" * 60)

# -----------------------------
# Statistical Analysis
# -----------------------------
mean_temp = temperature.mean()
median_temp = temperature.median()
mode_temp = temperature.mode().tolist()
max_temp = temperature.max()
min_temp = temperature.min()
range_temp = max_temp - min_temp
variance = temperature.var()
std_dev = temperature.std()

print("\nSTATISTICAL ANALYSIS")
print("-" * 40)

print(f"Mean Temperature           : {mean_temp:.2f} °C")
print(f"Median Temperature         : {median_temp:.2f} °C")

if len(mode_temp) > 0:
    print(f"Mode Temperature           : {mode_temp}")
else:
    print("Mode Temperature           : No Mode")

print(f"Maximum Temperature        : {max_temp:.2f} °C")
print(f"Minimum Temperature        : {min_temp:.2f} °C")
print(f"Range                      : {range_temp:.2f} °C")
print(f"Variance                   : {variance:.2f}")
print(f"Standard Deviation         : {std_dev:.2f}")

# -----------------------------
# Time Series Analysis
# -----------------------------
print("\nTIME SERIES ANALYSIS")
print("-" * 40)

# Hourly Average
hourly_average = (
    df.groupby(df["recorded_at"].dt.hour)["temperature"]
    .mean()
    .reset_index()
)

print("\nHourly Average Temperature")
print(hourly_average)

# Maximum Temperature Time
max_row = df.loc[df["temperature"].idxmax()]

# Minimum Temperature Time
min_row = df.loc[df["temperature"].idxmin()]

print("\nHighest Temperature")
print(f"{max_row['temperature']} °C")
print(f"Recorded At : {max_row['recorded_at']}")

print("\nLowest Temperature")
print(f"{min_row['temperature']} °C")
print(f"Recorded At : {min_row['recorded_at']}")

# -----------------------------
# Temperature Trend Plot
# -----------------------------
plt.figure(figsize=(10,5))

plt.plot(
    df["recorded_at"],
    df["temperature"],
    marker="o"
)

plt.title("Kochi Temperature Trend")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# -----------------------------
# Daily Summary Report
# -----------------------------
print("\nDAILY SUMMARY REPORT")
print("-" * 40)

total_readings = len(df)

observations = []

if mean_temp > 30:
    observations.append("Overall day was warm.")

if range_temp > 5:
    observations.append("Large temperature variation observed.")
else:
    observations.append("Temperature remained fairly stable.")

if max_temp >= 35:
    observations.append("Very high afternoon temperature.")

if min_temp <= 24:
    observations.append("Cool conditions observed.")

if len(observations) == 0:
    observations.append("No significant observations.")

report = {
    "Date": [today],
    "Total Readings": [total_readings],
    "Average Temperature": [round(mean_temp, 2)],
    "Highest Temperature": [max_temp],
    "Highest Time": [max_row["recorded_at"]],
    "Lowest Temperature": [min_temp],
    "Lowest Time": [min_row["recorded_at"]],
    "Observation": ["; ".join(observations)]
}

report_df = pd.DataFrame(report)

# Save report
os.makedirs("reports", exist_ok=True)
report_df.to_csv("reports/daily_report.csv", index=False)

print(f"Total Readings          : {total_readings}")
print(f"Average Temperature     : {mean_temp:.2f} °C")
print(f"Highest Temperature     : {max_temp:.2f} °C")
print(f"Highest Recorded At     : {max_row['recorded_at']}")
print(f"Lowest Temperature      : {min_temp:.2f} °C")
print(f"Lowest Recorded At      : {min_row['recorded_at']}")

print("\nObservations:")
for obs in observations:
    print(f"- {obs}")

print("\nDaily report saved as:")
print("reports/daily_report.csv")

# -----------------------------
# Save Hourly Average
# -----------------------------
hourly_average.to_csv("reports/hourly_average.csv", index=False)

print("\nHourly average saved as:")
print("reports/hourly_average.csv")