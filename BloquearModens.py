import pandas as pd, paramiko, os, mysql.connector, time, sys
from datetime import datetime, timedelta
from control_methods import ControlMethods
from mysql_services import mysqlConns
from GatofySSH import gatofyMethods

#===============================================================================================================
#SETANDO DATAS
tempo = datetime.now() - timedelta()
dataBanco = tempo.strftime('%Y-%m-%d %H:%M:%S')
dataLog = tempo.strftime('%Y-%m-%d_%H-%M-%S')

#VARIAVEIS DE DIRETORIO DE NOMES
padraoLog = '\n'+dataLog+'||log||gatofy_bloqueio||'

#===============================================================================================================
#QUERY BANCO NOC
query = '''select id_modem, nuImsi, dtBloqueioModem, id_status from modem where id_status = 5;'''

#===============================================================================================================
#INSTANCIANDO CLASSES A UTILIZAR
conn = mysqlConns()
gatofy = gatofyMethods()
meth = ControlMethods(padraoLog)

#===============================================================================================================
#ABRINDO CONEXÕES COM BANCO DE DADOS
try:
    connNoc = conn.open_connection_noc()
    engineNoc = conn.engine_create()

except:
    print('Falha na conexão ao Banco de Dados!!!')
    sys.exit()
    
#Buscando MODENS A BLOQUEAR no BANCO DO NOC e testando conexão com o Banco
try:
    dfNoc = pd.read_sql(query, con=connNoc).astype(str)
    print('Logando no BANCO DO NOC, extraindo Query!')
    
except:
    print('Falha ao Acessar o BANCO DO NOC! Encerrando o Script!')


#=======================================================================================================================
#BLOQUEANDO MODENS

dfBloqueios = dfNoc.copy()

if dfBloqueios.empty:
        print('Não há modens para bloqueio')
        
else:

    #FOR PARA BLOQUEAR MODENS
    count = 0

    for i in dfBloqueios.itertuples():


            dfConcatenar = dfBloqueios.copy()
            dfConcatenar = dfConcatenar.loc[(dfConcatenar['nuImsi'] == i.nuImsi)]
            
            print('Realizando bloqueio em: ' + str(i.nuImsi) + ' Contagem em:' + str(count))
            count = int(count) + 1
            
            try:
            
                response = gatofy.bloquearImsi(i.nuImsi)
                print(response)
            
            except:
                print('Não foi possível realizar o BLOQUEIO DOS MODENS')

                
#=======================================================================================================================            
#ATUALIZAR BLOQUEADOS NO BANCO

if dfNoc.empty:
    print('Não houve modens gerados para bloqueio')
else:
    dfNoc = dfNoc[['id_modem']]
    bloqueioLista = dfNoc['id_modem'].to_list()
    bloqueioTupla = meth.convert(bloqueioLista)
    
    try:
        #ATUALIZANDO BLOQUEIOS
        cursor = connNoc.cursor()
        cursor.execute('''UPDATE modem SET id_status = 3, dtBloqueioModem = "'''+dataBanco+'''" WHERE id_modem IN'''+bloqueioTupla+''';''')
        connNoc.commit()
        print('Realizada atualização no banco')

    except:
        the_type, the_value, the_traceback = sys.exc_info()
        erro = 'Falha na execução de update de modens BLOQUEADOS!!'
        meth.write_log(padraoLog + erro)
        print(the_type, ',' ,the_value,',', the_traceback)
                
                