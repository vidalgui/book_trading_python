import numpy as np
import pandas as pd
from scipy.stats import t
from _auxiliar import _salva_dataframes

# Define asset returns and monthly volatility
#Define os preços semanais pela FPC e calcula o Weekly Returns
def _calcula_weekly_returns():
    weekly_prices = pd.read_excel('Dataframe/FPC.xlsx')
    weekly_returns = pd.DataFrame()
    for i in list(weekly_prices.columns)[1:10]:
        weekly_returns["Date"] = weekly_prices["Date"]
        weekly_returns[i] = np.log(weekly_prices[i]) - np.log(weekly_prices[i].shift(1))

    _salva_dataframes(weekly_returns, "weekly_returns", formato="Excel")
    return weekly_returns




