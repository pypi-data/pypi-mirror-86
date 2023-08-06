from django.db import models
from datetime import date
from django.db.models.deletion import CASCADE
from dcim.models import Device

# Create your models here.

#class Categoria(models.Model):
#    nome = models.CharField(max_length=100)#define o tipo de registro
#    data_cricao = models.DateTimeField(auto_now_add=True)

#    def __str__(self):
#        return self.nome



class ActivityOptions(models.TextChoices):
    INSTALACAO = 'IN-ADD', 'Instalação/adição'
    SUBSTITUICAO = 'IN-SB', 'Instalação/substituição'
    REMOCAO = 'RE', 'Remoção'

"""
class Instalacaoativo(models.Model):

    comments = models.CharField(max_length=200) # comments
    atv_data = models.DateField(default=date.today)
    reg_atv= models.DateTimeField(auto_now_add=True)
    actor_id = models.ManyToManyField('Actor')
    options = models.CharField(
        max_length=6,
        choices=ActivityOptions.choices,
        default=ActivityOptions.INSTALACAO,
    )
    
    def __str__(self):
        return self.comments
"""
class Actor(models.Model):

    name = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    cellphone = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name



class Activity(models.Model):

    actor = models.ManyToManyField(Actor)
    type = models.CharField(
        max_length=6,
        choices=ActivityOptions.choices,
        default=ActivityOptions.INSTALACAO,
    )
    when = models.DateField(default=date.today)
    description = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.description


class OldDevice(models.Model):
    activity = models.OneToOneField(Activity, on_delete=CASCADE)