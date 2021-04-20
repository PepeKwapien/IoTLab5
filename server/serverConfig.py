import os
from tinydb import TinyDB

ip = "test.mosquitto.org"
device_name = "server"
topic = "Kwapien-IoT5"
date_format = "%Y-%m-%d %H:%M:%S"
file_date_format = "%Y-%m-%d,%H:%M:%S"

db = TinyDB(os.path.abspath("db.json"))
