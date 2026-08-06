import schedule
import time
from fetch_weather import fetch_temperature

schedule.every(5).minutes.do(fetch_temperature)

print("Weather Monitoring Started...")

fetch_temperature()

while True:

    schedule.run_pending()

    time.sleep(1)