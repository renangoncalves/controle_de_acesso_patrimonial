#!/usr/bin/env python
# -*- coding: utf8 -*-

import MFRC522
import RPi.GPIO as GPIO
import MFRC522
import signal
import time


'''Definição da classe'''
class RFID:
    
    ''' Método construtor da classe'''
    def __init__(self, key):
        self.key = key
        self.rfid = MFRC522.MFRC522()
        self.setoresReservados = 8
        self.tamanhoPermissao = 21
        self.tamanhoSetor = 16  

    '''Declaracao de métodos'''
    def get_id(self):
        '''Pega UID do cartão'''
         
        (status,TagType) = self.rfid.MFRC522_Request(self.rfid.PICC_REQIDL)
        print "RFID.get_id -- MFRC522_Request:  " + str(status)
        (status, uid) = self.rfid.MFRC522_Anticoll()
        print "RFID.get_id -- MFRC522_Anticoll:  " + str(status)
        
        if status == self.rfid.MI_OK:
            print "\n RFID.get_id -- Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
        else:
            print "\n RFID.get_id -- Card NOT detected"
        return (status, uid)
    
    def read_setor(self, setorMemoria):
        
        # obtêm o UID da tag presente no leitor
        (status, self.uid) = self.get_id()
        
        if status == self.rfid.MI_OK:
            self.rfid.MFRC522_SelectTag(self.uid)
            # Realiza a autenticação no setor que deseja realizar a leitura dos dados 
            status = self.rfid.MFRC522_Auth(self.rfid.PICC_AUTHENT1A, setorMemoria, self.key, self.uid)
                        
            if status == self.rfid.MI_OK:
                # realiza a leitura do setor e blocos definidos
                retornoBackData = self.rfid.MFRC522_Read(setorMemoria)
                print "return backData[byteMemoria]: " + str(retornoBackData) + " \n "
                self.rfid.MFRC522_StopCrypto1()
                # Retorna o status e o valor do byte lido
                return retornoBackData
            else:
                print "Authentication error"
                
    def read_byte(self, setorMemoria, byteMemoria):
        
        # obtêm o UID da tag presente no leitor
        (status, self.uid) = self.get_id()
        
        if status == self.rfid.MI_OK:
            self.rfid.MFRC522_SelectTag(self.uid)
            # Realiza a autenticação no setor que deseja realizar a leitura dos dados 
            status = self.rfid.MFRC522_Auth(self.rfid.PICC_AUTHENT1A, setorMemoria, self.key, self.uid)
                        
            if status == self.rfid.MI_OK:
                # realiza a leitura do setor e blocos definidos
                retornoBackData = self.rfid.MFRC522_Read_Memoria(setorMemoria, byteMemoria)
                print "return backData[byteMemoria]: " + str(retornoBackData) + " \n "
                self.rfid.MFRC522_StopCrypto1()
                # Retorna o status e o valor do byte lido
                return retornoBackData
            else:
                print "Authentication error"
         
    def set_permissao (self, agrupador, permissao):
        print " RFID.set_permissao "
        resultadoGravacao = "erro"
        i=0         
        while i<21:
            # diaSemana sempre 0; horaAtual = i * 8 => 7 * 24 = 168 / 8 = 21
            print "i: " + str(i)
            diaSemana = 0
            horaAtual = i * 8
            (setorMemoria, byteMemoria, resto_deslocamento_horaAtual) = self.calc_setor_bloco(agrupador, diaSemana, horaAtual)
            
            memoriaAtual = self.read_setor(setorMemoria)
            print "\n memoriaAtual" + str(memoriaAtual)
            while byteMemoria < 16 and i < 21:
                memoriaAtual[byteMemoria] = permissao[i]
                print  "byteMemoria: " + str(byteMemoria) + " i: " + str(i)
                byteMemoria = byteMemoria + 1
                i = i + 1
            ''' 
            Descrição geral: 
                o for a seguir foi implementado para corrigir um bug sem explicação.
                quando tenta acessar os dados da tag por algum motivo na segunda tentativa da erro.
            Passo a passo do problema: 
                Obter o UID, obtêm os dados do setor desejado, processa o que deve ser gravado,
                quando manda gravar o sistema não consegue detectar a tag e da erro na operação. 
            Solução: quando manda gravar o dado na tag, manda executar ate 5x, provável que na segunda seja bem sucedida,
                caso não consiga em nenhuma das 5 o sistema vai dar erro.
            '''   
            for x in range(0,3):  
                resultadoGravacao = self.set_setor(setorMemoria, memoriaAtual)
                print 'RFID set_permissao -- resultadoGravacao: '+str(resultadoGravacao)
            # incluir no final do processo o status da operacao (OK ou ERRO) 
            #if i > 21:
            #    return resultadoGravacao
          
    def calc_setor_bloco(self, agrupador, diaSemana, horaAtual):                  
        # Calculo do deslocamento para verificar da permissão de acesso
        print " "
        print " \n " + " -------------------- Calc_Setor_Bloco -------------------- " + " \n "
        print "RFID calc_setor_bloco -- Agrupador: " + str(agrupador)
        print "RFID calc_setor_bloco -- diaSemana: "+ str(diaSemana)
        print "RFID calc_setor_bloco -- horaAtual: " +str( horaAtual)

        # Aponta para o ínicido da permissão correspondente ao dia da semana
        deslocamento_diaSemana = diaSemana * 3
        deslocamento_horaAtual = horaAtual / 8
        resto_deslocamento_horaAtual =horaAtual % 8
        tamanhoPermissaoPorSemana = 21

        byteMemoriaLogica = (agrupador * tamanhoPermissaoPorSemana) + (deslocamento_diaSemana) + (deslocamento_horaAtual)
        setorMemoria = (byteMemoriaLogica / 16) +  (self.setoresReservados) + (byteMemoriaLogica / 48)
        byteMemoria = byteMemoriaLogica % 16  
        print " "
        print "RFID calc_setor_bloco -- byteMemoriaLogica: "+str(byteMemoriaLogica)
        print "RFID calc_setor_bloco -- setorMemoria: "+str(setorMemoria)
        print "RFID calc_setor_bloco -- byteMemoria: "+str(byteMemoria)
        print "RFID calc_setor_bloco -- resto_deslocamento_horaAtual: " +str(resto_deslocamento_horaAtual) 
      
        print " \n " + " --------------------   FIM   Calc_Setor_Bloco -------------------- " + " \n "
        return (setorMemoria, byteMemoria, resto_deslocamento_horaAtual)
        
    def set_setor(self, setorMemoria, data):
        print " RFID.set_setor "
        
        print "RFID set_setor -- setorMemoria: " + str(setorMemoria)
        print "RFID set_setor -- data/memoriaAtual: " + str(data)
        
        # obtêm o UID da tag presente no leitor
        (status, self.uid) = self.get_id()
        
        if status == self.rfid.MI_OK:
           
            # Select the scanned tag
            self.rfid.MFRC522_SelectTag(self.uid)

            # Authenticate
            status = self.rfid.MFRC522_Auth(self.rfid.PICC_AUTHENT1A, setorMemoria, self.key, self.uid)
            print "\n"
               
            # Write the data
            self.rfid.MFRC522_Write(setorMemoria, data)
            # Stop
            self.rfid.MFRC522_StopCrypto1()
            return 'ok'
            # Make sure to stop reading for cards
        else:
            print "Authentication error"
            return 'erro'   
                 
    '''não esta sendo utilizado'''      
    def sync(self, uid, setorMemoria):
       
        '''conecta no cartão'''
        self.leMemoriaTag = MFRC522.MFRC522()

        
        # Select the scanned tag
        self.leMemoriaTag.MFRC522_SelectTag(uid)
           
        # Authenticate
        status = self.leMemoriaTag.MFRC522_Auth(self.leMemoriaTag.PICC_AUTHENT1A, setorMemoria, self.key, uid)
        print "return "
        return status
        print str(status)
   