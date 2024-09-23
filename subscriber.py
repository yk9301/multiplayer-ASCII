import paho.mqtt.client as mqtt
import logging
from main import *



def subscriber():
    # Logging aktivieren für detaillierte Debug-Informationen
    logging.basicConfig(level=logging.DEBUG)

    # Client initialisieren
    client = mqtt.Client(client_id="subscriber1", protocol=mqtt.MQTTv311)
    client.enable_logger()

    # Broker-Adresse und Port
    broker_address = "192.168.86.72" 
    port = 1883  # Standard-MQTT-Port

    # Callbacks zuweisen
    client.on_connect = on_connect
    client.on_message = on_message

    # Verbindung zum Broker herstellen
    try:
        client.connect(broker_address, port=port, keepalive=60)
    except Exception as e:
        print(f"Verbindungsfehler: {e}")
        exit(1)

    # Netzwerk-Loop starten und dauerhaft laufen lassen
    client.loop_forever()

# Callback-Funktion für Verbindung
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Subscriber verbunden")
        client.subscribe("update")  # Abonniere das Thema
    else:
        print(f"Subscriber Verbindung fehlgeschlagen mit Code {rc}")

# Callback-Funktion für empfangene Nachrichten
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    topic = msg.topic
    print(f"Nachricht empfangen: Thema: {topic}, Nachricht: {message}")
    
    # Aktion basierend auf der Nachricht ausführen
    if topic == "update":
        print(message)
    
        