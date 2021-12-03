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
padraoLog = '\n'+dataLog+'||log||gatofy_desbloqueio||'

#===============================================================================================================
#QUERY BANCO NOC
query = '''select id_modem, nuImsi, dtBloqueioModem, id_status from modem where id_status = 6;'''

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
#DESBLOQUEANDO MODENS

dfDesbloqueios = dfNoc.copy()

if dfDesbloqueios.empty:
        print('Não há modens para desbloqueio')
        meth.write_log(padraoLog +'Não há modens para desbloqueio')
        sys.exit()
        
else:

    #FOR PARA DESBLOQUEAR MODENS
    count = 0

    for i in dfDesbloqueios.itertuples():

            dfConcatenar = dfDesbloqueios.copy()
            dfConcatenar = dfConcatenar.loc[(dfConcatenar['nuImsi'] == i.nuImsi)]
            
            print('Realizando desbloqueio em: ' + str(i.nuImsi) + ' Contagem em:' + str(count))
            count = int(count) + 1
            
            try:
            
                response = gatofy.desbloquearImsi(i.nuImsi)
                print(response)
            
            except:
                print('Não foi possível realizar o DESBLOQUEIO DOS MODENS')

                
#=======================================================================================================================            
#ATUALIZAR DESBLOQUEADOS NO BANCO

if dfNoc.empty:
    print('Não houve modens gerados para desbloqueio')
    meth.write_log(padraoLog +'Não há modens para desbloqueio')
    sys.exit()
    
else:
    dfNoc = dfNoc[['id_modem']]
    desbloqueioLista = dfNoc['id_modem'].to_list()
    desbloqueioTupla = meth.convert(desbloqueioLista)

    try:

        #ATUALIZANDO DESBLOQUEIOS
        cursor = connNoc.cursor()
        cursor.execute('''UPDATE modem SET id_status = 1, dtBloqueioModem = null WHERE id_modem IN'''+desbloqueioTupla+''';''')
        connNoc.commit()
        print('Realizada atualização no banco')

    except:
        the_type, the_value, the_traceback = sys.exc_info()
        erro = 'Falha na execução de update de modens DESBLOQUEADOS!!'
        meth.write_log(padraoLog + erro)
        print(the_type, ',' ,the_value,',', the_traceback)
                
                