#!/usr/bin/env python
# -*- coding: utf8 -*-

import RFID
import BDConexao
import BDLogAcesso
import BDDispositivo
import BDListaNegra
import EntradaSaida
from datetime import datetime
import time
import RPi.GPIO as GPIO

#from _ast import Delete

'''Inicialização do sistema '''

print "\n \n Versão 0.2 de 2016-02-09 - 22:30 \n \n" 

''' Definição das GPIO'''
GPIO_RelePorta = 18
GPIO_ReleAlarme = 16
GPIO_Botao = 12
GPIO_Emergencia = 11
GPIO_SensorPorta = 36

'''
           BOARD -- BCM
IO      -- Pino  -- GPIO
LED VD  --  18   -- GPIO 24
LED VM  --  16   -- GPIO 23
Botao   --  12   -- GPIO 18
Chave 1 --  36   -- GPIO 16 
Chave 2 --  11   -- GPIO 17 
'''

''' Informações curinga'''
debug = True
now = datetime.now()
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
continue_reading = True
agrupador = 0
nomeDispositivo = 'Porta Principal'
horaAtual = now.hour
diaSemana = now.weekday()

        
''' Iniciando os objetos'''
saidaRelePorta = EntradaSaida.EntradaSaida(1, GPIO_RelePorta)
saidaReleAlarme = EntradaSaida.EntradaSaida(1, GPIO_ReleAlarme)
entradaBotao= EntradaSaida.EntradaSaida(0, GPIO_Botao)
entradaEmergencia = EntradaSaida.EntradaSaida(0, GPIO_Emergencia)
entradaSensorPorta = EntradaSaida.EntradaSaida(0, GPIO_SensorPorta)

verificaRFID = RFID.RFID(key)
conectaBDLogAcesso = BDLogAcesso.BDLogAcesso()


''' Definição dos tempode de acionamentos das saídas'''
tempoAcionamentoAlarme = 2
tempoAcionamentoRelePorta = 2        
# Capture SIGINT for cleanup when the script is aborted

def end_read(signal,frame):
        global continue_reading
        print "Ctrl+C captured, ending read."
        continue_reading = False
        GPIO.cleanup()

'''Verifica estado da entrada de Emergência. '''
def callbackEmergencia(gpio_pin):
    conectaBDLogAcesso.insert(now.today(), '000000', 'Entrada Emergencia Acionado', nomeDispositivo)
    saidaReleAlarme.set()
    conectaBDLogAcesso.insert(now.today(), '000000', 'Saida de Alarme Acionado.', nomeDispositivo)
    saidaRelePorta.set()
    conectaBDLogAcesso.insert(now.today(), '000000', 'Porta Destravada', nomeDispositivo)
    if (debug == True): print "\n Main -- Emergência Acionada, porta destravada!! "

'''Verifica estado da entrada do botão emulador.'''    
def callbackBotao(gpio_pin):
    saidaReleAlarme.clear()
    conectaBDLogAcesso.insert(now.today(), '000000', 'Abertura Botao de Saida.', nomeDispositivo)
    saidaRelePorta.set_wait_clear(tempoAcionamentoRelePorta)
    if (debug == True): print "\n Main -- Porta aberta por botão emulador!! "

'''Verifica estado da entrada do sensor de porta. '''
def callbackSensorPorta(gpio_pin):
    conectaBDLogAcesso.insert(now.today(), '000000', 'Porta Arrombada.', nomeDispositivo)
    saidaReleAlarme.set()
    conectaBDLogAcesso.insert(now.today(), '000000', 'Saida de Alarme Acionado.', nomeDispositivo)
    saidaRelePorta.clear()
    if (debug == True): print "\n Main -- Porta arrombada, alarme acionado!! "
   
     
GPIO.add_event_detect(GPIO_Emergencia, GPIO.RISING, callback=callbackEmergencia, bouncetime = 500)
GPIO.add_event_detect(GPIO_Botao, GPIO.RISING, callback=callbackBotao, bouncetime = 500)
GPIO.add_event_detect(GPIO_SensorPorta, GPIO.RISING, callback=callbackSensorPorta, bouncetime = 500)
if (debug == True): print "Main - Loop Principal do sistema de controle de acesso. "

while continue_reading:
      #try:
  
   #FinalizaMain=int(input("Insira o numero 0 para finalizar o teste: "))
   print '\n \n \n'
   
   ''' Zera as variáveis do sistema'''
   valorByteMemoria = 0
   resto_deslocamento_horaAtual = 0
   setorMemoria = 0
   posicaoByteMemoria = 0
   statusBotao = False
   RFID_OK = False
   
   ''' Verifica dia da semana e hora atual, calcula posição memória '''
   if (horaAtual != now.hour) or (diaSemana != now.weekday()):
       print horaAtual
       print diaSemana
       '''Calcula posição memória para validar acesso'''
       (setorMemoria, posicaoByteMemoria, resto_deslocamento_horaAtual) = verificaRFID.calc_setor_bloco(agrupador, diaSemana, horaAtual)
    
    
   '''Verifica se existe algum cartão para validar permissão de acesso. '''
   (status, uidTag) = verificaRFID.get_id()
   print status
   if (status == 0):
       print '   1   '
       if (debug == True): print "Main -- UID: "+str(uidTag[0])+","+str(uidTag[1])+","+str(uidTag[2])+","+str(uidTag[3])
       '''Captura o valor do byte correspondente ao diaSemana e Horário para validar o acesso'''
       print '   2   '
       valorByteMemoria = verificaRFID.read_byte(setorMemoria, posicaoByteMemoria)
       print '   3   '
       print valorByteMemoria
       print '   4   '
       '''Pega o bit 3 (quarto bit da direita para esquerda) e verifica se o resultado eh diferente de 0. Caso seja diferente de 0 eh pq esta OK, o bit analisado é 1.'''
       if (valorByteMemoria != None):
           print '   5   '
           if (valorByteMemoria & (1 << resto_deslocamento_horaAtual)):
               print '   6   '
               if (debug == True): print "Main -- Albre a Porta "
               conectaBDLogAcesso.insert(now.today(), uidTag, 'Abertura Cartao MIFARE.', nomeDispositivo)
               saidaRelePorta.set_wait_clear(tempoAcionamentoRelePorta)
           else:
               conectaBDLogAcesso.insert(now.today(), uidTag, 'Acesso Negado Cartão MIFARE.', nomeDispositivo)
               if (debug == True): print "Main -- Acesso Negado Cartão MIFARE!!"
       continualendo = False
    


    #except:
    #    print(" Main -- except valor incorreto:  ")
    #input()



    #if (FinalizaMain == 0):
    #    if (debug == True): print "Encerrando os testes: \n "
    #    continue_reading = False
    #else:
    #    if (debug == True): print "Principal -- Opção incorreta"
     