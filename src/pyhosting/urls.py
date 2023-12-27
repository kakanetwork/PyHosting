from django.contrib import admin
from django.urls import path
from apphosting import views

urlpatterns = [
    path('', views.PageLogin, name='inicio'),
    path('painel/', views.PageAdmin, name='admin'),
    path('paineladmin/', views.PageAdminDominio, name='admindominio'),
    path('paineluser/', views.PageUser, name='userdominio'),
    path('cadastrar/', views.PageCadastro, name='cadastrar'),
    path('unauthorized/', views.PageUnauthorized, name='unauthorized'),
    
    path('logout/', views.Logout, name='logout'),

    path('trocasenha/', views.trocar_senha, name='trocasenha'),

    path('remover_dominio/<int:item_id>/', views.remover_dominio, name='remover_dominio'),
    path('adicionar_dominio/', views.adicionar_dominio, name='adicionar_dominio'),
    path('senha_admdom/<int:id>/', views.senha_admdom, name='senha_admdom'),

    path('remover_user/<int:id>/', views.remover_user, name='remover_user'),
    path('adicionar_user', views.adicionar_user, name='adicionar_user'),
]
