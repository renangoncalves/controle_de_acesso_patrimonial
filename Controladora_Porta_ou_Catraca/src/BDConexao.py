#!/usr/bin/env python
# -*- coding: utf8 -*-

#Referencia
# https://github.com/rg3915/python-sqlite
# http://pythonclub.com.br/gerenciando-banco-dados-sqlite3-python-parte1.html
# http://pythonclub.com.br/gerenciando-banco-dados-sqlite3-python-parte2.html
import sqlite3

class BDConexao(object):

    ''' A classe Connect representa o banco de dados. '''

    def __init__(self):
        print("BDConexão ___init___ -- Iniciando a classe BDConexao.")
        #conn = sqlite3.connect('BDDispositivo.db')
        
    def conectar(self):
        self.conn = sqlite3.connect('BDDispositivo.db')
        print("BDConexão conectar -- Conectado no banco de dados.")
        #criar verificação se realmente foi possível conectar no BD 
        
    def desconectar(self):
        self.conn.close()
        print("BDConexão desconectar -- Finalizada a conexão com o banco de dados.\n\n")
        #criar verificação se realmente foi possível conectar no BD
        
    def cria_Banco_Dados (self):
        print("BDConexão cria_Banco_Dados -- Criando as tabelas e inseri os dados padrão.")
        self.conectar()
        # definindo um cursor
        cursor = self.conn.cursor()
        # criar tabelas padrão
        cursor.execute("""
        CREATE TABLE Dispositivo (
            idDispositivo INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            IP VARCHAR(15) NOT NULL,
            idAgrupador INTEGER NOT NULL,
            idTipoDispositivo INTEGER NOT NULL,
            IPServidor VARCHAR(15) NOT NULL
            );    
        """)
        self.conn.commit()
        
        cursor.execute("""
        CREATE TABLE ListaNegra (
            idListaNegra INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            chave VARCHAR(15) NOT NULL,
            chaveBloqueada VARCHAR(15) NOT NULL
            );    
        """)
        self.conn.commit()
         
        cursor.execute("""
        CREATE TABLE LogAcesso (
            idLogAcesso INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            chavePessoa VARCHAR(15) NOT NULL,
            tipoEvento VARCHAR(30) NOT NULL,
            Dispositivo VARCHAR(15) NOT NULL
            );
        """)      
        self.conn.commit()
        
        # inserindo dados na tabela
        cursor.execute("""
            INSERT INTO Dispositivo (IP, idAgrupador, idTipoDispositivo, IPServidor)
            VALUES ('192.168.001.100', 0, 0, '192.168.001.001')
        """)
        self.conn.commit()
        
        cursor.execute("""
            INSERT INTO ListaNegra (chave, chaveBloqueada)
            VALUES ('123456', 'Nao')    
        """)
        self.conn.commit()
         