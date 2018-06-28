#!/usr/bin/env python
# -*- coding: utf8 -*-

import sqlite3
import BDConexao

class BDDispositivo(object):

    def __init__(self):
        self.debugRenan = False 
        if (self.debugRenan == True): print("BDDispositivo ___init___ -- Iniciando a classe BDDispositivo.")
        self.conectaBD = BDConexao.BDConexao()
    
    ##### REMOVER O INSERT NÃO SERÁ USADO
    def insert(self, IP, idAgrupador, idTipoDispositivo, IPServidor):
        if (self.debugRenan == True): print("BDDispositivo insert -- Inserindo dados no BD.")
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()
        # incluir o OBJETO BDConexão
        cursor.execute("""
            INSERT INTO Dispositivo (IP, idAgrupador, idTipoDispositivo, IPServidor)
            VALUES (?, ?, ?, ?)
        """, (IP, idAgrupador, idTipoDispositivo, IPServidor))
        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()
        
    def select(self):
        if (self.debugRenan == True): print("BDDispositivo select -- Selecionando registros.")
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()
        
        # incluir o OBJETO BDConexão
        cursor.execute("""
            SELECT * FROM Dispositivo
        """)
        if (self.debugRenan == True): print cursor.fetchall() 
        self.conectaBD.desconectar()
        #conn.commit()
        
    def update(self, IP, idAgrupador, idTipoDispositivo, IPServidor):
        if (self.debugRenan == True): print("BDDispositivo update -- Atualizando os registros.")
        self.conectaBD.conectar()
        cursor = self.conectaBD.conn.cursor()

        # incluir o OBJETO BDConexão
        cursor.execute("""
            UPDATE Dispositivo SET 
            IP = ?,
            idAgrupador = ?,
            idTipoDispositivo = ?,
            IPServidor = ?
        """, (IP, idAgrupador, idTipoDispositivo, IPServidor))
        self.conectaBD.conn.commit()
        self.conectaBD.desconectar()
        