# switch/models.py
from django.db import models


class PingHistory(models.Model):
    switch = models.ForeignKey("switch.Switch", on_delete=models.CASCADE, related_name="ping_history")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_reachable = models.BooleanField()
    response_time = models.FloatField(null=True, blank=True, help_text="ms cinsinden")

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.switch.name} @ {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"


class Vendor(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class DeviceModel(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.vendor.name} - {self.name}"

class Switch(models.Model):
    STATUS_CHOICES = [
        ('up', 'Up'),
        ('down', 'Down'),
        ('unknown', 'Unknown'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Device Name")
    ip_address = models.GenericIPAddressField(unique=True, verbose_name="IP Adress")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name="Vendor")
    model = models.ForeignKey(DeviceModel, on_delete=models.CASCADE, verbose_name="Model")
    snmp_community = models.CharField(max_length=50, default='public', verbose_name="SNMP Community")
    snmp_version = models.CharField(max_length=5, choices=[('1', 'SNMP v1'), ('2c', 'SNMP v2c'), ('3', 'SNMP v3')], default='2c')

    system_description_oid = models.CharField(max_length=200, default='1.3.6.1.2.1.1.1.0', verbose_name="Sistem Description OID")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unknown', verbose_name="Status")
    last_seen = models.DateTimeField(null=True, blank=True, verbose_name="Last Seen")
     # --- YENİ EKLENEN ALANLAR ---
    device_type = models.CharField(
        max_length=50, 
        default='cisco_ios', 
        verbose_name="Device Type (Netmiko için)",
        help_text="Exmp: cisco_ios, hp_procurve, arista_eos"
    )
    username = models.CharField(max_length=100, verbose_name="SSH Username", blank=True)
    password = models.CharField(max_length=100, verbose_name="SSH Password", blank=True)

    #---------------------------------


    def __str__(self):
        return self.name


