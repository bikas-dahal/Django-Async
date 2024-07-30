from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync
import json

from .models import Message



class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
        print(self.scope.get('url_route').get('kwargs').get('id'))
        
    def disconnect(self, close_code):
        print('Connection closed: %s' % close_code)

    def receive(self, text_data):
        text_data = json.loads(text_data)       
        
        message = Message()
        message.messages = text_data['message']
        message.sender = self.scope['user']
        message.receiver = self.scope['receiver']
        
    
    def recevier_function(self, text_data):
        print('Received: %s' % text_data)

        
        