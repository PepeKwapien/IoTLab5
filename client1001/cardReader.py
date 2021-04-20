from src.client1001.clientConfig import *
import time
from random import getrandbits as grb
import json
from datetime import datetime


def read_card():
    return read_card_example(grb(8))


def read_card_example(number):
    c_id = number
    time_from_epoch = time.time()
    local_time = datetime.fromtimestamp(time_from_epoch).strftime(date_format)
    print(f"Card with ID {c_id} read at {local_time}")
    time.sleep(1)

    return json.dumps({"terminal_id": str(terminalID), "card_id": str(c_id), "time": time_from_epoch})
