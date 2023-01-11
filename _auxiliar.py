import pandas as pd
from workalendar.america import Brazil
from datetime import datetime
import os
import sys

from constantes import *

# Monta um dataframe com todas os meses e horas dos meses 
def _periodo_e_horas_meses(mes_inicial=MES_INICIAL, qtd_meses=MESES_TOTAL_BOOK):
       
    try:
        col_periodo = []
        col_horas_mes = []
        mes = mes_inicial

        if isinstance(mes_inicial, str):
           mes = datetime.strptime(mes, '%Y-%m-%d')

        for i in range(qtd_meses):

            horas = ((pd.to_datetime(mes) + pd.DateOffset(months=1)) - mes)*24
            horas_int = int(str(horas)[:3])

            col_horas_mes.append(horas_int)
            col_periodo.append(mes)
            
            mes = pd.to_datetime(mes) + pd.DateOffset(months=1)

        periodos_e_horas = pd.DataFrame({'Periodo': col_periodo, 'Horas': col_horas_mes})
        print('> Dataframe de meses e horas montado com sucesso')
        
        #Salva o Dataframe
        #_salva_dataframes(df=periodos_e_horas, nome="periodos_e_horas",formato='Excel')

        # Retorna um Dataframe
        return periodos_e_horas

    except:
        print('> Data precisa estar formatada em AAAA-MM-DD e quantidade de meses precisa ser um numero inteiro positivo')
        sys.exit()


# Funcao para salvar os DFs gerados em Dataframes para facil acesso
def _salva_dataframes(df, nome, caminho=SALVA_OS_DFS, formato='Excel'):
    
    try:
        if not os.path.exists(caminho):
            os.makedirs(caminho)
        
        if formato == 'Excel':
            arq = f'{caminho}\\{nome}.xlsx'

            if os.path.exists(arq):
                os.remove(arq)

            df.to_excel(arq)

        elif formato == 'csv':     
            arq = f'{caminho}\\{nome}.csv'
            
            if os.path.exists(arq):
                os.remove(arq)

            df.to_csv(arq)

        else:
            arq = f'{caminho}\\{nome}.df'
            
            if os.path.exists(arq):
                os.remove(arq)

            df.to_pickle(arq)

        print(f'> O Dataframe "{nome}" foi salvo na pasta {caminho}.\n')
    
    except:
        print(f'> Não foi possivel salvar o "{nome}". Algum parametro esta errado.')


# Funcao para decidir qual é o ultimo dia util antes da data enviada
def _ultimo_dia_util(formato='data'):
    calendario_br = Brazil()

    try:
        dia = datetime.today().date() - pd.DateOffset(days=1)

        while calendario_br.is_working_day(dia) == False:
            dia = pd.to_datetime(dia) - pd.DateOffset(days=1)
        
        if formato == 'str':
            dia_util = dia.strftime('%Y-%m-%d')
        elif formato == 'data':
            dia_util = dia.date()
            
        print(f'> O ultimo dia util foi : {dia_util}')

    except:
        print("Formatação da data incorreta: 'AAAA-MM-DD'")

    # Retorna uma data
    return dia_util