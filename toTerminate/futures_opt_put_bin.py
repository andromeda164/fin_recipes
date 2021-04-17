""" ******************************************************

    Put-Optionspreis auf Futures-Option

    Beschreibung:   Funktion zur Berechnung des theoretischen
                    Preises einer Put-Option auf eine
                    Futures-Option, berechnet via

                    Der Zinssatz r muss vorgaengig
                    KONTINUIERLICH verzinst worden sein.
                    Siehe S. 28 des Manuals fuer die
                    Berechnungsformeln.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    F               float       Futures price
    K               float       Strike price
    r               float       interest rate
    sigma           float       volatility
    time            float       time to maturity
    no_steps        int         number of binominal steps

    Status
    -----------------------------------------------------
    Syntax          --
    Numerisch       --
    Testprogramm    --
    Literatur-Ref   --
*******************************************************"""
import math
import fin_recipes

def futures_option_price_put_american_binomial(F, X, r, sigma, time, no_steps):
    futures_prices = [0.0]*(no_steps+2) # nicht no_steps+1 !!! ergibt sonst 1 zu wenig!
    put_values = [0.0]*(no_steps+2) # nicht no_steps+1 !!! ergibt sonst 1 zu wenig!
    t_delta = time / no_steps
    Rinv = math.exp(-r*(t_delta))
    u = math.exp(sigma*math.sqrt(t_delta))
    d = 1.0/u
    uu = u*u
    uInv = 1.0 / u
    pUp = (1-d)/(u-d)
    pDown = 1.0 - pUp
    print(futures_prices, put_values, t_delta)
    futures_prices[0] = F*math.pow(d, no_steps)
    for i in range(1, no_steps+1):
        # terminal tree nodes
        futures_prices[i] = uu*futures_prices[i-1]
    for i in range(no_steps+1):
        put_values[i] = max(0.0, (X-futures_prices[i]))
    for step in range(no_steps-1,-1,-1): #(int step=no_steps-1; step>=0; --step) {
        for i in range(step+1):
            futures_prices[i] = uInv*futures_prices[i+1]
            put_values[i] = (pDown*put_values[i]+pUp*put_values[i+1])*Rinv
            put_values[i] = max(put_values[i], X-futures_prices[i]) # check for exercise
    return put_values[0]

if __name__=="__main__":
    # Test
    print('Test for Black&Scholes formula')
    print('Price for an American Put Option on a Futures (p. 92 manual).')
    print()
    F = 50.0
    K = 50.0
    r = 0.08
    sigma = 0.20
    time = 0.50
    no_steps = 10
    style = 'american'
    type = 'put'
    value = futures_option_price_put_american_binomial(F, K, r, sigma, time, no_steps)
    print('The result should be according to DerivaGem: %6.5f.' % (2.81058961))
    print('The theoretical price for a %s %s option with strike %4.2f is: %6.5f' \
          % (style, type, K, value)) 
