from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from .models import Usuario_BD, Dominios_BD
from .decorators import login_admin, login_admindominio, login_user
import random


''' FUNCOES DE LOGIN E CADASTRO '''

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')  
        try:
            usuario = Usuario_BD.objects.get(email=email) 
            verifica_senha = check_password(senha, usuario.senha)

            if verifica_senha:
                request.session['user_flag'] = usuario.flag  
                if usuario.flag == 'A':
                    # Se a flag for 'A' (Admin), redirecione para a pagina de admin
                    return redirect('admin')
                elif usuario.flag == 'D':
                    # Se a flag for 'D' (Dominio), redirecione para a pagina de adm de dominio
                    return redirect('admindominio')
                else:
                    # Se a flag for outra (nesse caso 'U'), redirecione para a pagina de usuario de dominio
                    return redirect('userdominio')
            else:
                raise Usuario_BD.DoesNotExist 
            
        except Usuario_BD.DoesNotExist:
            return render(request, 'login.html')
        
    else:
        return render(request, 'login.html')

def cadastro(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        flag = request.POST.get('flag')
        senha = request.POST.get('senha')
        senhavoip = random.randint(10000, 99999)

        try:
            novo_usuario = Usuario_BD()
            novo_usuario.email = email
            novo_usuario.senha = make_password(senha)
            novo_usuario.senhavoip = senhavoip
            novo_usuario.flag = flag
            novo_usuario.save() 
        except:
            erro_cadastro = "Voce ja possui uma conta com esse email!"
            return render(request, 'cadastro.html', {'erro_cadastro': erro_cadastro})

        return redirect('inicio')

    else:
        return render(request, 'cadastro.html')
    

''' FUNCOES DE ERRO '''

def erro_autorizacao(request):
    return render(request, 'erro_autorizacao.html')



''' TROCA DE SENHA '''



''' FUNCOES RELACIONADAS AOS DOMINIOS '''

def remover_dominio(request):
    pass

def adicionar_dominio(request):
    pass

def trocar_senha(request):
    pass

@login_admin
def admin(request):
    dados_dominios = Dominios_BD.objects.all()
    return render(request, 'admin/painel.html', {'dominios': dados_dominios})

@login_admindominio
def admindominio(request):
    return render(request, 'admin-dominio/painel.html')

@login_user
def userdominio(request):
    return render(request, 'user-dominio/painel.html')


