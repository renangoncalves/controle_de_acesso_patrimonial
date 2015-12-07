#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
from datetime import datetime
import decimal
import time
import EntradaSaida


continue_reading = True
now = datetime.now()

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
# variavel de retorno da função = objeto.função do objeto
RelePorta = EntradaSaida.EntradaSaida(1, 18)

# Welcome message
print " "
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

Agrupador = 0
setoresReservados = 8

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print " "
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
       
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

#--------- INICIO calculo para identificar setor e bloco onde está a permissão de acesso ---------------------------------------        
        
        diaSemana = now.weekday()
        horaAtual = now.hour
        # Calculo do deslocamenta para valifação da permissao de acesso
        print " "
        print " \n " + " -------------------- Read -------------------- " + " \n "
        print "Agrupador: " + str(Agrupador)
        print "diaSemana: "+ str(diaSemana)
        print "horaAtual: " +str( horaAtual)

        # Aponta para o inicido da permissao correspondente ao dia da semana
        deslocamento_diaSemana = diaSemana * 3
        deslocamento_horaAtual = horaAtual / 8
        resto_deslocamento_horaAtual =horaAtual % 8
        tamanhoPermissaoPorSemana = 21

        byteMemoriaLogica = (Agrupador * tamanhoPermissaoPorSemana) + (deslocamento_diaSemana) + (deslocamento_horaAtual)
        setorMemoria = (byteMemoriaLogica / 16) +  (setoresReservados) + (byteMemoriaLogica / 48)
        byteMemoria = byteMemoriaLogica % 16  
        print " "
        print "byteMemoriaLogica: "+str(byteMemoriaLogica)
        print "setorMemoria: "+str(setorMemoria)
        print "byteMemoria: "+str(byteMemoria)
        print "resto_deslocamento_horaAtual: " +str(resto_deslocamento_horaAtual) 
      
#--------- FIM ------------------------------------------------------------------------------------
        
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, setorMemoria, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            
            retornoBackData = MIFAREReader.MFRC522_Read_Memoria(setorMemoria, byteMemoria, resto_deslocamento_horaAtual)
            print "return backData[byteMemoria]: " + str(retornoBackData) + " \n "
            #MIFAREReader.MFRC522_Read(setorMemoria)
            MIFAREReader.MFRC522_StopCrypto1()
            continue_reading = False

            if (retornoBackData & (1 << resto_deslocamento_horaAtual)):
         
                # Chama a funcao para acionar a saida e passa os parametros para a abertura do dispositivo
                print " ------ Acesso Liberado ------ "
                tempoAcionamento = 2
                RelePorta.set_wait_clear(tempoAcionamento)
                
            else:  
                # Chama a funcao para acionar a saida e passa os parametros tudo zerado, para o broqueio do dispositivo.
                print " ------ Acesso Negado ------ "
    
        else:
            print "Authentication error"
        


  
