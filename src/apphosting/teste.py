#!/usr/bin/python3
import os
nome_dominio = 'arco.mil'

comando = "python3 ../criar_dominio.py {0}".format(nome_dominio)
os.system(comando)
os.system("../exeroot")

