#!/usr/bin/env python
# -*- coding: utf8 -*-

import RFID
import BDConexao
import BDLogAcesso
import BDDispositivo
import BDListaNegra
import EntradaSaida
from datetime import datetime
from time import sleep
#from duplicity.globals import select
from _ast import Delete
#import Connect

print "\n \n Versão 2016-02-21 - 20:14 \n \n" 
now = datetime.now()
teste = 100
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
continue_reading = True
realizatesteEnquanto = 0
debugRenan = False

while continue_reading:
    realizatesteEnquanto = 0
    try:
        print "\n \n \n \n \n"
        print "0 - Encerrar o teste."
        print "1 - Ler UID."
        print "2 - Aciona saídas, RelePorta e ReleAlarme."
        print "3 - Verifica estado das entradas, Botão, SensorPorta e Emergência."
        print "4 - Ler setor memória."
        print "41 - Ler 2 setores da memória"
        print "42 - Validação do Acesso"
        print "43 - Validação do Acesso e Registra evento no BD"
        print "44 - LOOP de Validação do Acesso e Registra evento no BD"

        print "5 - Ler byte memória."
        print "6 - Calcula posição de memória."
        print "7 - Grava setor"
        print "71 - Grava setor - permissão do agrupador 0"
        print "8 - Grava a permissão na memória."
        print "9 - LoopPrincipal -- monitora emulador e RFID."
        print "10 - Conectar / Desconectar do banco de dados."
        print "11 - Criar banco de dados."
        print "12 - Tabela Dispositivo."
        print "13 - Tabela ListaNegra."
        print "14 - Tabela LogAcesso."
        print "15 - Chama o Main."
        print "\n"
        
        teste=int(input("Insira o numero correspondente ao teste desejado: "))
        print "\n"
            
    except:
        print(" TesteClasses - Except-- Valor incorreto:  ")
    #input()



    if (teste == 0):
        print "TesteClasses - Encerrando os testes: \n "
        continue_reading = False

    elif (teste == 1):
        while realizatesteEnquanto < 10:
            print "\n \n TesteClasses - Ler UID"
            le_id = RFID.RFID(key)
            (status, uidTag) = le_id.get_id()
            if (status == 0):
                print "TesteClasses -- UID: "+str(uidTag[0])+","+str(uidTag[1])+","+str(uidTag[2])+","+str(uidTag[3])
            realizatesteEnquanto = realizatesteEnquanto+1
            del le_id
                
    
    elif (teste == 2):
        while realizatesteEnquanto < 10:
            print "TesteClasses -- Aciona saídas, RelePorta e ReleAlarme. "
            RelePorta = EntradaSaida.EntradaSaida(1, 18)
            tempoAcionamento = 2
            RelePorta.set_wait_clear(tempoAcionamento)
            ReleAlarme = EntradaSaida.EntradaSaida(1, 16)
            tempoAcionamento = 2
            ReleAlarme.set_wait_clear(tempoAcionamento)
            print "TesteClasses -- Saída rele, desligado"
            realizatesteEnquanto = realizatesteEnquanto+1
            
            del RelePorta     
            del ReleAlarme

    elif (teste == 3):
        while realizatesteEnquanto < 10:
            print "TesteClasses -- Verifica estado das entradas, Botão, SensorPorta e Emergência."
            bntEmulador = EntradaSaida.EntradaSaida(0, 12)
            statusPinoBotao = bntEmulador.get()
            sensorPorta = EntradaSaida.EntradaSaida(0, 36)
            statusPinoSensor = bntEmulador.get()
            emergencia = EntradaSaida.EntradaSaida(0, 11)
            statusPinoEmergencia = bntEmulador.get()
            print statusPinoBotao
            print statusPinoSensor
            print statusPinoEmergencia
            realizatesteEnquanto = realizatesteEnquanto+1
            del bntEmulador
            del sensorPorta 
            del emergencia
    
    elif (teste == 4):
        while realizatesteEnquanto < 5:
            print "TesteClasses -- Ler setor memória"
            memoria = None
            status = 2
            try:
                print "\n \n"
                setorMemoria=int(input("Digite o numero do setor desejado: "))
                realizatesteEnquanto1 = 0
            except:
                print(" TesteClasses -- Ler setor memória except-- Valor incorreto:  ")
        
            le_id = RFID.RFID(key)
            while status != 0: 
                (status, uidTag) = le_id.get_id()
                if (status == 0):
                    print "TesteClasses -- UID: "+str(uidTag[0])+","+str(uidTag[1])+","+str(uidTag[2])+","+str(uidTag[3])
                    le_memoria = RFID.RFID(key)  
                    while memoria == None:
                        print "\n \n \n \n"
                        print status
                        print uidTag
                        memoria = le_memoria.read_setor(setorMemoria, status, uidTag)
                        print "TesteClasses read_setor -- Dados memória: "+ str(memoria)
                        if (realizatesteEnquanto1 == 10):
                            break
                        realizatesteEnquanto1 = realizatesteEnquanto1+1
                    del le_memoria
                elif (realizatesteEnquanto1 == 10):
                    break
                realizatesteEnquanto1 = realizatesteEnquanto1+1
            realizatesteEnquanto = realizatesteEnquanto+1
            del le_id
            
    elif (teste == 41):
        while realizatesteEnquanto < 5:
            print "TesteClasses -- Ler 2 vezes o setores da memória"
            memoria = None
            memoria1 = None
            status = 2
            setorMemoria1 = 4
            try:
                print "\n \n"
                setorMemoria=int(input("Digite o numero do setor desejado: "))
                realizatesteEnquanto1 = 0
                if (setorMemoria == 000):
                    break
            except:
                print(" TesteClasses -- Ler setor memória except-- Valor incorreto:  ")
        
            le_id = RFID.RFID(key)
            while status != 0: 
                (status, uidTag) = le_id.get_id()
                if (status == 0):
                    print "TesteClasses -- UID: "+str(uidTag[0])+","+str(uidTag[1])+","+str(uidTag[2])+","+str(uidTag[3])
                    le_memoria = RFID.RFID(key)  
                    while memoria == None:
                        print "\n \n \n \n"
                        print status
                        print uidTag
                        memoria = le_memoria.read_setor(setorMemoria, status, uidTag)
                        while memoria1 == None:
                            memoria1 = le_memoria.read_setor(setorMemoria1, status, uidTag)
                            if (realizatesteEnquanto1 == 10):
                                break
                            realizatesteEnquanto1 = realizatesteEnquanto1+1
                        print "TesteClasses read_setor -- Dados memória: "+ str(memoria)
                        print "TesteClasses read_setor -- Dados memória: "+ str(memoria1)
                        if (realizatesteEnquanto1 == 10):
                            break
                        realizatesteEnquanto1 = realizatesteEnquanto1+1
                    del le_memoria
                elif (realizatesteEnquanto1 == 10):
                    break
                realizatesteEnquanto1 = realizatesteEnquanto1+1
            realizatesteEnquanto = realizatesteEnquanto+1
            del le_id
    
    elif (teste == 42):
        while realizatesteEnquanto < 1:
            print "TesteClasses -- Validação do Acesso"
            ''' Zera as variáveis do sistema'''
            #valorByteMemoria = 0
            #retorno_uidTag = "Erro"
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
                print "\n \n \n \n"
                (status, uidTag) = le_id.get_id()
                print now.today()
                if (status == 0):
                    print "TesteClasses -- UID: "+str(uidTag[0])+","+str(uidTag[1])+","+str(uidTag[2])+","+str(uidTag[3])
                    while valorByteMemoria == None:
                        valorByteMemoria = le_memoria.read_byte(setorMemoria, posicaoByteMemoria)
                        if (valorByteMemoria != None):
                            print "TesteClasses read_setor -- Dados memória: "+ str(valorByteMemoria)
                            while memoria1 == None:
                                memoria1 = le_memoria.read_setor(setorMemoria1, status, uidTag)
                                if (realizatesteEnquanto1 == 3):
                                    memoria1 = "FF"
                                realizatesteEnquanto1 = realizatesteEnquanto1+1
                                print "TesteClasses read_setor -- Dados memória: "+ str(memoria1)
                                if (memoria1 != None) and (memoria1 != "FF"):             
                                    #Renan 2015-11-18 - Joao - Pega o bit 3 (quarto bit da direita para esquerda) e verifica se o resultado eh diferente de 0. Caso seja diferente de 0 eh pq esta OK, o bit analisado é 1.
                                    if (valorByteMemoria != None):
                                        print now.today()
                                        if (valorByteMemoria & (1 << resto_deslocamento_horaAtual)) and (memoria1[0] == 1):
                                            RFID_OK = True
                                            print "\n \n \n \n RFID_OK == True  "
                                                     
                                    if (RFID_OK == True):
                                        RelePorta = EntradaSaida.EntradaSaida(1, 18)
                                        tempoAcionamento = 2
                                        RelePorta.set_wait_clear(tempoAcionamento)
                                        #break
                                        print "TesteClasses -- UID: "+str(uidTag[0])+","+str(uidTag[1])+","+str(uidTag[2])+","+str(uidTag[3])
                                        print "\n \n \n \n Principal -- Porta Aberta!!  "
                            
                                    else:
                                        print "\n \n \n \n Principal -- Acesso Negado Porta Fechada!!  "
                                        print "TesteClasses -- UID: "+str(uidTag[0])+","+str(uidTag[1])+","+str(uidTag[2])+","+str(uidTag[3])
                        
                        if (realizatesteEnquanto1 == 2):
                            valorByteMemoria = "FF"
                        realizatesteEnquanto1 = realizatesteEnquanto1+1
                    del le_memoria
                    realizatesteEnquanto1 = realizatesteEnquanto1+1

                elif (realizatesteEnquanto == 5):
                    break
                print "TesteClasses - realizatesteEnquanto: " + str(realizatesteEnquanto)
                realizatesteEnquanto = realizatesteEnquanto+1
            del le_id        
    
    elif (teste == 43):
        while realizatesteEnquanto < 1:
            print "TesteClasses -- Validação do Acesso e Registra evento no BD"
            ''' Zera as variáveis do sistema'''
            #valorByteMemoria = 0
            #retorno_uidTag = "Erro"
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
                print "\n \n \n \n"
                (status, uidTag) = le_id.get_id()
                print now.today()
                if (status == 0):
                    if (debugRenan == True): print "TesteClasses -- UID: "+str(uidTag[0])+","+str(uidTag[1])+","+str(uidTag[2])+","+str(uidTag[3])
                    while valorByteMemoria == None:
                        valorByteMemoria = le_memoria.read_byte(setorMemoria, posicaoByteMemoria)
                        if (valorByteMemoria != None):
                            if (debugRenan == True): print "TesteClasses read_setor -- Dados memória: "+ str(valorByteMemoria)
                            while memoria1 == None:
                                memoria1 = le_memoria.read_setor(setorMemoria1, status, uidTag)
                                if (realizatesteEnquanto1 == 3):
                                    memoria1 = "FF"
                                realizatesteEnquanto1 = realizatesteEnquanto1+1
                                if (debugRenan == True): print "TesteClasses read_setor -- Dados memória: "+ str(memoria1)
                                if (memoria1 != None) and (memoria1 != "FF"):             
                                    #Renan 2015-11-18 - Joao - Pega o bit 3 (quarto bit da direita para esquerda) e verifica se o resultado eh diferente de 0. Caso seja diferente de 0 eh pq esta OK, o bit analisado é 1.
                                    if (valorByteMemoria != None):
                                        print now.today()
                                        uidTag = str(uidTag[0])+str(uidTag[1])+str(uidTag[2])+str(uidTag[3])
                                        if (valorByteMemoria & (1 << resto_deslocamento_horaAtual)) and (memoria1[0] == 1):
                                            conectaBDLogAcesso = BDLogAcesso.BDLogAcesso()
                                            conectaBDLogAcesso.insert(now.today(), str(uidTag), 'Abertura Cartao MIFARE.', nomeDispositivo)
                                            RelePorta = EntradaSaida.EntradaSaida(1, 18)
                                            tempoAcionamento = 2
                                            RelePorta.set_wait_clear(tempoAcionamento)
                                            if (debugRenan == True): print "\n \n \n \n TesteClasses -- Porta Aberta!!  "
                                            del conectaBDLogAcesso
                                        else:
                                            if (debugRenan == True): print "\n \n \n \n TesteClasses -- Acesso Negado Porta Fechada!!  "
                                            conectaBDLogAcesso = BDLogAcesso.BDLogAcesso()
                                            conectaBDLogAcesso.insert(now.today(), str(uidTag), 'Acesso Negado Cartao MIFARE.', nomeDispositivo)
                                            del conectaBDLogAcesso
                        
                        if (realizatesteEnquanto1 == 2):
                            valorByteMemoria = "FF"
                        realizatesteEnquanto1 = realizatesteEnquanto1+1
                    del le_memoria
                    realizatesteEnquanto1 = realizatesteEnquanto1+1

                elif (realizatesteEnquanto == 5):
                    break
                if (debugRenan == True): print "TesteClasses - realizatesteEnquanto: " + str(realizatesteEnquanto)
                realizatesteEnquanto = realizatesteEnquanto+1
            del le_id        

    
    elif (teste == 44):
        debugAllRenan = False
        debugRenan = 1
        
        ''' Função igual ao teste 44 do TesteClasses  '''
        realizatesteEnquanto = True
        while realizatesteEnquanto == True:
            if (debugAllRenan == True): print "TesteClasses -- LOOP de Validação do Acesso e Registra evento no BD"
            ''' Zera as variáveis do sistema'''
            #valorByteMemoria = 0
            #retorno_uidTag = "Erro"
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
                                        if (valorByteMemoria & (1 << resto_deslocamento_horaAtual)) and (memoria1[0] == 1):
                                            if (debugAllRenan == True) or (debugRenan == 1): print "TesteClasses -- Porta Aberta!! \n \n  "
                                            conectaBDLogAcesso = BDLogAcesso.BDLogAcesso()
                                            conectaBDLogAcesso.insert(now.today(), str(uidTag), 'Abertura Cartao MIFARE.', nomeDispositivo)
                                            RelePorta = EntradaSaida.EntradaSaida(1, 18)
                                            tempoAcionamento = 2
                                            RelePorta.set_wait_clear(tempoAcionamento)
                                            del conectaBDLogAcesso
                                        else:
                                            if (debugAllRenan == True) or (debugRenan == 1): print "TesteClasses -- Acesso Negado Porta Fechada!!  \n \n "
                                            conectaBDLogAcesso = BDLogAcesso.BDLogAcesso()
                                            conectaBDLogAcesso.insert(now.today(), str(uidTag), 'Acesso Negado Cartao MIFARE.', nomeDispositivo)
                                            del conectaBDLogAcesso
                        
                        if (realizatesteEnquanto1 == 2):
                            valorByteMemoria = "FF"
                        realizatesteEnquanto1 = realizatesteEnquanto1+1
                    del le_memoria
                    realizatesteEnquanto1 = realizatesteEnquanto1+1

                #elif (realizatesteEnquanto == 5):
                #    break
                #if (debugAllRenan == True): print "TesteClasses - realizatesteEnquanto: " + str(realizatesteEnquanto)
                #realizatesteEnquanto = realizatesteEnquanto+1
                #self.teste = self.teste + 1
                #print "TesteClasses - realizatesteEnquanto: " + str(self.teste)
            del le_id        

    elif (teste == 14):
        dataHora = now.today() 
        print "Principal -- Tabela LogAcesso." 
        print dataHora
        nomeDispositivo = 'Porta Principal'
        chave = '123456'
        dataHoraInicio  = "2016-02-25 00:00:00.0000"
        dataHoraFim     = "2016-02-25 23:59:59.9999"

        conectaBDLogAcesso = BDLogAcesso.BDLogAcesso()
        #conectaBDLogAcesso.insert(data, chavePessoa, tipoEvento, Dispositivo)
        conectaBDLogAcesso.insert(dataHora, chave, 'Acesso Liberado', nomeDispositivo)
        conectaBDLogAcesso.insert("2016-02-02 11:11:11.1111", '123456', 'Acesso Liberado', nomeDispositivo)
        conectaBDLogAcesso.select_all()
        conectaBDLogAcesso.select(dataHoraInicio, dataHoraFim)
        conectaBDLogAcesso.delete(dataHoraInicio, dataHoraFim)
        #conectaBDLogAcesso.insert(now.today(), '000000', 'Evento do Sistema', nomeDispositivo)
        conectaBDLogAcesso.insert(now.today(), '000000', 'Entrada Emergencia Acionado.', nomeDispositivo)
        conectaBDLogAcesso.select(dataHoraInicio, dataHoraFim)
        conectaBDLogAcesso.select_all()
        
    elif (teste == 13):
        print "TesteClasses -- Tabela ListaNegra."
        conectaBDListaNegra = BDListaNegra.BDListaNegra()
        
        #print '\n \n \n 1'
        #conectaBDListaNegra.select_all()
        #print '\n \n \n 2'
        #conectaBDListaNegra.insert('222222', 'Nao')
        #print '\n \n \n 3'
        #conectaBDListaNegra.select_all()
        #print '\n \n \n 3.5'
        #chave = '111111'
        resultadoListaNegra = conectaBDListaNegra.select('111111')
        if (resultadoListaNegra != None):
            print "Acesso negado!, usuário bloqueado"
            print resultadoListaNegra
        else:
            print "Alguma coisa!"

            
        #print '\n \n \n 4'
        #conectaBDListaNegra.update('222222')
        #print '\n \n \n 5'
        #conectaBDListaNegra.select('222222')
        #print '\n \n \n 6'
        #conectaBDListaNegra.delete('222222')
        #print '\n \n \n 7'
        #conectaBDListaNegra.select_all()
    
    elif (teste == 7):
        print "Principal -- Grava setor"
        try: 
            print "\n \n"
            setorMemoria = int(input("Digite o numero do setor: "))
        except:
            print(" Principal -- Grava setor except-- Valor incorreto:  ")
            
        gravaSetor = RFID.RFID(key)  
        data = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        i=0
        #resultadoGravacao = gravaSetor.set_setor(setorMemoria, data)
        for x in range(0,3):  
                gravaSetor.set_setor(setorMemoria, data)
        #print "Principal -- resultadoGravacao: " + str(resultadoGravacao)
        
    elif (teste == 71):
        print "Principal -- Grava setor - permissão do agrupador 0"
        
        setorMemoria = 8
           
        gravaSetor = RFID.RFID(key)  
        data = [128,255,15,128,255,15,128,255,15,128,255,15,128,255,15,128]
        gravaSetor.set_setor(setorMemoria, data)
        
        setorMemoria = 5   
        gravaSetor = RFID.RFID(key)  
        data = [255,15,128,255,15,5,6,7,8,9,10,11,12,13,14,15]
        gravaSetor.set_setor(setorMemoria, data)

    elif (teste == 72):
        print "Principal -- Validade da Tag"
        try: 
            print "\n \n"
            setorMemoria = int(input("Digite o numero do setor \"4\" : "))
        except:
            print(" Principal -- Grava setor except-- Valor incorreto:  ")
            
        gravaSetor = RFID.RFID(key)  
        data = [16,7,31,0,0,0,0,0,0,0,0,0,0,0,0,0]
        i=0
        resultadoGravacao = gravaSetor.set_setor(setorMemoria, data)
        print "Principal -- resultadoGravacao: " + str(resultadoGravacao)























































       

    elif (teste == 5):        
        print "Principal -- Ler byte memória"
        try: 
            print "\n \n"
            setorMemoria=int(input("Digite o numero do setor desejado: "))
            byteMemoria=int(input("Digite o numero do byte desejado: "))
            
        except:
            print(" Principal -- Ler setor/byte memória except-- Valor incorreto:  ")
            
        le_memoria = RFID.RFID(key)  
       
        memoria = le_memoria.read_byte(setorMemoria, byteMemoria)
        print "Principal read_byte -- Valor byte: "+ str(memoria)
    
   
    elif (teste == 6):   
        print "Principal -- Calcula posição memória"
        
        try: 
            print "\n \n"
            agrupador = int(input("Digite o numero do agrupador: "))
        except:
            print(" Principal -- Calcula posição memória except-- Valor incorreto:  ")
        
        
        diaSemana = now.weekday()
        horaAtual = now.hour

        defineInicioMemoriaAgrupador = RFID.RFID(key)
        (setorMemoria, byteMemoria, resto_deslocamento_horaAtual) = defineInicioMemoriaAgrupador.calc_setor_bloco(agrupador, diaSemana, horaAtual)
        print "Principal -- setorMemoria:  " + str(setorMemoria)
        print "Principal -- byteMemoria:  " + str(byteMemoria)
                
    elif (teste == 7):
        print "Principal -- Grava setor"
        try: 
            print "\n \n"
            setorMemoria = int(input("Digite o numero do setor: "))
        except:
            print(" Principal -- Grava setor except-- Valor incorreto:  ")
            
        gravaSetor = RFID.RFID(key)  
        data = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        i=0
        resultadoGravacao = gravaSetor.set_setor(setorMemoria, data)
        print "Principal -- resultadoGravacao: " + str(resultadoGravacao)
        
    elif (teste == 71):
        print "Principal -- Grava setor - permissão do agrupador 0"
        
        setorMemoria = 8   
        gravaSetor = RFID.RFID(key)  
        data = [128,255,15,128,255,15,128,255,15,128,255,15,128,255,15,128]
        gravaSetor.set_setor(setorMemoria, data)
        
        setorMemoria = 9   
        gravaSetor = RFID.RFID(key)  
        data = [255,15,128,255,15,5,6,7,8,9,10,11,12,13,14,15]
        gravaSetor.set_setor(setorMemoria, data)


    elif (teste == 8):
        print "Principal -- Grava permissão"        
        try: 
            print "\n \n"
            agrupador = int(input("Digite o numero do agrupador: "))
        except:
            print(" Princiapal -- Grava permissão except -- Valor incorreto:  ")
        
        #horário comercial
        #permissao = [128,255,15,128,255,15,128,255,15,128,255,15,128,255,15,128,255,15,128,255,15]
        #Tempo todo
        permissao = [255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255]
        
        setPermissao = RFID.RFID(key)
        resultadoGravacao = setPermissao.set_permissao(agrupador, permissao)
        print "Principal Grava Permissão -- resultadoGravacao:  " + str(resultadoGravacao) 
         # Bug quando manda gravar a permissão da erro mas se mandar gravar de maneira independente o setor funciona.
    
    elif (teste == 9):
        print "Principal -- Monitorando RFID e Botão Emulador"
        continualendo = True
        bntEmulador = EntradaSaida.EntradaSaida(0, 12)
        verificaRFID = RFID.RFID(key)
        agrupador = 0
            
        while continualendo:
            valorByteMemoria = 0
            
            resto_deslocamento_horaAtual = 0
            setorMemoria = 0
            posicaoByteMemoria = 0
            stadoPino = False
            
            RFID_OK = False
            horaAtual = now.hour
            diaSemana = now.weekday()
            
            '''Verifica se o botão emulador está pressionado'''                    
            stadoPino = bntEmulador.get()
            '''Calcula posição memória para validar acesso'''
            (setorMemoria, posicaoByteMemoria, resto_deslocamento_horaAtual) = verificaRFID.calc_setor_bloco(agrupador, diaSemana, horaAtual)
            '''Captura o valor do byte correspondente ao diaSemana e Horário para validar o acesso'''
            valorByteMemoria = verificaRFID.read_byte(setorMemoria, posicaoByteMemoria)
            print "Principal -- valorByteMemoria: " + str(valorByteMemoria)
            
            #Renan 2015-11-18 - Joao - Pega o bit 3 (quarto bit da direita para esquerda) e verifica se o resultado eh diferente de 0. Caso seja diferente de 0 eh pq esta OK, o bit analisado é 1.
            if (valorByteMemoria != None):
                if (valorByteMemoria & (1 << resto_deslocamento_horaAtual)):
                    RFID_OK = True
                    print "RFID_OK == True"
         
            if (stadoPino == True) or (RFID_OK == True):
                RelePorta = EntradaSaida.EntradaSaida(1, 18)
                tempoAcionamento = 2
                RelePorta.set_wait_clear(tempoAcionamento)
                print "Principal -- Porta Aberta!!"
            else:
                print "Principal -- Acesso Negado Porta Fechada!!"
            continualendo = False
            
    elif (teste == 91):
        print "Principal -- Monitorando RFID e Botão Emulador"
        continualendo = True
        agrupador = 0
            
        while continualendo:
            verificaRFID = RFID.RFID(key)
            valorByteMemoria = 0
            
            resto_deslocamento_horaAtual = 0
            setorMemoria = 0
            posicaoByteMemoria = 0
            
            RFID_OK = False
            horaAtual = now.hour
            diaSemana = now.weekday()

            '''Calcula posição memória para validar acesso'''
            (setorMemoria, posicaoByteMemoria, resto_deslocamento_horaAtual) = verificaRFID.calc_setor_bloco(agrupador, diaSemana, horaAtual)
            '''Captura o valor do byte correspondente ao diaSemana e Horário para validar o acesso'''
            valorByteMemoria = verificaRFID.read_byte(setorMemoria, posicaoByteMemoria)
            print "Principal -- valorByteMemoria: " 
            print valorByteMemoria
            
            #Renan 2015-11-18 - Joao - Pega o bit 3 (quarto bit da direita para esquerda) e verifica se o resultado eh diferente de 0. Caso seja diferente de 0 eh pq esta OK, o bit analisado é 1.
            if (valorByteMemoria != None):
                if (valorByteMemoria & (1 << resto_deslocamento_horaAtual)):
                    RFID_OK = True
                    print "RFID_OK == True"
         
            if (RFID_OK == True):
                RelePorta = EntradaSaida.EntradaSaida(1, 18)
                tempoAcionamento = 2
                RelePorta.set_wait_clear(tempoAcionamento)
                print "Principal -- Porta Aberta!!"
            else:
                print "Principal -- Acesso Negado Porta Fechada!!"
            continualendo = True
     
    elif (teste == 10):
        print "Principal -- Conectar / Desconectar do banco de dados."
        conectaBD = BDConexao.BDConexao()
        conectaBD.conectar()
        sleep(1)
        conectaBD.desconectar()


    elif (teste == 11):
        print "Principal -- Criar banco de dados."
        conectaBD = BDConexao.BDConexao()
        conectaBD.cria_Banco_Dados()
        
    elif (teste == 12):
        print "Principal -- Tabela Dispositivo."
        conectaBDDispositivo = BDDispositivo.BDDispositivo()
        conectaBDDispositivo.select()
        conectaBDDispositivo.update('010.000.000.100', 1, 1, '010.000.000.001')
        conectaBDDispositivo.select()
        conectaBDDispositivo.update('192.168.001.100', 1, 1, '192.168.001.001')
        conectaBDDispositivo.select()
        
            

    elif (teste == 15):
        print "Principal -- Chama o Main." 
    
    else:
        print "Principal -- Opção incorreta"
   
    