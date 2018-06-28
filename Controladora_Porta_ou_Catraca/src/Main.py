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
import SocketServidor
import threading
import thread


'''Inicialização do sistema '''

print "\n \n Versão 0.4_Beta de 2016-03-22 - 19:44 \n \n" 
print "Desabilitado a conexão remota! \n\n  "

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

''' Obter caracteristicas dipositivo '''
#BDDispositivo.get
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
agrupador = 0
nomeDispositivo = 'Porta Principal'


''' Informações curinga'''
debugAllRenan = False
debugRenan = 1

now = datetime.now()
continue_reading = True
horaAtual = now.hour
diaSemana = now.weekday()
teste = True

        
''' Iniciando os objetos'''
saidaRelePorta = EntradaSaida.EntradaSaida(1, GPIO_RelePorta)
saidaReleAlarme = EntradaSaida.EntradaSaida(1, GPIO_ReleAlarme)
entradaBotao= EntradaSaida.EntradaSaida(0, GPIO_Botao)
entradaEmergencia = EntradaSaida.EntradaSaida(0, GPIO_Emergencia)
entradaSensorPorta = EntradaSaida.EntradaSaida(0, GPIO_SensorPorta)

verificaRFID = RFID.RFID(key)
conectaBDLogAcesso = BDLogAcesso.BDLogAcesso()
conectaBDDispositivo = BDDispositivo.BDDispositivo()

''' Definição dos tempode de acionamentos das saídas'''
tempoAcionamentoAlarme = 2
tempoAcionamentoRelePorta = 5    

def end_read(signal,frame):
        global continue_reading
        print "Ctrl+C captured, ending read."
        continue_reading = False
        #thread.join()
        GPIO.cleanup()
        # finalizar a thread, mas ainda não funciona 
        thread.exit()
        Socket.stop
        thread.exit()
        del Socket
        del threading
        Thread.stop()
        del conexaoSocket
   
'''Verifica estado da entrada de Emergência. '''
def callbackEmergencia(gpio_pin):
    if (debugAllRenan == True): print "\n Main -- Emergência Acionada, porta destravada!! "
    x = stadoPorta(1)
    if (debugAllRenan == True): print "callbackBotao", str(x) 
    conectaBDLogAcesso.insert(now.today(), '000000', 'Entrada Emergencia Acionado', nomeDispositivo)
    saidaReleAlarme.set()
    conectaBDLogAcesso.insert(now.today(), '000000', 'Saida de Alarme Acionado.', nomeDispositivo)
    saidaRelePorta.set()
    conectaBDLogAcesso.insert(now.today(), '000000', 'Porta Destravada', nomeDispositivo)

'''Verifica estado da entrada do botão emulador.'''    
def callbackBotao(gpio_pin):
    if (debugAllRenan == True): print "\n Main -- Porta aberta por botão emulador!! "
    x = stadoPorta(1)
    if (debugAllRenan == True): print "callbackBotao", str(x) 
    saidaReleAlarme.clear()
    conectaBDLogAcesso.insert(now.today(), '000000', 'Abertura Botao de Saida.', nomeDispositivo)
    saidaRelePorta.set_wait_clear(tempoAcionamentoRelePorta)
    x = stadoPorta(2)
    if (debugAllRenan == True): print "callbackBotao", str(EstadoPorta)

'''Verifica estado da entrada do sensor de porta. '''
def callbackSensorPorta (gpio_pin):
    xxx = stadoPorta(3)
    if (debugAllRenan == True): print "callbackBotao", str(xxx) 
 
    if (entradaSensorPorta.get() == 1) and ( xxx == False):
        if (debugAllRenan == True): print "\n Main -- Porta arrombada, alarme acionado!! "
        conectaBDLogAcesso.insert(now.today(), '000000', 'Porta Arrombada.', nomeDispositivo)
        saidaReleAlarme.set()
        conectaBDLogAcesso.insert(now.today(), '000000', 'Saida de Alarme Acionado.', nomeDispositivo)
        saidaRelePorta.clear()
        time.sleep(tempoAcionamentoRelePorta)
    else:
        if (debugAllRenan == True): print "Porta Aberta"  

