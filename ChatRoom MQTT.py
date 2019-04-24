import threading
import paho.mqtt.client as mqtt
import os

def on_connect(client, userdata, flags, rc):
    global canal
    global user_name
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome "+user_name+", you're connected to "+canal)
    client.subscribe(canal)

def on_message(client, userdata, msg):
    global user_name
    incoming_message = msg.payload.decode()
    splitted_msg = [x.strip() for x in incoming_message.split(',',1)]
    sender_name = splitted_msg[0]
    if sender_name != user_name:
        print(sender_name + ":" + splitted_msg[1])

def publicar():
    global user_name
    global canal
    new_msg = input()
    client.publish(canal, user_name + "," + new_msg);
    return publicar()

def recibir():
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


def config():
    global user_name
    global canal
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    while True:
        user_name = input("Enter your username: ")
        if user_name.isalpha():
            break
        print("Please enter characters A-Z only")
    
    while True:
        canal = input("Enter the channel you want to connect: ")
        if canal.isalpha():
            break
        print("Please enter characters A-Z only")
    
    return "Loading chat ("+canal+")..."

print(config())
client = mqtt.Client()
client.connect("broker.hivemq.com",1883,60)
hilo1 = threading.Thread(target=publicar)
hilo2 = threading.Thread(target=recibir)
hilo1.start()
hilo2.start()
