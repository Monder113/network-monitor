from django.utils.timezone import now
from .services import snmp_get_request
import os, platform

def ping(ip):
    cmd = "ping -n 1 " if platform.system().lower()=="windows" else "ping -c 1 "
    return os.system(cmd + ip) == 0

def check_switch_status(switch):
    try:
        oid = switch.system_description_oid or "1.3.6.1.2.1.1.1.0"
        response = snmp_get_request(switch.ip_address, switch.snmp_community, oid)
    except Exception:
        response = None

    if response:
        switch.status = 'up'
        switch.last_seen = now()
    else:
        # SNMP yoksa ping fallback
        if ping(switch.ip_address):
            switch.status = 'up'
            switch.last_seen = now()
        else:
            switch.status = 'down'

    switch.save()
    return switch.status