def stadoPorta(operacao):
    global EstadoPorta
    
    if (operacao == 1):
        ''' Porta aberta Cartão ou Botão Saída '''
        EstadoPorta = True
        if (debugAllRenan == True): print "stadoPorta: 1", str(EstadoPorta)
        return EstadoPorta
    if (operacao == 2):
        '''Porta Fechada '''
        EstadoPorta = False
        if (debugAllRenan == True): print "stadoPorta: 2", str(EstadoPorta)
        return EstadoPorta
    if (operacao == 3):
        '''Consulta estado da porta '''
        if (debugAllRenan == True): print "stadoPorta: 3", str(EstadoPorta)
        return EstadoPorta
    else:
        EstadoPorta = False
    
    print "stadoPorta: ", str(EstadoPorta) 
       
def validacaoAcessoRFID():
        ''' Função igual ao teste 44 do TesteClasses  '''
        realizatesteEnquanto = True
        while realizatesteEnquanto == True:
            if (debugAllRenan == True): print "TesteClasses -- LOOP de Validação do Acesso e Registra evento no BD"
            ''' Zera as variáveis do sistema'''
            nomeDispositivo = 'Porta Principal'
            realizatesteEnquanto1 = 0
            resto_deslocamento_horaAtual = 0
            setorMemoria = 0
            posicaoByteMemoria = 0
            RFID_OK = False
            agrupador = 0
            diaSemana = now.weekday()
            horaAtual = now.hour
            '''Onde está gravada as informações genéricas do usuário (data expiração, nível acesso)'''
            setorMemoria1 = 4
            le_memoria = RFID.RFID(key)  

            '''Calcula posição memória para validar acesso'''
            (setorMemoria, posicaoByteMemoria, resto_deslocamento_horaAtual) = le_memoria.calc_setor_bloco(agrupador, diaSemana, horaAtual)

            valorByteMemoria = None
            memoria1 = None
            status = 2
        
            le_id = RFID.RFID(key)
            while status != 0: 
                (status, uidTag) = le_id.get_id()
                if (status == 0):
                    if (debugAllRenan == True) or (debugRenan == 1): print "Inicio Validação RFID: " + str(now.today())
                    if (debugAllRenan == True): print "TesteClasses -- UID: "+str(uidTag[0])+","+str(uidTag[1])+","+str(uidTag[2])+","+str(uidTag[3])
                    while valorByteMemoria == None:
                        valorByteMemoria = le_memoria.read_byte(setorMemoria, posicaoByteMemoria)
                        if (valorByteMemoria != None):
                            if (debugAllRenan == True): print "TesteClasses read_setor -- Dados memória: "+ str(valorByteMemoria)
                            while memoria1 == None:
                                memoria1 = le_memoria.read_setor(setorMemoria1, status, uidTag)
                                if (realizatesteEnquanto1 == 3):
                                    memoria1 = "FF"
                                realizatesteEnquanto1 = realizatesteEnquanto1+1
                                if (debugAllRenan == True): print "TesteClasses read_setor -- Dados memória: "+ str(memoria1)
                                if (memoria1 != None) and (memoria1 != "FF"):             
                                    #Renan 2015-11-18 - Joao - Pega o bit 3 (quarto bit da direita para esquerda) e verifica se o resultado eh diferente de 0. Caso seja diferente de 0 eh pq esta OK, o bit analisado é 1.
                                    if (valorByteMemoria != None):
                                        if (debugAllRenan == True) or (debugRenan == 1): print "Fim validação RFID:    " + str(now.today())
                                        uidTag = str(uidTag[0])+str(uidTag[1])+str(uidTag[2])+str(uidTag[3])
                                        if (debugAllRenan == True) or (debugRenan == 1):print "uidTag: " + uidTag 
                                        '''Verifica se a chave está na lista negra '''
                                        conectaBDListaNegra = BDListaNegra.BDListaNegra()
                                        resultadoListaNegra = conectaBDListaNegra.select(uidTag)
                                        if (resultadoListaNegra != None):
                                            if (debugAllRenan == True) or (debugRenan == 1):print "Acesso negado, usuário bloqueado"
                                            conectaBDLogAcesso = BDLogAcesso.BDLogAcesso()
                                            conectaBDLogAcesso.insert(now.today(), str(uidTag), 'Negado, usuario da Lista Negra', nomeDispositivo)
                                            del conectaBDLogAcesso
                                        else:                                               
                                            '''Verifica validade permissão de acesso, Horário e validade da permissão (31/07/2016)'''    
                                            if (valorByteMemoria & (1 << resto_deslocamento_horaAtual)) and (memoria1[0] <= 16) and (memoria1[1] <= 07) and (memoria1[2] <= 31):
                                                if (debugAllRenan == True) or (debugRenan == 1): print "TesteClasses -- Porta Aberta!!"
                                                x = stadoPorta(1)
                                                saidaReleAlarme.clear()
                                                conectaBDLogAcesso = BDLogAcesso.BDLogAcesso()
                                                conectaBDLogAcesso.insert(now.today(), str(uidTag), 'Abertura Cartao MIFARE.', nomeDispositivo)
                                                RelePorta = EntradaSaida.EntradaSaida(1, 18)
                                                tempoAcionamento = 2
                                                RelePorta.set_wait_clear(tempoAcionamento)
                                                del conectaBDLogAcesso
                                            else:
                                                if (debugAllRenan == True) or (debugRenan == 1): print "TesteClasses -- Acesso Negado Porta Fechada!!"
                                                conectaBDLogAcesso = BDLogAcesso.BDLogAcesso()
                                                conectaBDLogAcesso.insert(now.today(), str(uidTag), 'Acesso Negado Cartao MIFARE.', nomeDispositivo)
                                                del conectaBDLogAcesso
                                        x = stadoPorta(2)
                        if (realizatesteEnquanto1 == 2):
                            valorByteMemoria = "FF"
                            uidTag = str(uidTag[0])+str(uidTag[1])+str(uidTag[2])+str(uidTag[3])
                            if (debugAllRenan == True) or (debugRenan == 1):print "Erro na validacao do acesso"
                            conectaBDLogAcesso = BDLogAcesso.BDLogAcesso()
                            conectaBDLogAcesso.insert(now.today(), str(uidTag), 'Erro na validacao do acesso', nomeDispositivo)
                            del conectaBDLogAcesso           
                        realizatesteEnquanto1 = realizatesteEnquanto1+1
                    del le_memoria
                    realizatesteEnquanto1 = realizatesteEnquanto1+1
                realizatesteEnquanto = False
                return realizatesteEnquanto
    
            realizatesteEnquanto = False
            return realizatesteEnquanto

            if (debugAllRenan == True) or (debugRenan == 1): print "\n \n"
            del le_id 
        realizatesteEnquanto = False
        return realizatesteEnquanto


def conexaoSocket(): 
    conectaTCP = SocketServidor.SocketServidor()

GPIO.add_event_detect(GPIO_Emergencia, GPIO.RISING, callback=callbackEmergencia, bouncetime = 500)
GPIO.add_event_detect(GPIO_Botao, GPIO.RISING, callback=callbackBotao, bouncetime = 500)
GPIO.add_event_detect(GPIO_SensorPorta, GPIO.RISING, callback=callbackSensorPorta, bouncetime = 500)

Socket = threading.Thread(name='Socket', target=conexaoSocket)
# quando executado assim ele fica presso aqui e não é possivel realizar a validação de tag
Socket.run()

# quando executado assim não finaliza só com o kill
#Socket.start()


while teste == True:
    
    validacaoAcessoRFID()
