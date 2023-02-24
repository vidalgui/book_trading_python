import pandas as pd
from workalendar.america import Brazil
from datetime import date, datetime

from constantes import *
from _auxiliar import _periodo_e_horas_meses, _salva_dataframes

# Monta a BD Operacoes para o Book de Trading
def captura_bd_operacoes(caminho_bd=BD_OPERACOES_DIR, col_inicio_vol=COL_INICIO_VOLUME, col_inicio_preco=COL_INICIO_PRECO, qtd_meses=MESES_BD_OPERACOES):

    bd_operacoes_arq = pd.read_excel(caminho_bd, sheet_name="BD_COMERCIAL", skiprows=3, usecols="B:FK")
    bd_operacoes_arq.dropna(subset=['COD_WBC'], inplace=True)

    # Monta um Dataframe com os meses e as horas dos meses
    df_periodos_e_horas = _periodo_e_horas_meses()

    # Transformando os COD WBC em unicos 
    bd_operacoes_arq['Duplicados'] = bd_operacoes_arq['COD_WBC'].duplicated(keep=False)
    cod_wbc_duplicados = 0
    todos_cod_wbc = []

    for i, linha in bd_operacoes_arq.iterrows():

        if linha['Duplicados']:
            todos_cod_wbc.append(f'wbc_{cod_wbc_duplicados}')
            cod_wbc_duplicados += 1

        else:
            todos_cod_wbc.append(linha['COD_WBC'])
        
    bd_operacoes_arq['COD_WBC'] = todos_cod_wbc

    # Monta o DF de Volumes da BD Operações,transpondo os volumes para linha
    bd_operacoes_vol = bd_operacoes_arq.iloc[:, col_inicio_vol : col_inicio_vol + qtd_meses]
    bd_operacoes_vol.columns = df_periodos_e_horas['Periodo'].to_list()
    bd_operacoes_vol['COD_WBC'] = bd_operacoes_arq['COD_WBC']
    bd_operacoes_vol = bd_operacoes_vol.melt(id_vars=["COD_WBC"],var_name="Periodo",value_name="Vol MWm")

    # Monta o DF de Precos da BD Operações, transpondo os precos para linha
    bd_operacoes_preco = bd_operacoes_arq.iloc[:, col_inicio_preco : col_inicio_preco + qtd_meses]
    bd_operacoes_preco.columns = df_periodos_e_horas['Periodo'].to_list()
    bd_operacoes_preco['COD_WBC'] = bd_operacoes_arq['COD_WBC']
    bd_operacoes_preco = bd_operacoes_preco.melt(id_vars=["COD_WBC"],var_name="Periodo",value_name="Preco")

    # Unifica os DFs de volume e preco
    bd_operacoes_vol_e_preco = bd_operacoes_vol.merge(bd_operacoes_preco, on=['COD_WBC','Periodo'], how='left').reset_index(drop=True)

    # Monta o DF com as informações de cada contrato, sem volume e preco
    bd_operacoes_sem_vol_preco = bd_operacoes_arq.iloc[:,:col_inicio_vol]
    bd_operacoes_sem_vol_preco = bd_operacoes_sem_vol_preco.join(bd_operacoes_arq['Compra/venda']).join(bd_operacoes_arq['_'])

    # Monta o DF final com todas as operações, as informacoes, volumes e precos
    bd_operacoes_em_linhas = bd_operacoes_vol_e_preco.merge(bd_operacoes_sem_vol_preco, on='COD_WBC', how='left').reset_index(drop=True)
    bd_operacoes_em_linhas = bd_operacoes_em_linhas.dropna(subset=['Vol MWm', 'Preco']).reset_index(drop=True)

    #Salva o Dataframe
    _salva_dataframes(df=bd_operacoes_em_linhas, nome="bd_operacoes_em_linhas",formato='Excel')

    # Retorna um Dataframe
    return bd_operacoes_em_linhas


