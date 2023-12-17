from django.db import models




''' CRIANDO AS TABELAS DO BD '''

class Usuario_BD(models.Model):
    # tabela que armazena todos usuarios (nome = Usuario_BD)
    # Colunas abaixo:
    id = models.AutoField(primary_key=True) 
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=6)
    # flag determina o tipo de usuario (A = Admin, D = Admin de Dominio, U = Usuario de Dominio)
    flag = models.CharField(max_length=1, default='U') 



class Dominios_BD(models.Model):
    # tabela que armaze os dominios (nome = Dominios_BD)
    # Colunas abaixo:
    id = models.AutoField(primary_key=True)
    dominio = models.CharField(max_length=256,unique=True)
    # id_admin determina o admin que criou o dominio (associa a tabela Usuario_BD)
    id_admin = models.CharField(max_length=256)

