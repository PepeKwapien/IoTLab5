import paho.mqtt.client as mqttc
from src.server.serverConfig import *
from src.server.userInteraction import user_interation as ui
import json
from tinydb import where
import time
from datetime import datetime


def on_message(client, userdata, message):
    decrypted = json.loads(message.payload)

    if not decrypted["terminal_id"] or not decrypted["card_id"] or not decrypted["time"]:
        return

    t_id = decrypted["terminal_id"]
    c_id = decrypted["card_id"]

    terminals = db.table('terminals')
    exist = terminals.search(where('id') == t_id)
    if not exist:
        print(f"Terminal ID {t_id} is not on the list of all available terminals. Access not granted")
        return

    cards = db.table('cards')
    exist = cards.search(where('id') == c_id)
    if not exist:
        cards.insert({'id': c_id})
        print(f"New card entry - ID: {c_id}")

    work_time = db.table("work_time")
    work_time.insert({"terminal_id": decrypted["terminal_id"], "card_id": decrypted["card_id"],
                      "time": decrypted["time"]})
    local_time = datetime.fromtimestamp(decrypted["time"]).strftime(date_format)
    print(f"New work entry - Card ID: {c_id}\t Terminal ID: {t_id}\t at {local_time}")


def start_server():
    client = mqttc.Client(device_name)
    client.connect(ip)
    client.on_message = on_message
    client.loop_start()
    client.subscribe(topic)

    while not client.is_connected:
        time.sleep(1)

    ui()
    client.loop_stop()


if __name__ == "__main__":
    start_server()
