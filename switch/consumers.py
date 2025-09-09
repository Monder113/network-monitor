import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SwitchStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Tüm switch güncellemelerini göndereceğimiz bir grup adı tanımlıyoruz.
        self.room_group_name = 'switch_updates'

        # Gruba katılma
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Gruptan ayrılma
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Gruptan bir mesaj alındığında bu fonksiyon çalışır (Celery'den gelen).
    async def switch_status_update(self, event):
        # WebSocket üzerinden istemciye (tarayıcıya) mesajı gönder
        await self.send(text_data=json.dumps({
            'id': event['id'],
            'html': event['html'],
        }))

from .models import Switch
from netmiko import ConnectHandler
from asgiref.sync import sync_to_async


class SwitchCliConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.switch_id = self.scope['url_route']['kwargs']['switch_id']
        try:
            # Veritabanından Switch nesnesini al
            self.switch = await sync_to_async(Switch.objects.get)(id=self.switch_id)
            await self.accept()
            await self.send(text_data=json.dumps({
                "message": f"{self.switch.name} ({self.switch.ip_address}) bağlantısı kuruldu.\nKomut girebilirsiniz."
            }))
        except Switch.DoesNotExist:
            await self.close()

    async def disconnect(self, close_code):
        pass

    @sync_to_async(thread_sensitive=True)
    def execute_command(self, command):
        try:
            connection_details = {
                "device_type": self.switch.device_type,
                "host": self.switch.ip_address,
                "username": self.switch.username,
                "password": self.switch.password,
                "conn_timeout": 10,
            }
            with ConnectHandler(**connection_details) as net_connect:
                return net_connect.send_command(
                    command,
                    strip_prompt=False,
                    strip_command=False
                )
        except Exception as e:
            return f"❌ Hata: {str(e)}"

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json.get("command")

        # Önce komutu ekrana bas
        await self.send(text_data=json.dumps({"message": f"$ {command}"}))

        # Komutu çalıştır
        output = await self.execute_command(command)

        # Sonucu ekrana bas
        await self.send(text_data=json.dumps({"message": output}))
