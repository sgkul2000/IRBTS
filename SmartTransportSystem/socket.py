import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer

class TrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.bus_no = self.scope["url_route"]["kwargs"]["bus_no"]
        self.group_name = "bus_%s" % self.bus_no

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()
        await self.send(text_data=json.dumps({
            'type':'connection_established',
            'message':'you are now connected',
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if(text_data_json['type'] == 'driver'):
            message = text_data_json["location"]
            # await self.send(text_data=json.dumps({"busNo": self.bus_no, "location": message, "type": "server"}))
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "server_forward",
                    "busNo": self.bus_no,
                    "location": message,
                    "cur_stop": text_data_json["cur_stop"],
                    "sender_channel_name": self.channel_name,
                },)
        else:
            await self.send(text_data=json.dumps({"type": "server"}))

    async def server_forward(self, event):
        #send message and username of sender to websocket
        if self.channel_name != event['sender_channel_name']:
            await self.send(
                text_data=json.dumps(
                    {
                        "busNo": event["busNo"],
                        "location": event["location"],
                        "cur_stop": event["cur_stop"]
                    }
                )
            )

