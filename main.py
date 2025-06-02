import json
import time

import paho.mqtt.client as mqtt
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties
from sense_hat import SenseHat


def main():
    print("Hello from intdash-relay-example!")
    # 初期化
    sense = SenseHat()
    client = mqtt.Client(protocol=mqtt.MQTTv5)

    # MQTT v5 プロパティ（Content-Type を text/plain に設定）
    properties = Properties(PacketTypes.PUBLISH)
    properties.ContentType = "text/plain"

    # MQTTブローカー接続
    MQTT_BROKER = "0.0.0.0"  # TODO: MQTT Brokerのアドレス
    MQTT_PORT = 1883
    MQTT_TOPIC = "sensors/acceleration"

    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # データ送信ループ
    try:
        while True:
            acceleration = sense.get_accelerometer_raw()
            x = round(acceleration["x"], 5)
            y = round(acceleration["y"], 5)
            z = round(acceleration["z"], 5)

            payload = {
                "x": x,
                "y": y,
                "z": z,
            }

            client.publish(
                topic=MQTT_TOPIC,
                payload=json.dumps(payload),
                qos=0,
                properties=properties,
            )
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("停止しました。")
        client.disconnect()


if __name__ == "__main__":
    main()
