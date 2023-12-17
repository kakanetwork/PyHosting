from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from .models import Usuario_BD, Dominios_BD
from django.contrib import messages

from .decorators import login_admin, login_admindominio, login_user
import random


# ======================================================================
''' FUNCOES PARA SERVICOS '''
# ======================================================================


def Redirecionamento(flag):
    # nessa funcao eu pego a flag do usuario e redireciono para a pagina correta 
    if flag == 'A':
        print('Redirecionamento para admin')
        return redirect('admin')
    elif flag == 'D':
        print('Redirecionamento para admin de dominio')
        return redirect('admindominio')
    else:
        print('Redirecionamento para user de dominio')
        return redirect('userdominio')


def trocar_senha(request):
    if request.method == 'POST':
        novasenha = request.POST.get('novaSenha')
        confirmasenha = request.POST.get('confirmarSenha')
        senhaatual = request.POST.get('senhaAtual')
        
        user_id = request.session.get('user_id')
        usuario = Usuario_BD.objects.get(id=user_id)
        if check_password(senhaatual, usuario.senha):
            if novasenha == confirmasenha:
                usuario.senha = make_password(novasenha)
                usuario.save()

                return redirect('logout')
            else:
                mensagem = "Informe a mesma senha na confirmação!"
                messages.error(request, mensagem)
                return redirect('admin')
        else:
            mensagem = "Senha Atual esta incorreta!"
            messages.error(request, mensagem)
            return redirect('admin')
    else:
        return redirect('unauthorized')


def Logout(request):        
    request.session.flush()
    return redirect('inicio')


# ======================================================================
''' FUNCOES RENDER'S DAS PAGINAS '''
# ======================================================================

# Pagina principal responsavel pelo login
def PageLogin(request):
    # verifica se o metodo e POST ou GET para realizar a acao
    if request.method == "POST":
        # Pega o email e senha informados pelo usuario
        email = request.POST.get('email')
        senha = request.POST.get('senha')  
        try:
            # tenta a conexao com o BD com base no email informado
            usuario = Usuario_BD.objects.get(email=email) 
            # verifica se a senha informada e igual a senha do BD (check_password para descriptografar a senha do BD)
            verifica_senha = check_password(senha, usuario.senha)
            if verifica_senha:
                # se a senha bater, eu pego a flag daquele usuario e armazeno em uma nova sessao junto ao ID dele
                user_flag = usuario.flag
                request.session['user_flag'] = user_flag  
                request.session['user_id'] = usuario.id     
                # envio para a funcao redirecionamento (ctrl + click na funcao, para acompanhar ela)
                return Redirecionamento(user_flag)
            else:
                # se a senhas nao coincidir ele manda para o "except" 
                raise Usuario_BD.DoesNotExist 
        except Usuario_BD.DoesNotExist:
            # se o usuario nao existir, a pagina e recarregada e pedido para informar novamente a senha/email
            return render(request, 'login.html')
    else:
        request.session.flush()
        return render(request, 'login.html')
    
def PageCadastro(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        flag = 'A'
        senha = request.POST.get('senha')
        try:
            novo_usuario = Usuario_BD()
            novo_usuario.email = email
            novo_usuario.senha = make_password(senha)
            novo_usuario.flag = flag
            novo_usuario.save() 
        except:
            erro_cadastro = "Voce ja possui uma conta com esse email!"
            return render(request, 'cadastro.html', {'erro_cadastro': erro_cadastro})
        return redirect('inicio')
    else:
        return render(request, 'cadastro.html')
    
def PageUnauthorized(request):
    return render(request, 'erro_autorizacao.html')



# ======================================================================
''' FUNCOES DOS ADMINS '''
# ======================================================================

@login_admin
def PageAdmin(request):
    mensagens = messages.get_messages(request)
    dados_dominios = Dominios_BD.objects.all()
    return render(request, 'admin/painel.html', {'dados_dominios': dados_dominios, 'mensagens': mensagens})

@login_admin
def remover_dominio(request, item_id):
    user_id = request.session.get('user_id')
    result = Dominios_BD.objects.filter(id_admin=user_id)
    try:
        result.get(id=item_id).delete()
        return redirect('admin')
    except:
        return redirect('admin') 
    

@login_admin
def adicionar_dominio(request):
    nome_dominio = request.POST.get('nome_dominio')
    id_admin = request.session.get('user_id')
    print(nome_dominio, id_admin)
    if Dominios_BD.objects.filter(dominio=nome_dominio).exists():
        return redirect('admin')    
    try:
        
        add_dominio = Dominios_BD()
        add_dominio.dominio = nome_dominio
        add_dominio.id_admin = id_admin
        add_dominio.save() 
    except:
        return redirect('logout')
    
    return redirect('admin')


# ======================================================================
''' FUNCOES DOS ADMINS '''
# ======================================================================


@login_admindominio
def PageAdminDominio(request):
    return render(request, 'admin-dominio/painel.html')

@login_user
def PageUser(request):  
    return render(request, 'user-dominio/painel.html')

