#!/usr/bin/env python
# -*- coding: utf8 -*-
# http://wiki.python.org.br/SocketBasico
# http://stackoverflow.com/questions/23956353/convert-python-dict-to-json-string
# http://stackoverflow.com/questions/19483351/converting-json-string-to-dictionary-not-list-python

import socket
import json
import BDLogAcesso

HOST = '10.42.0.88'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
#tcp.connect(("10.42.0.88", 5000))
print 'Para sair use CTRL+X\n'
#msg = raw_input()
#-------- 2016-02-13 Json
continue_reading = True
while continue_reading:
    
    try:
        print "\n SocketCliente -- Selecione uma opção."
        print "0 - Encerrar conexão.              !!! OK !!!"
        print "1 - Config. Dispositivo."
        print "2 - Inserir cartão na ListaNegra.  !!! OK !!!"
        print "3 - Remover cartão da listaNegra.  !!! OK !!!"
        print "4 - Obter LogAcesso."
        print "5 - Gravar permissão de acesso."
        #print "6 - Recebe retorno do servidor."
        print "10 - Finalizando Thread de conexão remota do servidor."
        
        
        numeroFuncao=int(input("Insira o número correspondente a operação desejada: "))
        print "\n"
            
    except:
        print(" SocketCliente -- except -- Valor incorreto:  ")

    if (numeroFuncao == 5):
        print "SocketCliente -- Gravar permissão de acesso.\n"
        try: 
            print "\n \n"
            
            mensagemInsertListaNegra = dict()
            mensagemInsertListaNegra['funcao'] = numeroFuncao
            mensagemInsertListaNegra['permissao'] = int(input("Digite código da chave: "))
            
            print mensagemInsertListaNegra
            mensagemInsertListaNegra_str = json.dumps(mensagemInsertListaNegra)
            mensagemInsertListaNegra_str
            tcp.send (mensagemInsertListaNegra_str)
        except:
            print(" SocketCliente -- Inserir cartão na ListaNegra except-- Valor incorreto:  ")
    


























        
    if (numeroFuncao == 0):    
        print "SocketCliente -- Finalizar conexão."
        tcp.close()
        continue_reading = False

    if (numeroFuncao == 1):    
        print "SocketCliente -- Config Dispositivo."
        print "!!!!! Não Implementado !!!!!"

    if (numeroFuncao == 2):
        print "SocketCliente -- Inserir cartão na ListaNegra"
        try: 
            print "\n \n"
            mensagemInsertListaNegra = dict()
            mensagemInsertListaNegra['funcao'] = numeroFuncao
            mensagemInsertListaNegra['chave'] = int(input("Digite código da chave: "))
            #mensagemInsertListaNegra['inserir'] = int(input("Digite Sim para inserir Não para remover a chave: "))
            print mensagemInsertListaNegra
            mensagemInsertListaNegra_str = json.dumps(mensagemInsertListaNegra)
            mensagemInsertListaNegra_str
            tcp.send (mensagemInsertListaNegra_str)
        except:
            print(" SocketCliente -- Inserir cartão na ListaNegra except-- Valor incorreto:  ")
            
    if (numeroFuncao == 3):    
        print "SocketCliente -- Remover cartão da listaNegra.\n"
        try: 
            print "\n \n"
            mensagemDeleteListaNegra = dict()
            mensagemDeleteListaNegra['funcao'] = numeroFuncao
            mensagemDeleteListaNegra['chave'] = int(input("Digite código da chave: "))
            #mensagemInsertListaNegra['inserir'] = int(input("Digite Sim para inserir Não para remover a chave: "))
            print mensagemDeleteListaNegra
            mensagemDeleteListaNegra_str = json.dumps(mensagemDeleteListaNegra)
            mensagemDeleteListaNegra_str
            tcp.send (mensagemDeleteListaNegra_str)
        except:
            print(" SocketCliente -- Remove cartão na ListaNegra except-- Valor incorreto:  ")
    
    if (numeroFuncao == 4):    
        print "SocketCliente -- Obter LogAcesso.\n"
        print "!!!!! Não TESTADOOOOOOO !!!!!"
        #try: 
        conectaBDLogAcesso = BDLogAcesso.BDLogAcesso()

        mensagemLogAcesso = dict()
        mensagemLogAcesso['funcao'] = numeroFuncao
        dataHoraInicio = "2016-02-23 00:00:00.0000"
        dataHoraFim = "2016-02-23 23:59:59.9999"
        conectaBDLogAcesso.select(dataHoraInicio, dataHoraFim)

        #mensagemLogAcesso['dataInicio'] = int(input("Digite a data Inicio, seguindo o padrão (AAAA-MM-DD HH:MM:SS.mmmm) : "))
        #mensagemLogAcesso['dataFim'] = int(input("Digite a data Fim, seguindo o padrão (AAAA-MM-DD HH:MM:SS.mmmm) : "))
        print mensagemLogAcesso
        mensagemLogAcesso_str = json.dumps(mensagemLogAcesso)
        mensagemLogAcesso_str
        tcp.send (mensagemLogAcesso_str)
        #except:
        #    print(" SocketCliente -- except-- Valor incorreto:  ")
    
    if (numeroFuncao == 55):    
        print "SocketCliente -- Gravar permissão de acesso.\n"
        print "!!!!! Não Implementado !!!!!"
        try: 
            mensagemGravarPermissaoAcesso = dict()
            mensagemGravarPermissaoAcesso['funcao'] = numeroFuncao
            mensagemGravarPermissaoAcesso['numeroAgrupador'] = int(input("Digite o numero do agrupador: "))
            
            print "\n 1 - Horário comercial liberado das 7h até as 18h59" 
            print "2 - Tempo todo. \n"
            CodigoPermissaoAcesso['permissao'] = int(input("Digite o código da permissão: "))
            if (CodigoPermissaoAcesso == 1):
                mensagemGravarPermissaoAcesso = [128,255,07,128,255,07,128,255,15,128,255,15,128,255,15,128,255,15,128,255,15]
            elif (CodigoPermissaoAcesso == 2):
                mensagemGravarPermissaoAcesso = [255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255] 
            else:
                print "Erro, calor incorreto. "
                CodigoPermissaoAcesso = None
                
            if (CodigoPermissaoAcesso != None):               
                print mensagemGravarPermissaoAcesso
                mensagemGravarPermissaoAcesso_str = json.dumps(mensagemGravarPermissaoAcesso)
                print mensagemGravarPermissaoAcesso_str
                #tcp.send (mensagemGravarPermissaoAcesso_str)
            
            
            
            
            
            
            
            #print "Implementação pendente -- Nível do usuário e Validade da TAG"
            #print "Indicar ao usuário se foi liberada ou negada a solicitação de acesso;"
            #print "Monitorar estado da porta identificando aberta, fechada ou se houve um arrombamento;"
            #print "Registrar log dos acessos de entrada e saída dos usuários em cada um dos dispositivos;"
            #print "Segurança: Se houver comunicação em rede no sistema, esta deve ser segura;"
            #print "Sincronismo: Os eventos devem sem sincronizados com o servidor de modo transparente para o usuário;"
        except:
            print(" SocketCliente -- except-- Valor incorreto:  ")
    
        
        
        
    if (numeroFuncao == 6):    
        #print "SocketCliente -- Obter LogAcesso."
        print "!!!!! Não Implementado !!!!!"
        mensagemInsertListaNegra = dict()
        mensagemInsertListaNegra['funcao'] = numeroFuncao
        print mensagemInsertListaNegra
        mensagemInsertListaNegra_str = json.dumps(mensagemInsertListaNegra)
        mensagemInsertListaNegra_str
        tcp.send (mensagemInsertListaNegra_str)
        print "Teste 2016-02-16"



        
    if (numeroFuncao == 10):
        print "SocketCliente -- Finalizando Thread da conexão remota.\n"
        mensagemInsertListaNegra = dict()
        mensagemInsertListaNegra['funcao'] = numeroFuncao
        mensagemInsertListaNegra_str = json.dumps(mensagemInsertListaNegra)
        mensagemInsertListaNegra_str
        tcp.send (mensagemInsertListaNegra_str)
        tcp.close()
        continue_reading = False
#-------------- 2016-02-13 Json
