# switch/tasks.py
import time
from celery import shared_task
from django.utils import timezone
from .models import Switch, PingHistory
from .services import snmp_get_request
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string # Template render etmek için

@shared_task
def check_device_status(switch_id):
    """
    Verilen ID'ye sahip switch'i kontrol eder, durumunu günceller,
    geçmiş kaydı oluşturur VE SONUCU WEBSOCKET'E GÖNDERİR.
    """
    try:
        switch = Switch.objects.get(id=switch_id)
    except Switch.DoesNotExist:
        return

    # ... (SNMP kontrol kısmı aynı kalıyor) ...
    start_time = time.time()
    value, error = snmp_get_request(
        switch.ip_address,
        switch.snmp_community,
        switch.system_description_oid
    )
    if error:
        print(f"SNMP error on {switch.name}: {error}")
    end_time = time.time()
    is_reachable = value is not None
    response_time_ms = (end_time - start_time) * 1000 if is_reachable else None
    
    if is_reachable:
        switch.status = 'up'
        switch.last_seen = timezone.now()
    else:
        switch.status = 'down'
    switch.save()
    
    PingHistory.objects.create(
        switch=switch,
        is_reachable=is_reachable,
        response_time=response_time_ms
    )
    print(f"Checked: {switch.name} - Status: {'Up' if is_reachable else 'Down'}")

    # --- YENİ EKLENEN KISIM ---
    # Kanala mesaj gönderme
    channel_layer = get_channel_layer()
    
    # Güncellenen satırın HTML'ini sunucu tarafında hazırlayalım
    html = render_to_string("switch/partials/switch_table_row.html", {"switch": switch})
    
    # Consumer'daki `switch_status_update` metodunu tetikleyecek mesajı gönderiyoruz.
    # async_to_sync sarmalayıcısını senkron bir görevden (Celery) asenkron bir fonksiyona (group_send)
    # çağrı yapmak için kullanıyoruz.
    async_to_sync(channel_layer.group_send)(
        'switch_updates', # Mesajın gönderileceği grup
        {
            'type': 'switch.status.update', # Çalıştırılacak consumer metodu
            'id': switch.id,
            'html': html
        }
    )


# poll_all_switches görevinde değişiklik yok.
@shared_task
def poll_all_switches():
    switches = Switch.objects.all()
    for switch in switches:
        check_device_status.delay(switch.id)