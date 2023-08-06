from django.shortcuts import render,redirect,get_object_or_404
from .models import Instalacaoativo, Actor
from django.http import HttpResponse
import datetime
from django.views.generic import View
from dcim.models import Device, DeviceRole
from django.urls import reverse,reverse_lazy
from django.db.models import Q

class ListConectividadeView(View):
    """
    List all reg in the database.
    """
    def get(self, request):
 
        rg = Instalacaoativo.objects.all()
        dv = Device.objects.all()  
        dr = DeviceRole.objects.prefetch_related('devices_set').all() #pega papel

        return render(request, 'conectividadeapp/listagem.html', {
            'registro': rg,
            'device': dv,
            'devicerole': dr,
            
        })


