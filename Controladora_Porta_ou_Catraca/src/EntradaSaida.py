#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import time
from datetime import datetime

# Definição da classe
class EntradaSaida:
    
    # Método construtor da classe
    def __init__(self, _modo, _pino):
        '''_modo = 0 >>  pino eh de entrada'''
        '''_modo = 1 >>  pino eh de saída'''
        self.modo = _modo
        self.pino = _pino
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        if (_modo == 0):
            GPIO.setup(self.pino, GPIO.IN)
        else:
            GPIO.setup(self.pino, GPIO.OUT)
    
    # Declaração de métodos   
    def set(self):
        '''escrever 1 no pino'''
        GPIO.output(self.pino, 1)

    def clear(self):
        '''escrever 0 no pino'''
        GPIO.output(self.pino, 0)
        
    def get(self):
        '''ler valor do pino'''
        estadoPino = GPIO.input(self.pino)
        return estadoPino
    
    #   define_espera_limpa
    def set_wait_clear(self, tempo):
        self.set()
        time.sleep(tempo)
        self.clear()
