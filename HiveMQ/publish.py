import paho.mqtt.client as mqtt

broker = "broker.hivemq.com"
port = 1883
topic = "chat/general"

client = mqtt.Client()

client.connect(broker, port)

while True:
    message = input("Enter Message: ")

    client.publish(topic, message)

    print("Message Published:", message)

    if message.lower() == "exit":
        break

client.disconnect()