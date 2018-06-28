#!/usr/bin/env python
# -*- coding: utf8 -*-
# http://wiki.python.org.br/SocketBasico
# http://stackoverflow.com/questions/23956353/convert-python-dict-to-json-string
# http://stackoverflow.com/questions/19483351/converting-json-string-to-dictionary-not-list-python

import socket
import thread
import json
import BDConexao
import BDLogAcesso
import BDDispositivo
import BDListaNegra

class SocketServidor(object):

    def __init__(self):
 
        #HOST = '172.18.131.75'
        HOST = "10.42.0.88"
        PORT = 5000            # Porta que o Servidor esta
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (HOST, PORT)
        tcp.bind(orig)
        tcp.listen(1)
        while True:
            con, cliente = tcp.accept()
            print 'Concetado por', cliente
            while True:
                msg = con.recv(1024)
                if not msg: break
                print cliente, msg
                msg_json = json.loads(msg)
                print 'Código da Função:  ' + str(msg_json['funcao'])
                self.defineOperacao(msg_json)
                #del self.defineOperacao              
            print 'Finalizando conexao do cliente', cliente
            con.close()
            
            
            
    def defineOperacao(self, msg_json):
        if   (msg_json['funcao'] == 1) : print "SocketCliente -- Config. Dispositivo.\n"
        elif (msg_json['funcao'] == 2) : self.insertListaNegra(msg_json)
        elif (msg_json['funcao'] == 3) : self.deletListaNegra(msg_json)
        elif (msg_json['funcao'] == 4) : self.LogAcesso(msg_json) 
        elif (msg_json['funcao'] == 5) : self.gravaPermissaoTag(msg_json)
        elif (msg_json['funcao'] == 10): self.finalizaThreadConexao()
        
        else: print '\n Função inexistente \n ', cliente

    
    def gravaPermissaoTag(self, msg_json):
        print "SocketCliente -- Gravar permissão de acesso.\n"
    
    def LogAcesso(self, msg_json):
# deveria retornar para o cliente a lista dos eventos
        print "SocketServidor -- LogAcesso."
        conectaBDLogAcesso = BDLogAcesso.BDLogAcesso()
        conectaBDLogAcesso.select(msg_json['dataInicio'], msg_json['dataFim'])


# Funções funcionando
    def insertListaNegra(self, msg_json):
        #if (msg_json['funcao'] == 2):    
        print "SocketServidor -- Insert ListaNegra."
        conectaBDListaNegra = BDListaNegra.BDListaNegra()
        conectaBDListaNegra.insert(msg_json['chave'], 'Nao')
        
    def deletListaNegra(self, msg_json):                    
        #if (msg_json['funcao'] == 3):    
        print "SocketServidor -- Delete ListaNegra."
        conectaBDListaNegra = BDListaNegra.BDListaNegra()
        conectaBDListaNegra.delete(msg_json['chave'])
        
    def finalizaThreadConexao(self):
        print "SocketCliente -- Finalizando Thread da conexão remota.\n"
        thread.exit()        
