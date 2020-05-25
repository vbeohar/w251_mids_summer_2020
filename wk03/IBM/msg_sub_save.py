import paho.mqtt.client as mqttClient
import time

# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("Connected to broker")
#         global Connected                #Use global variable
#         Connected = True                #Signal connection
#     else:
#         print("Connection failed")
count = 0
def on_message(client, userdata, message):
    count += 1
    print("Received message " + str(message.payload) + "on topic "
    + message.topic + "' with QoS " + str(message.qos))
    with open('/mnt/mybucket/'+str(count)+".jpg", 'a+') as f:
         f.write("Message received: "  + message.payload + "\n")

Connected = False   #global variable for the state of the connection

broker_address= "localhost"  #Broker address
port = 1883                         #Broker port

client = mqttClient.Client("Python")               #create new instance
# client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
# client.connect(broker_address,port,60) #connect
client.subscribe("test_topic") #subscribe
client.loop_forever() #then keep listening forever
