import os

#Logins e Senhas
EHUB_EMAIL = "guilherme.cruz@elera.com"
EHUB_SENHA = "Ber@2021!"

#Diretórios
FORECAST_ASSUMPTIONS_DIR = r"C:\Users\lumm\OneDrive - Elera\Documentos\Python Scripts\Book no BI\Recursos\Forecast Assumptions.xlsx"
BD_OPERACOES_DIR = r"C:\Users\lumm\OneDrive - Elera\Documentos\Python Scripts\Book no BI\Recursos\BD_OPERACOES.xlsm"
INFLACOES_DFS_DIR = r'Z:\Risk\28. Portfolio Data Base\09.Inflação\Dataframe'
SALVA_OS_DFS = f'{os.getcwd()}\Dataframe'

# Constantes para o Book
MES_INICIAL = '2022-01-01'
STOP_LOSS = 20000000 #20 MILHOES
VAR = 30000000 #30 MILHOES
PLD_PISO = 55.7
PLD_TETO = 646.58
ALFA_T_STUDENT = 0.05
LIMITE_FY_BOOK_MWM = 60
LIMITE_FY_BOOK_MWM = 20

# Anos e Meses do Book de Trading
ANOS_OPERACIONAL_BOOK = 2
MESES_OPERACIONAL_BOOK = ANOS_OPERACIONAL_BOOK * 12

ANOS_TOTAL_BOOK = 5
MESES_TOTAL_BOOK = ANOS_TOTAL_BOOK * 12

# Anos e Meses da BD Operacoes
ANOS_BD_OPERACOES = 5
MESES_BD_OPERACOES = ANOS_BD_OPERACOES * 12

COL_INICIO_VOLUME = 26
COL_INICIO_PRECO = 92

