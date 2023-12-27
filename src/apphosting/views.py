from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect
from .models import Usuario_BD, Dominios_BD
from django.contrib import messages

from .decorators import login_admin, login_admindominio, login_user
import random
import os
import sys

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
        flag = request.session.get('user_flag')
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
                request.session['mensagem_info'] = mensagem
                return Redirecionamento(flag)
        else:
            mensagem = "Senha Atual esta incorreta!"
            request.session['mensagem_info'] = mensagem 
            return Redirecionamento(flag)
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
        print(email,senha)
        try:
            # tenta a conexao com o BD com base no email informado
            usuario = Usuario_BD.objects.get(email=email) 
            # verifica se a senha informada e igual a senha do BD (check_password para descriptografar a senha do BD)
            verifica_senha = check_password(senha, usuario.senha)
            print(verifica_senha)
            print(usuario.senha, senha)
            if verifica_senha:
                print('verificou senha')
                # se a senha bater, eu pego a flag daquele usuario e armazeno em uma nova sessao junto ao ID dele
                user_flag = usuario.flag
                request.session['user_flag'] = user_flag  
                request.session['user_id'] = usuario.id     
                # envio para a funcao redirecionamento (ctrl + click na funcao, para acompanhar ela)
                print("vai redirecionar")
                return Redirecionamento(user_flag)
            else:
                # se a senhas nao coincidir ele manda para o "except" 
                print('erroa1')
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
        print(email, senha)
        try:
            print('criando user')
            novo_usuario = Usuario_BD()
            novo_usuario.email = email
            novo_usuario.senha = make_password(senha)
            novo_usuario.flag = flag
            novo_usuario.save() 
        except Exception as err:
            print(err)
            erro_cadastro = "Voce ja possui uma conta com esse email! {0}".format(err)
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
    id_admin = request.session.get('user_id')
    mensagens = request.session.pop('mensagem_info', None)
    dados_dominios = Dominios_BD.objects.all()
    dados_admdominio = Usuario_BD.objects.filter(flag='D', id_admin=id_admin)
    return render(request, 'admin/painel.html', {'dados_dominios': dados_dominios, 'dados_admdominio': dados_admdominio, 'mensagens': mensagens})

@login_admin
def remover_dominio(request, item_id):
    user_id = request.session.get('user_id')
    result = Dominios_BD.objects.filter(id_admin=user_id)

    try:
        dominio = result.get(id=item_id)
        nome_dominio = dominio.dominio
        dominio.delete()
    except:
        return redirect('admin') 

    comando = "python3 /projetoasa/src/apagar_dominio.py {0}".format(nome_dominio)
    os.system(comando)
    os.system("/projetoasa/src/exeroot")

    email = 'root@{0}'.format(nome_dominio)  
    adm_dom = Usuario_BD.objects.filter(id_admin=user_id, email=email, flag='D').first()

    if adm_dom:
        print('apagando admin de dominio')
        id_admdom = adm_dom.id
        adm_dom.delete()
    else:
        print('admin nao encontrado... continuando codigo')
    
    user_dom = Usuario_BD.objects.filter(id_admin=id_admdom, flag='U')

    if user_dom:
        print('apagando usuario')
        user_dom.delete()
    else:
        print('usuario nao encontrado... continuando codigo')

    return redirect('admin')

@login_admin
def senha_admdom(request, id):
    if request.method == 'POST':
        id = request.POST.get('id')
        nova_senha = request.POST.get('novaSenha')
        confirma_senha = request.POST.get('confirmarSenha')
        print(nova_senha, confirma_senha)
        if nova_senha == confirma_senha:
            adm_dominio = Usuario_BD.objects.get(id=id, flag='D')
            try:
                nome_admdom = adm_dominio.email
                adm_dominio.senha = make_password(nova_senha)
                adm_dominio.save()
                print(nova_senha)
                mensagem = "A senha do seu {0} e: {1}".format(nome_admdom, nova_senha)
                request.session['mensagem_info'] = mensagem
            except:
                return redirect('logout')
            return redirect('admin')
        else:
            mensagens = "Informe a mesma senha em ambos os campos"
            return render(request, 'admin/senha_admdom.html', {'mensagens': mensagens, 'id': id})
    else:
        return render(request, 'admin/senha_admdom.html', {'id': id})
    

