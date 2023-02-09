import numpy as np
from scipy.stats import t

# Define asset returns and monthly volatility
asset_returns = np.array([30, 20, -10, 50, -20])
monthly_volatility = np.array([0.01, 0.03, 0.02, 0.04, 0.03])

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


