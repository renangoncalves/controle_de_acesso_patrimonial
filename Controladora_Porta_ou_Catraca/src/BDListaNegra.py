#!/usr/bin/env python
# -*- coding: utf8 -*-

import sqlite3
import BDConexao


class BDListaNegra(object):

    def __init__(self):
        self.debugRenan = False
        if (self.debugRenan == True): print("BDListaNegra ___init___ -- Iniciando a classe BDLogAcesso.")
        self.conectaBD = BDConexao.BDConexao()

    def select(self, chave):
        resultadoListaNegra = None
        if (self.debugRenan == True): print"BDListaNegra select -- Selecionando dados no BD."
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()
                
        sql = "SELECT chave FROM ListaNegra WHERE chave=?"
        #cursor.execute(sql, [(chave)])
        for resultadoListaNegra in cursor.execute(sql, [(chave)]):
            print resultadoListaNegra 

        if (self.debugRenan == True): print cursor.fetchall()  # ou use fetchone()
                
        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()
        return resultadoListaNegra
        
    def insert(self, chave, statusChave):
        if (self.debugRenan == True): print "BDListaNegra insert -- Inserindo dados no BD."
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()
                
        #cursor.execute("""
        #    INSERT INTO ListaNegra (chave, chaveBloqueada)
        #    VALUES (?, ?)
        #""", (chave, statusChave))
        
        sql = "INSERT INTO ListaNegra (chave, chaveBloqueada) VALUES (?, ?)"
        cursor.execute(sql, (chave, statusChave))
        if (self.debugRenan == True): print cursor.fetchall()
        
        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()
        
    def update(self, chave):
        if (self.debugRenan == True): print("BDListaNegra update -- Atualizando os registros, chave bloqueada.")
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()
        
        # incluir o OBJETO BDConexão
        #cursor.execute("""
        #    UPDATE ListaNegra set chaveBloqueada = 'Sim' WHERE chave = ?
        #""", (chave))
        
        sql = "UPDATE ListaNegra SET ChaveBloqueada = 'Sim' WHERE chave=?"
        cursor.execute(sql, [(chave)])
        if (self.debugRenan == True): print cursor.fetchall()
       
        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()
        
    def delete(self, chave):
        if (self.debugRenan == True): print("BDListaNegra delete -- Apagando registros.")
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()
        

        sql = "DELETE FROM ListaNegra WHERE chave=?"
        cursor.execute(sql, [(chave)])
        if (self.debugRenan == True): print cursor.fetchall()
       
        #cursor.execute("""
        #    DELETE FROM ListaNegra WHERE chave = ?
        #""", (chave))
        #print cursor.fetchall()
        
        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()
        