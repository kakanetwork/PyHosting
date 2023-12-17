from django.db import models

# Create your models here.

# criando classe que se conecta e cria o DB 
class Usuario_BD(models.Model): 
    id_user = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=6)
    senhavoip = models.CharField(max_length=5)
    flag = models.CharField(max_length=1, default='U')

class Dominios_BD(models.Model):
    id = models.AutoField(primary_key=True)
    dominio = models.CharField(max_length=256,unique=True)