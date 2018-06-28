#!/usr/bin/env python
# -*- coding: utf8 -*-

import sqlite3
import BDConexao

class BDLogAcesso(object):

    def __init__(self):
        self.debugRenan = False 
        if (self.debugRenan == True): print("BDLogAcesso ___init___ -- Iniciando a classe BDLogAcesso.")
        self.conectaBD = BDConexao.BDConexao()
        
    def insert(self, data, chavePessoa, tipoEvento, Dispositivo):
        if (self.debugRenan == True): print("BDLogAcesso insert -- Inserindo dados no BD.")
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()

        cursor.execute("""
            INSERT INTO LogAcesso (data, chavePessoa, tipoEvento, Dispositivo)
            VALUES (?, ?, ?, ?)
        """, (data, chavePessoa, tipoEvento, Dispositivo))
        if (self.debugRenan == True): print cursor.fetchall()

        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()
         
    def select_all(self):
        self.debugRenan = True
        if (self.debugRenan == True): print("BDLogAcesso select_all -- Selecionando registros.")
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()

        cursor.execute("""
            SELECT * FROM LogAcesso
        """)
        if (self.debugRenan == True): print cursor.fetchall()

        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()
               
    def select(self, dataHoraInicio, dataHoraFim):
        if (self.debugRenan == True): print("BDLogAcesso select -- Selecionando registros.")
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()

        cursor.execute("""
            SELECT * FROM LogAcesso WHERE data between ? and ?
            """, (dataHoraInicio, dataHoraFim))
        if (self.debugRenan == True): print cursor.fetchall()
        
        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()

    def delete(self, dataHoraInicio, dataHoraFim):
        if (self.debugRenan == True): print("BDLogAcesso delete -- Apagando registros.")
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()
        
        cursor.execute("""
            DELETE FROM LogAcesso WHERE data between ? and ?
        """, (dataHoraInicio, dataHoraFim))
        if (self.debugRenan == True): print cursor.fetchall()

        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()
        
