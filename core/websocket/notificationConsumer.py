# Utils 
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import datetime
# Queries
from .queries.notificationConsumer import get_token, invalidate_token, make_aware_async

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            from apps.authentication.models import Token
            await self.accept()
            tokenString = self.scope['query_string'].decode('utf-8').split('=')[1]
            token       = await get_token(self, Token, tokenString)
            user        = token['user']
            currentDate = await self.aware_datetime()


            if not token:
                await self.send(text_data=json.dumps({
                    'message': 'Token de acceso invalido o expirado'
                }))
                await self.close()
                return
            
            if token['expiration'] < currentDate:
                await invalidate_token(token)
                await self.send(text_data=json.dumps({
                    'message': 'Token invalido o expirado. Por favor inicie sesión nuevamente.'
                }))
                await self.close()
            # create a room for the user
            await self.channel_layer.group_add(
                f'notification_{user}',
                self.channel_name
            )
            await self.send(text_data=json.dumps({
                'message': 'Conexión exitosa'
            }))

        except Exception as e:
            await self.send(text_data=json.dumps({
                'message': f'{str(e)}'
            }))
            await self.close()

            

    async def disconnect(self, close_code):
        try:
            await self.close()
        except Exception as e:
            pass
        finally:
            from apps.authentication.models import Token
            tokenString = self.scope['query_string'].decode('utf-8').split('=')[1]
            token       = await get_token(self, Token, tokenString)
            user        = token['user']
            await self.channel_layer.group_discard(f'notification_{user}', self.channel_name)
            

    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))


    async def notification_message(self, event):
        print('entre')
        print('message', event)
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))



    async def aware_datetime(self):
        naive_datetime = datetime.datetime.now()
        aware_datetime = await make_aware_async(naive_datetime) 
        return aware_datetime