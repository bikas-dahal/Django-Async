from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import Message, UserChannel
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Accept the WebSocket connection
        self.accept()

        # Ensure the user is authenticated
        if not self.scope['user'].is_authenticated:
            self.close()
            return

        try:
            user_channel = UserChannel.objects.get(user=self.scope['user'])
            user_channel.channel = self.channel_name
            user_channel.save()
        except Exception as e:
            user_channel = UserChannel()
            user_channel.user = self.scope['user']
            user_channel.channel = self.channel_name
            user_channel.save()

        self.receiver = self.scope.get('url_route').get('kwargs').get('id')


    def receive(self, text_data):
        try:
            text_data = json.loads(text_data)
            
            receiver = User.objects.get(id=self.receiver)
            print(text_data)
            
            if text_data.get('type') == 'message':
            
                sender = self.scope['user']
                
                message = Message(
                    messages=text_data.get('message'),
                    sender=sender,
                    receiver=receiver
                )
                message.save()
                

                # Send message to receiver's channel
                try:
                    receiver_channel = UserChannel.objects.get(user=receiver)
                    data = {
                        'type': 'receiver_function',
                        'type_of_data': 'message',
                        'message': text_data.get('message')
                    }
                    async_to_sync(self.channel_layer.send)(receiver_channel.channel, data)
                except UserChannel.DoesNotExist:
                    logger.warning(f"No UserChannel found for receiver {receiver}")
            
            elif text_data.get('type') == 'message_seen':
                      # Send message to receiver's channel
                try:
                    receiver_channel = UserChannel.objects.get(user=receiver)
                    data = {
                        'type': 'receiver_function',
                        'type_of_data': 'seen',
                    }
                    async_to_sync(self.channel_layer.send)(receiver_channel.channel, data)

                    unseen_message = Message.objects.filter(receiver=receiver, sender=self.scope.get('user'))
                    unseen_message.update(has_been_seen=True)
                    
                except UserChannel.DoesNotExist:
                    logger.warning(f"No UserChannel found for receiver {receiver}")
            
                
                
        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
        # except User.DoesNotExist:
        #     logger.error("User does not exist")
        # except Exception as e:
        #     logger.error(f"Error receiving message: {e}")

    def receiver_function(self, text_data):
        try:
            data = json.dumps(text_data)
            self.send(data)
            logger.info(f"Received: {text_data}")
        except Exception as e:
            logger.error(f"Error sending data: {e}")

    def disconnect(self, close_code):
        logger.info(f"Connection closed: {close_code}")
