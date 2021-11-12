from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json

class AppMessages(AsyncWebsocketConsumer):

    async def connect(self):
        self.groupname = "appmsg"
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data):
        datapoint = json.loads(text_data)
        val = datapoint['value']
        
        await self.channel_layer.group_send(
            self.groupname,
            {
                'type' : 'deprocessing',
                'value': val
            }
        )
        print('>>>>>>>', text_data)
        
    async def deprocessing(self, event):
        valOther = event['value']

        await self.send(text_data=json.dumps({'value': valOther}))

    async def disconnect(self, code):
        #await self.disconnect()
        pass