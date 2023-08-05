
# python 3.6
import random
import time

from paho.mqtt import client as mqtt_client

class MqTT:

    # default
    broker = 'broker.emqx.io'
    port = 1883
    # generate client ID with pub prefix randomly
    client_id = f'py-mqtt-mb-{random.randint(0, 1000)}'
    mq_client = mqtt_client.Client(client_id)
    is_connect = False

    def __init__(self):
        pass
    
    # version
    def version(self):
        return "1.0.0"

    # set broker
    def set_broker(self,ID,server,port):
        if ID != None:
            self.client_id = ID
        self.broker = server
        self.port = port

    # connect
    def connect(self):
        self.connect_mq()
        self.loop_start()
        time.sleep(1)
        return self.is_connect

    # connect server
    def connect_mq(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
                self.is_connect = True
            else:
                self.is_connect = False
                print("Failed to connect, return code %d\n", rc)
        #client = mqtt_client.Client(client_id)
        self.mq_client.on_connect = on_connect
        self.mq_client.connect(self.broker, self.port)
        return self.mq_client

    # disconnect
    def off(self):
        self.mq_client.disconnect()

    # publish
    def publish_message(self,topic="mb", data="msg"):
        result = self.mq_client.publish(topic, data)
        # result: [0, 1]
        status = result[0] # 0 is ok
        return status

    # subscribe
    def subscribe_message(self,topic,callback):
        def on_message(client, userdata, msg):
            # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            callback(msg.topic,msg.payload.decode())

        self.mq_client.subscribe(topic)
        self.mq_client.on_message = on_message

    # loop_start
    def loop_start(self):
        self.mq_client.loop_start()

    # loop_forever
    def loop_forever(self):
        self.mq_client.loop_forever()

    # client
    def get_client(self):
        return self.mq_client

mqtt = MqTT()
