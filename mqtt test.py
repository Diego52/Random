import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

def print_msg(client, userdata, message):
    print("%s : %s" % (message.topic, message.payload))
while True:
    subscribe.callback(print_msg, "SofiaTopic12345", hostname="broker.hivemq.com")
    #publish.single("homewatchtest-door", 'hola', hostname="test.mosquitto.org")

