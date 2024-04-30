import json
from django.shortcuts import render
from django.http import HttpResponse
from api.models import *
from ipware import get_client_ip

def my_view(request):
    client_ip, is_routable = get_client_ip(request)
    if request.user_agent.is_mobile:
        device = "Mobile"
    elif request.user_agent.is_tablet:
        device = "Table"
    elif request.user_agent.is_touch_capable:
        device = "is_touch_capable"
    elif request.user_agent.is_pc:
        device = "Pc"
    elif request.user_agent.is_bot:
        device = "Bot"
    else:
        device = "Unknown"
    browser = request.user_agent.browser.family
    os = request.user_agent.os.family
    ins = IpAdd()
    ins.ipAddr = client_ip
    ins.os = os
    ins.device = device
    ins.browser = browser
    ins.save()
    return render(request, 'index.html')