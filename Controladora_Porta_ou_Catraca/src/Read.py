#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
from datetime import datetime
import decimal
import time

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

# Welcome message
print " "
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# Váriáveis iniciais aod sistema

# setorMemoria=60
# Usado para definir qual parte da memória estará gravada a permissão de acesso
Agrupador = 0
# Define número de setores que serão reservados para dados genéricos
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
### ??? Renan 2015-11-29 - neste ponto deve ser inserida a chamada da funcao (calcula_Posicao_Memoria) que ira calcular o sertor da memoria (setorMemoria) onde esta gravada a permissao de acesso
        #(status, setorMemoria, byteMemoria) = calcula_Posicao_Memoria(Agrupador)
        #print "setorMemoria: " + setorMemoria+ "\n byteMemoria: " + byteMemoria
        
#--------- INICIO calculo para identificar setor e bloco onde está a permissão de acesso ---------------------------------------        
        # reescrever esse texto
    
        # Agrupador aponta para o inicicio da memorio logica onde deve estar gravada a permissao de acesso
        # Cada dia da semana ocupa 3 bytes, Dia da semana 0-SEG, 1-TER, 2-QUA, 3-QUI, 4-SEX, 5-SAB, 6-DOM 
        # Processo para definir byte a ser lido para a validacao da tag.
        ## Multiplica diaSemana por 3 e desloca esse valor em bytes
        ## Apos o deslocamento diaSemana com o hora desloca em bits
        #
        
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
        #---------------------------------------------------------------------------------------------
        ##João
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
### ??? Renan 2015-11-29 - idealmente a funcao acima deveria receber o bloco de memoria que deve ser realizada a leitura, lendo um setor e um bloco especifico. 
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, setorMemoria, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
### ??? Renan 2015-11-29 - inserir a funcao (MFRC522_Read_Memoria) que fara a validacao da permissao de acesso com base no setor e byte da memoria            
            retornoBackData = MIFAREReader.MFRC522_Read_Memoria(setorMemoria, byteMemoria, resto_deslocamento_horaAtual)
            print "return backData[byteMemoria]: " + str(retornoBackData) + " \n "
            #MIFAREReader.MFRC522_Read(setorMemoria)
            MIFAREReader.MFRC522_StopCrypto1()
            continue_reading = False
                    #Renan 2015-11-18 - Joao - Pega o bit 3 (quarto bit da direita para esquerda) e verifica se o resultado eh diferente de 0. Caso seja diferente de 0 eh pq esta OK, o bit analisado é 1.
            if (retornoBackData & (1 << resto_deslocamento_horaAtual)):
         
                # Chama a funcao para cionar a saida e passa os parametros para a abertura do dispositivo
                print " ------ Acesso Liberado ------ "

                saidaGPIO = 18
                tempoAcionamento = 2
                #acionador = acionador.acionarSaida()
                #MIFAREReader.MFRC522_Read_Memoria(setorMemoria)
                #acionador.acionarSaida(saidaGPIO, tempoAcionamento)
                GPIO.setmode(GPIO.BOARD)
                GPIO.setwarnings(False)
                GPIO.setup(saidaGPIO, GPIO.OUT)
                i = 1
                while(i):
                    print(" ------ LED ACESO ------ ")
                    GPIO.output(saidaGPIO, 1)
                    time.sleep(tempoAcionamento)
                    print(" ------ LED APAGADO ------ ")
                    GPIO.output(saidaGPIO, 0)
                    i=0
            else:  
                # Chama a funcao para acionar a saida e passa os parametros tudo zerado, para o broqueio do dispositivo.
                print " ------ Acesso Negado ------ "
    
        else:
            print "Authentication error"
        


## João
def calcula_Posicao_Memoria(signal, Agrupador):        
    print " "
    print "------------------------------------------------------------------------------------- "
    diaSemana = now.weekday()
    horaAtual = now.hour
    # Calculo do deslocamenta para valifação da permissão de acesso
    print "Read  - calcula_Posicao_Memoria -----------------------------------------------------------"
    print "Agrupador: " + str(Agrupador)
    print "diaSemana: "+ str(diaSemana)
    print "horaAtual: " +str( horaAtual)

    # Aponta para o inicido da permissão correspondente ao dia da semana
    deslocamento_diaSemana = diaSemana * 3
    deslocamento_horaAtual = horaAtual / 8
    resto_deslocamento_horaAtual =horaAtual % 8
    tamanhoPermissaoPorSemana = 21
#---------------------------------------------------------------------------------------------
    ##João
    byteMemoriaLogica = (Agrupador * tamanhoPermissaoPorSemana) + (deslocamento_diaSemana) + (deslocamento_horaAtual)
    setorMemoria = (byteMemoriaLogica / 16) +  (setoresReservados) + (byteMemoriaLogica / 48)
    byteMemoria = byteMemoriaLogica % 16  
### ??? inserir parte faltante da função para que ela retorne (return setorMemoria, byteMemoria) o setor e byte onde está a permissão necessária para validar.     
    print "Read  - calcula_Posicao_Memoria -----------------------------------------------------------"
    print "byteMemoriaLogica: "+str(byteMemoriaLogica)
    print "setorMemoria: " +setorMemoria + "byteMemoria: " + byteMemoria
        

    
 #---------------------------------------------------------------------------------------------           
        
