import pandas as pd
from workalendar.america import Brazil
from datetime import date, datetime

from constantes import *
from _auxiliar import *

from bd_operacoes import captura_bd_operacoes, etl_bd_operacoes
from precos_book import curva_precos_para_book, captura_fpc
"""
Etapa Atual:

- Alteraras operações da BD Operacoes

O que ainda precisa fazer nesse codigo:
- Fazer os precos serem reajustados pela inflacao IPCA utilizando o Dataframe do python de inflacao
    - Projeto Git: inflacao_banco_central -> "Z:\Risk\51. Python Projects\Git Repositories\inflacao_banco_central"
    - Os dataframes estão serão sempre salvos na pasta -> "Z:\Risk\28. Portfolio Data Base\09.Inflação\Dataframe"

- Incluir a tabela com os precos do FPC, igual a aba "VaR-Covar Matrix_FPC BER" para montar a volatilidade do Book de Trading
    - O excel Matriz_FPC é a minha ideia para termos os preços de M+0 a A+4
    - Todos os calculos de retorno semanal e retorno semanal com Ln seria feita em Python
    - Os calulos de média simples, desvio padrão e Variancia seriam feitos em Python
    - O calculo da Volatilidade Semanal e Mensal seriam feitas em Python

- Fazer o calculo de var para cada um dos percentis com a volatilidade calculada
- Montar o BI com cada dataframe calculado
- Pronto! Book no BI (～￣▽￣)~

"""
def main():
    print('> Começando o processo do Book de Trading <\n')

    # Faz tudo de novo ou usa os Exceis prontos?
    faz_tudo_de_novo = True
    if faz_tudo_de_novo:

        bd_operacoes = captura_bd_operacoes()
        print('> Processo de captura da BD Operacoes finalizado com sucesso <\n')

        precos_book = curva_precos_para_book()
        print('> Processo de captura da Curva de Precos para o Book de Trading finalizado com sucesso <\n')

        fpc = captura_fpc()
        print('> Processo de captura da FPC para o Book de Trading finalizado com sucesso <\n')

    else:

        bd_operacoes = pd.read_excel(f'{SALVA_OS_DFS}/bd_operacoes_em_linhas.xlsx')
        precos_book = pd.read_excel(f'{SALVA_OS_DFS}/precos_book.xlsx')

    etl_bd_operacoes(df_bd_operacos=bd_operacoes, df_precos_book=precos_book)
    print('> Processo de etl da BD Operacoes finalizado com sucesso <\n')


if __name__ == '__main__':
    main()
