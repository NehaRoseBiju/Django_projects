import requests
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)


def fetch_temperature():

    api = "https://api.open-meteo.com/v1/forecast?latitude=9.9312&longitude=76.2673&current=temperature_2m"

    response = requests.get(api)

    data = response.json()

    temperature = data["current"]["temperature_2m"]

    supabase.table("weather_readings").insert(
        {
            "temperature": temperature
        }
    ).execute()

    print("Temperature Stored:", temperature)


if __name__ == "__main__":
    fetch_temperature()