#!/usr/bin/env python
# -*- coding: utf8 -*-

import RFID
import ConexaoBD
import EntradaSaida
from datetime import datetime
from time import sleep
#import Connect

print "\n \n Versão 2016-01-11 - 20:30 \n \n" 
now = datetime.now()
teste = 100
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
continue_reading = True

while continue_reading:
    
    try:
        print "\n \n \n \n \n"
        print "!!!BUG na função 8 - Grava a permissão na memória.\n"
        print "!!!BUG na função 9 - Quando não possui uma tag o sistema morre.\n"
        print "0 - Encerrar o teste."
        print "1 - Ler UID."
        print "2 - Saída rele."
        print "3 - Botão emulador."
        print "4 - Ler setor memória."
        print "5 - Ler byte memória."
        print "6 - Calcula posição de memória."
        print "7 - Grava setor"
        print "71 - Grava setor - permissão do agrupador 0"
        print "8 - Grava a permissão na memória."
        print "9 - LoopPrincipal -- monitora emulador e RFID."
        print " - Grava memória."
        
        teste=int(input("Insira o numero correspondente ao teste desejado: "))
            
    except:
        print(" Principal except-- Valor incorreto:  ")
    #input()



    if (teste == 0):
        print "Encerrando os testes: \n "
        continue_reading = False

    elif (teste == 1):
        print "\n \n Ler UID"
        le_id = RFID.RFID(key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF])
        (status, uidTag) = le_id.get_id()
        if (status == 0):
            print "Principal -- UID: "+str(uidTag[0])+","+str(uidTag[1])+","+str(uidTag[2])+","+str(uidTag[3])
        
    elif (teste == 2):
        print "Principal -- Saída rele"
        RelePorta = EntradaSaida.EntradaSaida(1, 18)
        tempoAcionamento = 2
        RelePorta.set_wait_clear(tempoAcionamento)
        print "Principal -- Saída rele, desligado"

    elif (teste == 3):
        print "Principal -- Botão emulador"
        
        bntEmulador = EntradaSaida.EntradaSaida(0, 12)
        stadoPino = bntEmulador.get()
        # ver esquema de ligação
        # http://blog.filipeflop.com/embarcados/projetos-com-raspberry-pi.html
        print stadoPino
        
        if (stadoPino == True):
            print "Principal -- Porta Aberta. \n"
            RelePorta = EntradaSaida.EntradaSaida(1, 18)
            tempoAcionamento = 2
            RelePorta.set_wait_clear(tempoAcionamento)
        else: 
            print "Principal -- Porta Fechada. \n"
    
    elif (teste == 4):        
        print "Principal -- Ler setor memória"
        
        try: 
            print "\n \n"
            setorMemoria=int(input("Digite o numero do setor desejado: "))
        except:
            print(" Principal -- Ler setor memória except-- Valor incorreto:  ")
        
        le_memoria = RFID.RFID(key)  
        memoria = le_memoria.read_setor(setorMemoria)
        print "Principal read_setor -- Dados memória: "+ str(memoria)
        
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
        print "Monitorando RFID e Botão Emulador"
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
     
    
    else:
        print "Principal -- Opção incorreta"
     