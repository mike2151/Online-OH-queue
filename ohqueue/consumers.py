from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class QueueConsumer(WebsocketConsumer):

    def connect(self):
        self.group_name = 'ohqueue'

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def ohqueue_update(self, content):
        self.send(text_data=json.dumps({
                'type': 'ohqueue.update',
                'content': 'update'
            }))
        
