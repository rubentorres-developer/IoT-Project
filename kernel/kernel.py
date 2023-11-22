import json
import os
import requests

from pymongo import MongoClient
import paho.mqtt.client as mqtt


USERNAME = "LOCAL"
CLIENT_ID = f"SUB_{ USERNAME }"
TOPIC = f"IoT/{ USERNAME }"
ML_PROCESSOR_URL = os.environ["ML_PROCESSOR_URL"]
MONGODB_URL = os.environ["MONGODB_URL"]
MQTT_HOST = os.environ["MQTT_HOST"]


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(TOPIC)
        print(f"{ CLIENT_ID } has connected and subscribed to { TOPIC }!")
    else:
        print(f"{ CLIENT_ID } was unable to connect (return code = { rc })!")


def on_message(mongo_collection, client, userdata, message):
    data = message.payload.decode("utf-8")
    json_data = json.loads(data)
    response = requests.post(ML_PROCESSOR_URL, json=json_data)
    document = response.json()
    mongo_collection.insert_one(document)


def main():
    try:
        mongo_client = MongoClient(MONGODB_URL)
        mongo_database = mongo_client["database"]
        mongo_collection = mongo_database["collection"]

        client = mqtt.Client(CLIENT_ID)
        client.on_connect = on_connect
        client.on_message = lambda client, userdata, message: on_message(
            mongo_collection, client, userdata, message
        )
        client.connect(MQTT_HOST)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nTerminating the script due to a keyboard interrupt.")
    except Exception as e:
        print(e)
    finally:
        client.disconnect()
        client.loop_stop()
        print(f"{ CLIENT_ID } has disconnected.")


if __name__ == "__main__":
    main()
