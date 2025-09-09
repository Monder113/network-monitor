from django import forms
from .models import Switch

class SwitchForm(forms.ModelForm):
    class Meta:
        model = Switch
        fields = ['name', 'ip_address', 'vendor', 'model', 'snmp_community', 'system_description_oid']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ip_address': forms.TextInput(attrs={'class': 'form-control'}),
            'vendor': forms.Select(attrs={'class': 'form-control'}),  # ✅ dropdown
            'model': forms.Select(attrs={'class': 'form-control'}),   # ✅ dropdown
            'snmp_community': forms.TextInput(attrs={'class': 'form-control'}),
            'system_description_oid': forms.TextInput(attrs={'class': 'form-control'}),
        }
