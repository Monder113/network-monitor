# network_monitor_project/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'network_monitor.settings')
# YENİ EKLENEN SATIRLAR
# Bu satırlar, Django uygulamalarını ve modellerini yükleyerek
# "Apps aren't loaded yet." hatasını önler.
import django
django.setup()

app = Celery('network_monitor')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periyodik görevleri burada tanımla (Celery Beat)
app.conf.beat_schedule = {
    'poll-all-switches-every-minute': {
        'task': 'switch.tasks.poll_all_switches',
        'schedule': crontab(minute='*/1'), # Her dakika çalıştır
    },
}