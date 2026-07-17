import random
import time
import sys
from datetime import datetime
from supabase_config import supabase

print("====================================================")
print("  IoT Temperature Sensor Simulator Running           ")
print("  Press Ctrl+C to stop simulation.                 ")
print("====================================================")

try:
    while True:
        temperature = round(random.uniform(20.0, 40.0), 2)
        now = datetime.now()
        timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")

        data = {
            "temperature": temperature,
            "date": now.strftime("%Y-%m-%d"),
            "Time Stamp": timestamp_str
        }

        try:
            supabase.table("temp_readings").insert(data).execute()
            print(f"Temperature: {temperature:05.2f}°C | Time: {timestamp_str} | Uploaded Successfully")
        except Exception as e:
            print(f"Temperature: {temperature:05.2f}°C | Time: {timestamp_str} | Upload FAILED: {e}", file=sys.stderr)

        time.sleep(5)
except KeyboardInterrupt:
    print("\nSimulation stopped by user. Exiting gracefully...")
    sys.exit(0)