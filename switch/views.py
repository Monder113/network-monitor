from django.shortcuts import render, redirect, get_object_or_404
from .models import Switch
from .forms import SwitchForm
import json

def switch_list_view(request):
    switches = Switch.objects.all()
    return render(request, 'switch/switch_list.html', {'switches': switches})

def switch_detail_view(request, pk):
    switch = get_object_or_404(Switch, pk=pk)
    history = switch.ping_history.all()[:50]

    chart_labels = [h.timestamp.strftime('%H:%M:%S') for h in history][::-1] # Ters çevirerek zamanı düzelt
    chart_data = [h.response_time if h.is_reachable and h.response_time is not None else 0 for h in history][::-1]

    context = {
        'switch': switch,
        'history': history,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'switch/switch_detail.html', context)

def switch_add_view(request):
    if request.method == 'POST':
        form = SwitchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('switch_list')
    else:
        form = SwitchForm()
    return render(request, 'switch/switch_add.html', {'form': form})

from django.http import JsonResponse
from django.template.loader import render_to_string
  # Puresnmp tabanlı snmp_get fonksiyonu kullanılacak

def update_switch_status(request):
    switches = Switch.objects.all()
    html = render_to_string("switch/partials/switch_table.html", {"switches": switches})
    return JsonResponse({"html": html})

def switch_cli_view(request, pk):
    switch = get_object_or_404(Switch, pk=pk)
    return render(request, 'switch/switch_cli.html', {'switch': switch})