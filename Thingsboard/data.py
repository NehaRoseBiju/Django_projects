import json
import random
import time
import paho.mqtt.client as mqtt

BROKER = "thingsboard.cloud"
PORT = 1883

ACCESS_TOKEN = "7orHKrtbgPj83qvMNm8e"

client = mqtt.Client()

client.username_pw_set(ACCESS_TOKEN)

client.connect(BROKER, PORT)

while True:

    temperature = random.randint(20, 40)
    humidity = random.randint(40, 80)

    data = {
        "temperature": temperature,
        "humidity": humidity
    }

    client.publish(
        "v1/devices/me/telemetry",
        json.dumps(data),
        qos=1
    )

    print(data)

    time.sleep(5)