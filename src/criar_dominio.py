#!/usr/bin/python3

import os
import sys


# ====================================================================

# pega o dominio pelos argumentos
dominio = sys.argv[1]

# Cria o caminho da pasta
pasta_destino = os.path.join("/projetoasa/users", dominio)

# cria a pasta do dominio e pasta do adm
try:
    os.makedirs(pasta_destino+"/adm", exist_ok=True)
except Exception as err:
    print('Erro na criacao das pastas', err)
# caminho da zona do dominio
caminho_zona = os.path.join(pasta_destino, "{}.zone".format(dominio))


# ====================================================================

# conteudo do dominio que vai no named.conf
conteudo_named = '''
zone "{0}" IN {{
    type master;
    file "{1}";
}};


'''.format(dominio, caminho_zona)

# adicionando a zona no named.conf
try:
    with open("/etc/named.conf.projeto", "a") as file:
        file.write(conteudo_named)
except Exception as err:
    print('Erro na adicao do named', err)

# ====================================================================

# criando o conteudo da zona
conteudo_zona = '''
$TTL 120
$ORIGIN {0}.

@       IN SOA @ root (
                1
                2H              
                30M            
                1W              
                10 )   

        IN A 192.168.102.128
        IN NS ns
        IN MX 0 mail

ns      IN A 192.168.102.128
www     IN A 192.168.102.128
ftp     IN CNAME www
mail    IN A 192.168.102.128



'''.format(dominio)


# adiciona o conteudo no arquivo de zona
try:
    with open(caminho_zona, "w") as file:
        file.write(conteudo_zona)
except Exception as err:
    print('Erro na adicao da zona', err)


#=================================================================


# criando o conteudo do arquivo HTTPD do apache
conteudo_apache = '''
<VirtualHost *:80>
       <Directory {0}/>
               AllowOverride all
               Require all Granted
	       Options Indexes
       </Directory>
       DocumentRoot "{1}/"
       ServerName {2}
       ServerAlias www.{3}
       ErrorLog "{4}/error.log"
       CustomLog "{5}/access.log" common
</VirtualHost>



'''.format(pasta_destino, pasta_destino, dominio, dominio, pasta_destino, pasta_destino)

# adiciona o conteudo no arquivo do httpd
try:
    with open("/etc/httpd/conf/httpd.conf.projeto", "a") as file:
        file.write(conteudo_apache)
except Exception as err:
    print('Erro na adicao do apache', err)

# ====================================================================
