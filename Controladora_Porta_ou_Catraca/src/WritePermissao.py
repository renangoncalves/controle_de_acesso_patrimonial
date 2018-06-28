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
    setorMemoria = 4
   
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
                
# -----------------------------------------------------------------------------------------------        
        # RENAN -- Código para escrever uma permissão no bloco especifico 
            
        # Check if authenticated
        print str(MIFAREReader.MFRC522_Read(setorMemoria))
        
        data4 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        MIFAREReader.MFRC522_Write(4, data4)
        print str(MIFAREReader.MFRC522_Read(4))
                
 
        # Stop
        MIFAREReader.MFRC522_StopCrypto1()
    
        
               