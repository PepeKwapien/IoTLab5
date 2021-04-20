import paho.mqtt.client as mqttc
from src.client1001.cardReader import *


def start_client():
    client = mqttc.Client(device_name + str(terminalID))
    client.connect(ip)

    while not client.is_connected:
        time.sleep(1)

    print("Client connected!")

    while True:
        print("Type card ID or 'stop' to shutdown terminal")
        scan = input()

        if scan == "stop":
            break
        elif len(scan) == 0:
            msg = read_card()
            client.publish(topic, msg)
        else:
            try:
                int(scan)
            except Exception as ex:
                print("ID has to be an integer")
                continue
            msg = read_card_example(scan)
            client.publish(topic, msg)

    client.disconnect(ip)


if __name__ == "__main__":
    start_client()