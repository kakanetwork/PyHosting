
from django.contrib import admin
from django.urls import path
from apphosting import views

urlpatterns = [
    path('', views.login_view, name='inicio'),
    path('painel/', views.admin, name='admin'),
    path('painel/', views.admindominio, name='admindominio'),
    path('painel/', views.userdominio, name='userdominio'),
    path('cadastrar/', views.cadastro, name='cadastrar'),
    path('erro/', views.erro_autorizacao, name='erro_autorizacao'),
    path('remover_dominio/<int:item_id>/', views.remover_dominio, name='remover_dominio'),
    path('adicionar_dominio/', views.adicionar_dominio, name='adicionar_dominio'),
    path('trocar_senha/', views.trocar_senha, name='trocar_senha'),
]
