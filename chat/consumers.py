# first of all we must import the library json for 2 raisons:
#   1- It will help us to deserialiser or load data(messages and username) from the websocket
#   2- It will help us to serialiser or to send data(messages and username) to the websocket
import json

# Here we call the method to give us the access to the server. 
# To understand why we call Async and not sync go check this : https://blog.miguelgrinberg.com/post/sync-vs-async-python-what-is-the-difference
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    # Connection to the server
    async def connect(self):
        #conect to the url
        self.chat_box_name = self.scope["url_route"]["kwargs"]["chat_box_name"]
        
        #give a name to the group
        # Note: Only alphanumerics, hyphens, underscores, or periods are allowed!
        self.room_group_name = "chat_%s" % self.chat_box_name
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        
        # Accept the our request of connection to the server.
        await self.accept()
    
    # Disconnection from the server or Leave the room group.    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)  
        
    
    # Receive message and username from websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        
        #Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chatbox_message",
                "message": message,
                "username": username,
            }
            )
    # Receive message from room group 
    async def group_message(self, event):
        message = event["message"]
        username = event["username"]
        
        # send message and username of sender to websocket
        await self.send(
            text_data=json.dumps(
                {
                     "message": message,
                    "username": username,
                }
               
            )
        )
pass
        
        