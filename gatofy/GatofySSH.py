#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import paramiko, time, re

class gatofyMethods:
    
    def __init__(self):
        
        #SETANDO VARIAVEIS
        self.comInicial = '''\n'''''
        self.host = ""
        self.port = ""
        self.username = ""
        self.password = ""

    def find_between(self,  s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def find_between_r( self, s, first, last ):
        try:
            start = s.rindex( first ) + len( first )
            end = s.rindex( last, start )
            return s[start:end]
        except ValueError:
            return ""




    def getBloqueioStatus(self, imsiGet):
        host= self.host
        comInicial = self.comInicial
        port= self.port
        username= self.username
        password= self.password
        statusBloqueio = 0


        comGet = ''''''

        #CRIANDO SHELL EMULATOR
        
        client=paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port, username, password)
        channel = client.invoke_shell()
        out = channel.recv(9999)
        
        #CONECTANDO AO WEB SERVER

        channel.send(comInicial)
        while not channel.recv_ready():
            time.sleep(3)
        out = channel.recv(9999)
        saidaComandoInicial = out.decode("ascii")

        #COMANDO GET

        channel.send(comGet)
        while not channel.recv_ready():
            time.sleep(3)
        out = channel.recv(9999)
        saidaGet = out.decode("ascii")

        #ANALISANDO OUTPUTSTRING 
        valorAMBRMAXUL = self.find_between(saidaGet, 'AMBRMAXUL = ','\r')
        valorAMBRMAXDL = self.find_between(saidaGet, 'AMBRMAXDL = ', '\r')

        if valorAMBRMAXUL != '1':
            statusBloqueio = 0
            client.close()
            return statusBloqueio
        else:
            statusBloqueio = 1
            client.close()
            return statusBloqueio



    def bloquearImsi(self, imsiBloquear):
        
        host= self.host
        comInicial = self.comInicial
        port= self.port
        username= self.username
        password= self.password
        statusBloqueio = self.getBloqueioStatus(imsiBloquear)

        if statusBloqueio == 0:

            comBloqueio = ''' \n'''

            #ABRINDO CONEXÃO
            client=paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, port, username, password)


            #CRIANDO SHELL EMULATOR
            channel = client.invoke_shell()
            out = channel.recv(9999)

            #CONECTANDO AO WEB SERVER

            channel.send(comInicial)
            while not channel.recv_ready():
                time.sleep(3)
            out = channel.recv(9999)
            saidaComandoInicial = out.decode("ascii")

            #COMANDO BLOQUEIO

            channel.send(comBloqueio)
            while not channel.recv_ready():
                time.sleep(3)
            out = channel.recv(9999)
            saidaBloqueio = out.decode("ascii")

            if self.getBloqueioStatus(imsiBloquear) == 1:
                response = 'Bloqueado!'
                client.close()
                return response
            else:
                response = 'Não Bloqueado!'
                client.close()
                return response

        elif statusBloqueio == 1:
            response = 'Já Bloqueado!'
            return response

    def desbloquearImsi(self, imsiDesbloquear):
        
        host= self.host
        comInicial = self.comInicial
        port= self.port
        username= self.username
        password= self.password
        statusBloqueio = self.getBloqueioStatus(imsiDesbloquear)

        if statusBloqueio == 1:

            comDesbloqueio = '''\n'''

            #ABRINDO CONEXÃO
            client=paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host,port, username, password)


            #CRIANDO SHELL EMULATOR
            channel = client.invoke_shell()
            out = channel.recv(9999)

            #CONECTANDO AO WEB SERVER

            channel.send(comInicial)
            while not channel.recv_ready():
                time.sleep(3)
            out = channel.recv(9999)
            saidaComandoInicial = out.decode("ascii")

            #COMANDO DESBLOQUEIO

            channel.send(comDesbloqueio)
            while not channel.recv_ready():
                time.sleep(3)
            out = channel.recv(9999)
            saidaBloqueio = out.decode("ascii")

            if self.getBloqueioStatus(imsiDesbloquear) == 1:
                response = 'Não Desbloqueado!'
                client.close()
                return response
            else:
                response = 'Desbloqueado!'
                client.close()
                return response

        elif statusBloqueio == 0:
            response = 'Já Desbloqueado!'
            return response

