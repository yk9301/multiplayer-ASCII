import paho.mqtt.client as mqtt

def publisher(message: str, player):
    
    broker_address = "192.168.86.72" 
    client = mqtt.Client(client_id="Publisher" + str(player), protocol=mqtt.MQTTv311)
    client.connect(broker_address, 1883, 60)
    client.publish("update", message)
