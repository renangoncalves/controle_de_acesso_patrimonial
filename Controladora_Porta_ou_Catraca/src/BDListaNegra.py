#!/usr/bin/env python
# -*- coding: utf8 -*-

import sqlite3
import BDConexao

class BDListaNegra(object):

    def __init__(self):
        print("BDListaNegra ___init___ -- Iniciando a classe BDLogAcesso.")
        self.conectaBD = BDConexao.BDConexao()

    def select(self, chave):
        print"BDListaNegra select -- Selecionando dados no BD."
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()
                
        sql = "SELECT * FROM ListaNegra WHERE chave=?"
        cursor.execute(sql, [(chave)])
        print cursor.fetchall()  # ou use fetchone()
        
        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()
    
    def select_all(self):
        print "BDListaNegra select_all -- Selecionando dados no BD."
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()
        
        sql = "SELECT * FROM ListaNegra"
        cursor.execute(sql)
        print cursor.fetchall()
        
        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()
    
    def insert(self, chave, statusChave):
        print "BDListaNegra insert -- Inserindo dados no BD."
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()
                
        #cursor.execute("""
        #    INSERT INTO ListaNegra (chave, chaveBloqueada)
        #    VALUES (?, ?)
        #""", (chave, statusChave))
        
        sql = "INSERT INTO ListaNegra (chave, chaveBloqueada) VALUES (?, ?)"
        cursor.execute(sql, (chave, statusChave))
        print cursor.fetchall()
        
        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()
        
    def update(self, chave):
        print("BDListaNegra update -- Atualizando os registros, chave bloqueada.")
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()
        
        # incluir o OBJETO BDConexão
        #cursor.execute("""
        #    UPDATE ListaNegra set chaveBloqueada = 'Sim' WHERE chave = ?
        #""", (chave))
        
        sql = "UPDATE ListaNegra SET ChaveBloqueada = 'Sim' WHERE chave=?"
        cursor.execute(sql, [(chave)])
        print cursor.fetchall()
       
        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()
        
    def delete(self, chave):
        print("BDListaNegra delete -- Apagando registros.")
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()
        

        sql = "DELETE FROM ListaNegra WHERE chave=?"
        cursor.execute(sql, [(chave)])
        print cursor.fetchall()
       
        #cursor.execute("""
        #    DELETE FROM ListaNegra WHERE chave = ?
        #""", (chave))
        #print cursor.fetchall()
        
        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()
        