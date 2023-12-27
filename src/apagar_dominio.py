#!/usr/bin/python3
import os
import sys


#=====================================================================

# pega o dominio dos argumentos
dominio_apagar = sys.argv[1]

# apaga as pastas e arquivos de FTP, ZONA, HTACESS, WEB
os.system("rm -rf /projetoasa/users/{0}".format(dominio_apagar))

#=====================================================================

# Realiza a retirada do dominio do arquivo HTTPD do apache
cont = 0

# abro o arquivo Httpd.conf.projeto com o modo r+ 
with open("/etc/httpd/conf/httpd.conf.projeto", "r+") as httpd_file:

    # leio todas as linhas e a salvo em uma lista
    linhas = httpd_file.readlines()
    for linha in linhas:
        
        # viajo cada linha, ate achar onde inicia o virtualhost daquele dominio
        if dominio_apagar in linha:
            break
        cont += 1
    
    # ao final ja com a linha referente, eu subtraio - 1 (pois pego a linha do inicio do virtualhost)
    inicio_apagar = cont - 1

    # o final e apos 11 linhas da linha inicial, padrao
    fim_apagar = cont + 11

    # apago da lista, esse intervalo de linhas
    del linhas[inicio_apagar:fim_apagar]

    # retorno a linha 0 do arquivo 
    httpd_file.seek(0)

    # faco o truncate para ajustar o tamanho e garantir que foi apagado 
    # e salvo a lista (sem o virtualhost) em cima do arquivo original
    httpd_file.truncate()
    httpd_file.writelines(linhas)
    
#=====================================================================

# neste realizo quase o mesmo procedimento mas para o named.conf
cont = 0

with open("/etc/named.conf.projeto", "r+") as named_file:
    linhas = named_file.readlines()

    for linha in linhas:

        if dominio_apagar in linha:
            break
        cont += 1

    inicio_apagar = cont
    fim_apagar = cont + 4

    del linhas[inicio_apagar:fim_apagar]
        
    named_file.seek(0)
    named_file.truncate()

    named_file.writelines(linhas)

#=====================================================================
