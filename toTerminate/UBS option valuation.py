# calculate UBS PUT Option volatility

import fin_recipes
from black_scholes_imp_vol_bisect import *

stockprice = 27.2
strike = 32
r = 0.0275
time = 0.5
bid_option_price = 2.79
ask_option_price = 8.3

print(float(int(option_price_implied_volatility_put_black_scholes_bisections( \
            stockprice, strike, r, time, bid_option_price) * 10000)) / 100, end=' ')
print('/', end=' ')
print(float(int(option_price_implied_volatility_put_black_scholes_bisections( \
            stockprice, strike, r, time, ask_option_price) * 10000)) / 100, end=' ')
