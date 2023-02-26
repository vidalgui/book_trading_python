import pandas as pd
from workalendar.america import Brazil
from datetime import date

from constantes import *
from _auxiliar import *

from ehubAPI import forwardCurve
from _auxiliar import _periodo_e_horas_meses, _ultimo_dia_util, _salva_dataframes

"""
Neste código, atualmente estamos utilizando apenas a Curva Forward do eHub como parâmetro para os preços.
Para o Book de Trading, o ideal é utilizarmos os preços de negociações fechadas no dia útil anterior.
Para isto, precisamos de uma função que retorne os preços da mesma forma que fazemos manualmente no Book.
"""

# Monta a curva de precos que vai ser utilizada no Book de Trading
def curva_precos_para_book(mes_inicial= MES_INICIAL):

    # Roda a funcao da ultima curva forward
    curva_forward =  _ultima_curva_forward()

    # Roda a funcao da dos precos realizados
    forecast_assumptions =  _precos_realizados_forecast_assumptions()

    # Executa a funcao do periodo do book
    periodo_book = _periodo_e_horas_meses()

    # Define o mes inicial do Book
    mes_inicial = pd.to_datetime(mes_inicial)

    # Se o forecast_assumptions for None quer dizer que não tem PLD realizado ainda e 
    # Se eu não tiver o mes inicial na Curva Foward
    if forecast_assumptions.empty and (mes_inicial in curva_forward['Periodo']) == False:
        
        print('> Não consigo montar os precos do Book pois não tenho os PLDS realizados nem a curva forward')
        print('> Favor criar uma planilha igual ao Forecast Assumptions com a data correta e o PLD realizado')
    
    # Se somente o forecast_assumptions for None
    else:
        
        # ETL da curva forward para o preco do Book
        df_curva_forward = curva_forward[['dataSource', 'name', 'Periodo', 'vertexValue']]
        df_curva_forward = df_curva_forward.rename(columns={'dataSource': 'Fonte', 'name': 'Tipo', 'vertexValue': 'Valor'})
        df_curva_forward['Fonte'] = 'Ehub BBCCE'
        df_curva_forward['Tipo'] = 'Forward'
        df_curva_forward = df_curva_forward[df_curva_forward['Periodo'].isin(periodo_book['Periodo'])]

        # Aumenta o periodo até coincidir com o periodo do Book
        while not df_curva_forward['Periodo'].iloc[-1] == periodo_book['Periodo'].iloc[-1]:

            ult_linha = df_curva_forward.iloc[-1].copy()
            ult_linha['Periodo'] = pd.to_datetime(ult_linha['Periodo']) + pd.DateOffset(months=1)
            df_curva_forward = df_curva_forward.append([ult_linha])
        
        precos_book = df_curva_forward.sort_values(by='Periodo').reset_index(drop=True)
        precos_book = precos_book.merge(periodo_book, left_on='Periodo', right_on='Periodo', how='left')
        
        # Se somente o forecast_assumptions for None
        if not forecast_assumptions.empty:

            # ETL dos precos realizados para o preco do Book
            filtro_1 = (forecast_assumptions['FORECAST ASSUMPTIONS'] == 'PLD SE')
            filtro_2 = (forecast_assumptions['Tipo'] == "Forecast")
            df_forecast_assumptions = forecast_assumptions.loc[filtro_1 & filtro_2].rename(columns={'FORECAST ASSUMPTIONS': 'Fonte' })
            df_forecast_assumptions = df_forecast_assumptions[~df_forecast_assumptions['Periodo'].isin(df_curva_forward['Periodo'])]
            df_forecast_assumptions['Fonte'] = 'Forecast Assumptions'
            df_forecast_assumptions['Tipo'] = 'Realizado'

            precos_book = pd.concat([df_curva_forward, df_forecast_assumptions]).sort_values(by='Periodo').reset_index(drop=True)
            precos_book = precos_book.merge(periodo_book, left_on='Periodo', right_on='Periodo', how='left')
        
        print('> Precos para o Book montado com sucesso')

    #Salva o Dataframe
    #_salva_dataframes(df=precos_book, nome='precos_book', formato='Excel')

    # Retorna um Dataframe
    return precos_book


# Monta a curva forward do EHUB
def _ultima_curva_forward():

    #Define o ultimo dia util antes de hoje
    dia_util = _ultimo_dia_util(formato='str')

    # Dataframe da Curva Forward do EHUB 
    curva_forward = pd.DataFrame(forwardCurve(dia_util, EHUB_EMAIL, EHUB_SENHA))

    #ETL da Curva Forward do EHUB
    periodo = []
    for linha in curva_forward['vertexDate']:
        data = date(year= pd.to_datetime(linha).year, month=pd.to_datetime(linha).month, day=1)
        periodo.append(data)

    curva_forward['Periodo'] = periodo
    curva_forward['Periodo'] = curva_forward['Periodo'].astype("datetime64")

    print('> Curva forward calculado com sucesso')

    #Salva o Dataframe
    #_salva_dataframes(df=curva_forward, nome='curva_forward', formato='Excel')

    # Retorna um Dataframe
    return curva_forward


# Monta a curva de precos realizados da Forecast Assumptions
def _precos_realizados_forecast_assumptions(mes_inicial= MES_INICIAL, forecast_assumption_diretorio= FORECAST_ASSUMPTIONS_DIR):
    
    # Dataframe do arquivo de Forecast Assumption com os PLDs realizados 
    forecast_assumptions_arq = pd.read_excel(forecast_assumption_diretorio, skiprows=1, sheet_name="Assumptions")

    # Checa se o primeiro mes do Book é igual ao primeiro mes do Forecast Assumptions
    if forecast_assumptions_arq.columns[3] != pd.to_datetime(mes_inicial):
        print('> Mes inicial da Forecast Assumptions diferente do Mes inicial do Book de Trading')
        print('> Continuando sem realizado do PLD')
        
        forecast_assumptions = None
    else:
    # ETL do Forecast Assumptions
        forecast_assumptions = forecast_assumptions_arq.iloc[:,1:15].loc[7:,:].reset_index(drop=True)
        forecast_assumptions['FORECAST ASSUMPTIONS'] = forecast_assumptions.iloc[:,1]
        forecast_assumptions['FORECAST ASSUMPTIONS'].replace({'Previous Forecast': pd.NaT , 'Forecast': pd.NaT }, inplace=True)
        forecast_assumptions['FORECAST ASSUMPTIONS'].ffill(inplace=True)
        forecast_assumptions.rename(columns={'Unnamed: 2': 'Tipo'}, inplace=True)
        forecast_assumptions = forecast_assumptions[~forecast_assumptions.iloc[:,3].isna()]
        forecast_assumptions = pd.melt(forecast_assumptions, id_vars=['FORECAST ASSUMPTIONS', 'Tipo'],var_name='Periodo', value_name="Valor" )
        print('> Precos realizados calculado com sucesso')

    #Salva o Dataframe
    _salva_dataframes(df=forecast_assumptions, nome='forecast_assumptions', formato='Excel')

    # Retorna um Dataframe
    return forecast_assumptions

def captura_fpc():
    df_fpc = pd.read_excel(FPC_DIR,
                           sheet_name="FPC_TABLE", usecols="B:K", header=3)
    df_fpc = df_fpc.loc[df_fpc["Date"] >= "2015-12-31"]
    _salva_dataframes(df_fpc, 'FPC', formato="Excel")
    return df_fpc