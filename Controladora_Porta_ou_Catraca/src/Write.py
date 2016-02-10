#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

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

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Renan ---
    tipoTeste = 1
    setorMemoria = 8
    escreveValorMemoria = 0xFF
   
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
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

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, setorMemoria, key, uid)
        print "\n"
        
        # Renan -- Teste padrão do código exemplo
        if tipoTeste==0:
            # Check if authenticated
            if status == MIFAREReader.MI_OK:
    
                # Variable for the data to write
                data = []
    
                # Fill the data with 0xFF
                for x in range(0,16):
                    data.append(0xFF)
    
                print "Sector 8 looked like this:"
                # Read block 8
                MIFAREReader.MFRC522_Read(setorMemoria)
                print "\n"
    
                print "Sector 8 will now be filled with 0xFF:"
                # Write the data
                MIFAREReader.MFRC522_Write(setorMemoria, data)
                print "\n"
    
                print "It now looks like this:"
                # Check to see if it was written
                MIFAREReader.MFRC522_Read(setorMemoria)
                print "\n"
    
                data = []
                # Fill the data with 0x00
                for x in range(0,16):
                    data.append(0x00)
    
                print "Now we fill it with 0x00:"
                MIFAREReader.MFRC522_Write(setorMemoria, data)
                print "\n"
    
                print "It is now empty:"
                # Check to see if it was written
                MIFAREReader.MFRC522_Read(setorMemoria)
                print "\n"
    
                # Stop
                MIFAREReader.MFRC522_StopCrypto1()
    
                # Make sure to stop reading for cards
                continue_reading = False
            else:
                print "Authentication error"
        
# -----------------------------------------------------------------------------------------------        
        # RENAN -- Código para escrever uma permissão no bloco especifico 
        if tipoTeste == 1:
            
            # Check if authenticated
            if status == MIFAREReader.MI_OK:
    
                # Variable for the data to write
                #data = []
    
                # Fill the data with 0xFF
                #for x in range(0,16):
                #    data.append(escreveValorMemoria)
                
                # Renan 2015-11-30 - Gravar manualmente as permissao dos agrupadores 1 e 2
                permissao = 1
                if (permissao == 0):
                    #bloco 8
                    data1 = [128,255,15,128,255,15,128,255,15,128,255,15,128,255,15,128]
                    #bloco 9
                    data2 = [255,15,128,255,15,128,255,15,128,255,15,128,255,15,128,255]
                    #bloco 10
                    data3 = [15,128,255,15,128,255,15,128,255,15,0,0,0,0,0,0]
                
                if (permissao == 1):
                    #bloco 8
                    data1 = [255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255]
                    #bloco 9
                    data2 = [255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255]
                    #bloco 10
                    data3 = [255,255,255,255,255,255,255,255,255,255,0,0,0,0,0,0]
                 
                
                print "Sector 8 looked like this:"
                # Read block 8
                MIFAREReader.MFRC522_Read(setorMemoria)
                MIFAREReader.MFRC522_Read(setorMemoria+1)
                MIFAREReader.MFRC522_Read(setorMemoria+2)
                print "\n"
    
                print "Sector 8 will now be filled with 0xFF:"
                # Write the data
                MIFAREReader.MFRC522_Write(setorMemoria, data1)
                MIFAREReader.MFRC522_Write(setorMemoria+1, data2)
                MIFAREReader.MFRC522_Write(setorMemoria+2, data3)
                print "\n"
    
                print "It now looks like this:"
                # Check to see if it was written
                MIFAREReader.MFRC522_Read(setorMemoria)
                MIFAREReader.MFRC522_Read(setorMemoria+1)
                MIFAREReader.MFRC522_Read(setorMemoria+2)                
                print "\n"

                # Stop
                MIFAREReader.MFRC522_StopCrypto1()
    
                # Make sure to stop reading for cards
                continue_reading = False
            else:
                print "Authentication error"
# -----------------------------------------------------------------------------------------------
        
               