def etl_bd_operacoes(df_bd_operacos, df_precos_book):

    bd_operacoes = df_bd_operacos
    precos_book = df_precos_book

    # Filtra para somente pegar um book
    bd_operacoes = bd_operacoes[bd_operacoes['BOOK'] == 'Trading']

    # Une os DFs da BD operacoes com o Periodo e horas e com o Precos do Book
    df_uniao_bd_operacoes_e_periodo = bd_operacoes.merge(precos_book, left_on='Periodo', right_on='Periodo', how='left')
    print(df_uniao_bd_operacoes_e_periodo)
    # Modificação do Preco
    linhas_de_pld_mais = df_uniao_bd_operacoes_e_periodo['MOD PREÇO'] == 'PLD + Spread'
    bd_operacoes.loc[linhas_de_pld_mais,'MOD PREÇO'] = df_uniao_bd_operacoes_e_periodo.loc[linhas_de_pld_mais,'Preco'] + df_uniao_bd_operacoes_e_periodo.loc[linhas_de_pld_mais,'Valor']

    # Preco com IPCA = Ajustado
    linhas_de_preco_ajustado = ~pd.isnull(df_uniao_bd_operacoes_e_periodo['ÍNDICE'])
    bd_operacoes.loc[linhas_de_preco_ajustado,'MOD PREÇO'] = 'Ajustado'


    # Preenche com as horas, Volume em MWh e o PLD (Preço de mercado)
    bd_operacoes['Horas'] = df_uniao_bd_operacoes_e_periodo['Horas']
    bd_operacoes['Vol MWh'] = bd_operacoes['Vol MWm'] * df_uniao_bd_operacoes_e_periodo['Horas']
    bd_operacoes['PLD'] = df_uniao_bd_operacoes_e_periodo['Valor']

    #Cria colunas vazias
    bd_operacoes['Preco MTM'] = [pd.NaT] * len(bd_operacoes)
    bd_operacoes['CNPJ Contraparte'] = [pd.NaT] * len(bd_operacoes)

    # PLD+
    linhas_de_pld_mais = df_uniao_bd_operacoes_e_periodo['MOD PREÇO'] == 'PLD + Spread'
    bd_operacoes.loc[linhas_de_pld_mais,'MOD PREÇO'] = df_uniao_bd_operacoes_e_periodo.loc[linhas_de_pld_mais,'Preco'] + df_uniao_bd_operacoes_e_periodo.loc[linhas_de_pld_mais,'Valor']

    # Venda
    linhas_de_venda = df_uniao_bd_operacoes_e_periodo['Compra/venda'] == 'V'
    bd_operacoes.loc[linhas_de_venda,'Preco MTM'] = df_uniao_bd_operacoes_e_periodo.loc[linhas_de_venda,'Preco'] - df_uniao_bd_operacoes_e_periodo.loc[linhas_de_venda,'Valor']
    bd_operacoes.loc[linhas_de_venda,'CNPJ Contraparte'] = df_uniao_bd_operacoes_e_periodo.loc[linhas_de_venda,'CNPJ COMPRADOR'] 

    # Compra
    linhas_de_compra = df_uniao_bd_operacoes_e_periodo['Compra/venda'] == 'C'
    bd_operacoes.loc[linhas_de_compra,'Preco MTM'] = df_uniao_bd_operacoes_e_periodo.loc[linhas_de_compra,'Valor'] - df_uniao_bd_operacoes_e_periodo.loc[linhas_de_compra,'Preco']
    bd_operacoes.loc[linhas_de_venda,'CNPJ Contraparte'] = df_uniao_bd_operacoes_e_periodo.loc[linhas_de_venda,'CNPJ VENDEDOR'] 

    bd_operacoes['Receita MTM'] = bd_operacoes['Vol MWh'] * bd_operacoes['Preco MTM']

    # Salva o Dataframe
    _salva_dataframes(df=bd_operacoes, nome="bd_operacoes",formato='Excel')

    return bd_operacoes

