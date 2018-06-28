#!/usr/bin/env python
# -*- coding: utf8 -*-

import sqlite3
import BDConexao
from datetime import datetime

debugRenan = False
now = datetime.now()
nomeDispositivo = 'Principal'

if (debugRenan == True): print "CriarBD -- Criar banco de dados."
conectaBD = BDConexao.BDConexao()

if (debugRenan == True): print("CriarBD; ; Criando BD.")
#conn = sqlite3.connect('BDDispositivo.db')

conectaBD.conectar()
# definindo um cursor
cursor = conectaBD.conn.cursor()
        
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
conectaBD.conn.commit()
        
# criar tabelas padrão "ListaNegra"
cursor.execute("""
    CREATE TABLE ListaNegra (
        idListaNegra INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        chave VARCHAR(15) NOT NULL,
        chaveBloqueada VARCHAR(15) NOT NULL
        );    
""")
conectaBD.conn.commit()
         
#criar tabelas padrão "LogAcesso"
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
conectaBD.conn.commit()

if (debugRenan == True): print("CriarBD; ; Inserindo dados padrão do BD.")  
# inserindo dados na tabela Dispositivo
cursor.execute("""
    INSERT INTO Dispositivo (IP, idAgrupador, idTipoDispositivo, IPServidor, nomeDispositivo)
    VALUES (?, ?, ?, ?, ?)
    """, ('10.42.0.1', 0, 0, '10.42.0.88', nomeDispositivo))
conectaBD.conn.commit()
        
# inserindo dados na tabela ListaNegra
cursor.execute("""
    INSERT INTO ListaNegra (chave, chaveBloqueada)
    VALUES (?, ?)
    """, ('0123456789', 'Nao'))
conectaBD.conn.commit()
        
# inserindo dados na tabela LogAcesso
dataHora = now.today()
cursor.execute("""
    INSERT INTO LogAcesso (data, chavePessoa, tipoEvento, Dispositivo_idDispositivo, nomeDispositivo)
    VALUES (?, ?, ?, ?, ?)
    """, (dataHora, '000000', 'Banco de Dados Criado', 1, nomeDispositivo))
conectaBD.conn.commit()

if (debugRenan == True): print("CriarBD; ; Finalizada a criação do BD e inserção dos dados padrão.")

    