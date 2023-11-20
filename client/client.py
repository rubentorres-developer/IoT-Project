from datetime import datetime
import csv
import json
import time

import paho.mqtt.client as mqtt


USERNAME = "LOCAL"
CLIENT_ID = f"PUB_{ USERNAME }"
TOPIC = f"IoT/{ USERNAME }"


def on_publish(client, userdata, mid):
    print(f"Message ({ mid }) published!")


def main():
    try:
        client = mqtt.Client(CLIENT_ID)
        client.on_publish = on_publish
        client.connect("localhost")

        with open("online_data.csv", "r") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=";")
            next(csv_reader)
            for row in csv_reader:
                current_datetime = datetime.now()
                current_date = current_datetime.strftime("%d/%m/%y")
                current_time = current_datetime.strftime("%H:%M:%S:%f")

                data = {
                    "username": USERNAME,
                    "date": current_date,
                    "time": current_time,
                    "activity": None,
                    "acceleration_x": None,
                    "acceleration_y": None,
                    "acceleration_z": None,
                    "gyro_x": None,
                    "gyro_y": None,
                    "gyro_z": None,
                }

                (
                    data["acceleration_x"],
                    data["acceleration_y"],
                    data["acceleration_z"],
                    data["gyro_x"],
                    data["gyro_y"],
                    data["gyro_z"],
                ) = map(float, row)

                json_data = json.dumps(data)

                client.publish(TOPIC, json_data)

                time.sleep(1)
    except KeyboardInterrupt:
        print("\nTerminating the script due to a keyboard interrupt.")
    except Exception as e:
        print(e)
    finally:
        client.disconnect()
        print(f"{ CLIENT_ID } has disconnected.")


if __name__ == "__main__":
    main()
