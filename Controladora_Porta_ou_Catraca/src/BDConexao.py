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
        self.debugRenan = False
        if (self.debugRenan == True): print("BDConexão ___init___ -- Iniciando a classe BDConexao.")
        #conn = sqlite3.connect('BDDispositivo.db')
        
    def conectar(self):
        self.conn = sqlite3.connect('BDDispositivo.db')
        if (self.debugRenan == True): print("BDConexão conectar -- Conectado no banco de dados.")
        #criar verificação se realmente foi possível conectar no BD 
        
    def desconectar(self):
        self.conn.close()
        if (self.debugRenan == True): print("BDConexão desconectar -- Finalizada a conexão com o banco de dados.\n\n")
        #criar verificação se realmente foi possível conectar no BD
        
    def cria_Banco_Dados (self):
        if (self.debugRenan == True): print("BDConexão cria_Banco_Dados -- Criando as tabelas e inseri os dados padrão.")
        self.conectar()
        # definindo um cursor
        cursor = self.conn.cursor()
        
        # criar tabelas padrão "Dispositivo"
        cursor.execute("""
        CREATE TABLE Dispositivo (
            idDispositivo INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            IP VARCHAR(15) NOT NULL,
            idAgrupador INTEGER NOT NULL,
            idTipoDispositivo INTEGER NOT NULL,
            IPServidor VARCHAR(15) NOT NULL,
            nomeDispositivo VARCHAR(45) NOT NULL
            );    
        """)
        self.conn.commit()
        
        # criar tabelas padrão "ListaNegra"
        cursor.execute("""
        CREATE TABLE ListaNegra (
            idListaNegra INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            chave VARCHAR(15) NOT NULL,
            chaveBloqueada VARCHAR(15) NOT NULL
            );    
        """)
        self.conn.commit()
         
        # criar tabelas padrão "LogAcesso"
        cursor.execute("""
        CREATE TABLE LogAcesso (
            idLogAcesso INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            chavePessoa VARCHAR(15) NOT NULL,
            tipoEvento VARCHAR(30) NOT NULL,
            Dispositivo_idDispositivo INTEGER NOT NULL,
            nomeDispositivo VARCHAR(45) NOT NULL
            );
        """)      
        self.conn.commit()
        
        # inserindo dados na tabela Dispositivo
        cursor.execute("""
            INSERT INTO Dispositivo (IP, idAgrupador, idTipoDispositivo, IPServidor, nomeDispositivo)
            VALUES ('192.168.001.100', 0, 0, '192.168.001.001', 'Principal')
        """)
        self.conn.commit()
        
        # inserindo dados na tabela ListaNegra
        cursor.execute("""
            INSERT INTO ListaNegra (chave, chaveBloqueada)
            VALUES ('0123456789', 'Não')
        """)
        self.conn.commit()
        
        # inserindo dados na tabela LogAcesso
        cursor.execute("""
            INSERT INTO LogAcesso (data, chavePessoa, tipoEvento, Dispositivo_idDispositivo, nomeDispositivo)
            VALUES (2016-03-08 23:28:22.000000, 0, 0, 1, 'Principal')
        """)
        self.conn.commit()
        
         