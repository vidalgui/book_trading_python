import numpy as np
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

# Define number of months and degrees of freedom
num_months = len(asset_returns)
df = num_months - 1
print(df)


# Calculate VaR for every percentile from 1 to 99
for percentile in range(1, 100):
    confidence_level = percentile / 100
    t_value = t.ppf(1 - confidence_level, df)
    VaR = np.dot(asset_returns, (1 - t_value * np.sqrt(num_months)))
    print(VaR)


