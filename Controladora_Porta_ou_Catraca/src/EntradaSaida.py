#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import time
from datetime import datetime

# Definicao da classe
class EntradaSaida:
    
    # Metodo construtor da classe
    def __init__(self, _modo, _pino):
        '''_modo = 0 >>  '''
        '''_modo = 1 >>  '''
        self.modo = _modo
        self.pino = _pino
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.pino, GPIO.OUT)
    
    # Declaracao de metodos   
    def set(self):
        '''escrever 1 no pino'''
        GPIO.output(self.pino, 1)

    def clear(self):
        '''escrever 0 no pino'''
        GPIO.output(self.pino, 0)
        
    def get(self):
        '''ler valor do pino'''
    
    #   define_espera_limpa
    def set_wait_clear(self, tempo):
        self.set()
        time.sleep(tempo)
        self.clear()
