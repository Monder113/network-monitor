# switch/services.py
from puresnmp import get

def snmp_get_request(target_ip, community_string, oid, port=161, timeout=2):
    """
    Belirtilen hedefe bir SNMP GET isteği gönderir.
    Returns: (value: str | None, error_message: str | None)
    """
    try:
        # puresnmp direkt GET yapıyor
        value = get(target_ip, community_string, oid, port=port, timeout=timeout)
        return str(value), None
    except Exception as e:
        return None, str(e)