@login_admin
def adicionar_dominio(request):
    nome_dominio = request.POST.get('nome_dominio')
    id_admin = request.session.get('user_id')


    if Dominios_BD.objects.filter(dominio=nome_dominio).exists():
        mensagem = "Este nome de dominio ja esta em uso!"
        request.session['mensagem_info'] = mensagem
        return redirect('admin')

    try: 
        print('foi bd')
        add_dominio = Dominios_BD()
        add_dominio.dominio = nome_dominio
        add_dominio.id_admin = id_admin
        add_dominio.save() 
        id_dominio = add_dominio.id
    except:
        return redirect('logout')

    comando = "python3 /projetoasa/src/criar_dominio.py {0}".format(nome_dominio)
    os.system(comando)
    os.system("/projetoasa/src/exeroot")

    print('criando')
    mensagem = None

    try:
        senha = random.randint(100000,999999)
        print(senha)
        novo_admdominio = Usuario_BD()
        novo_admdominio.email = "root@{0}".format(nome_dominio)
        novo_admdominio.senha = make_password(senha)
        novo_admdominio.flag = 'D'
        novo_admdominio.id_admin = id_admin
        novo_admdominio.save()

        mensagem = "A senha do seu root@{0} e: {1}".format(nome_dominio, senha)
        request.session['mensagem_info'] = mensagem
        print('deu bom o admin dominio')
        print('debug2')
    except:
        print('deu ruim')
        return redirect('logout')

    print('debug1')
    return redirect('admin')
# ======================================================================
''' FUNCOES DOS ADMINS DE DOMINIO '''
# ======================================================================


@login_admindominio
def PageAdminDominio(request):
    id_admin = request.session.get('user_id')
    mensagens = request.session.pop('mensagem_info', None)
    users_dominio = Usuario_BD.objects.filter(id_admin=id_admin, flag='U')
    return render(request, 'admin-dominio/painel.html', {'mensagens': mensagens, 'users_dominio': users_dominio})

@login_admindominio
def remover_user(request,id):
    user = Usuario_BD.objects.filter(id=id, flag='U').first()
    
    if user:
        print(user.email)
        user.delete()
    else:
        print('Nenhum usuario encontrado...')

    return redirect('admindominio')
      
@login_admindominio
def adicionar_user(request):
    nome_user = request.POST.get('nome_user')
    id_admin = request.session.get('user_id')
    
    if nome_user == 'root':
        mensagem = "O nome ROOT nao pode ser definido para usuario"
        request.session['mensagem_info'] = mensagem

        return redirect('admindominio') 
    
    try:
        admdom = Usuario_BD.objects.filter(id=id_admin).first()
        dominio = admdom.email[5:]
    except:
        return redirect('logout')

    print(dominio)
    email_user = '{0}@{1}'.format(nome_user, dominio)
    
    if Usuario_BD.objects.filter(id_admin=id_admin, email=email_user, flag='U').exists():
        mensagem = "Este nome de usuario ja esta em uso!"
        request.session['mensagem_info'] = mensagem
        return redirect('admindominio')
    

    senha = random.randint(100000,999999)
    print(senha)
    try: 
        print('adicionando usuario')
        add_user = Usuario_BD()
        add_user.email = email_user
        add_user.id_admin = id_admin
        add_user.senha = make_password(senha)
        add_user.flag = 'U'
        add_user.save() 
    except Exception as err:
        print('Nao adicionou usuario', err)
        return redirect('logout')

    mensagem = "A senha do seu {0}@{1} e: {2}".format(nome_user, dominio, senha)
    request.session['mensagem_info'] = mensagem
    return redirect('admindominio')

# ======================================================================
''' FUNCOES DOS USUARIOS '''
# ======================================================================


@login_user
def PageUser(request):  
    mensagens = request.session.pop('mensagem_info', None)
    return render(request, 'user-dominio/painel.html', {'mensagens': mensagens})
