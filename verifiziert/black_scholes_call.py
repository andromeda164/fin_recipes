""" ******************************************************

    Call Option-Preis basieren auf Black&Scholes.

    Beschreibung:   Funktion zur Berechnung des theoretischen
                    Preises einer Call-Option mittels
			  klassischer Black&Scholes-Formel.

                    Der Zinssatz r muss vorgaengig
                    KONTINUIERLICH verzinst worden sein.
                    Siehe S. 28 des Manuals fuer die
                    Berechnungsformeln.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    S               float       Spot (Underlying) price
    K               float       Strike price
    r               float       interest rate
    sigma           float       volatility
    time            float       time to maturity

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK          Manual p. 57
    Literatur-Ref   OK          Pag. 244, Hull
*******************************************************"""
import math
from cum_normal import *
import fin_recipes

# the calculation of the cumularive normal distribution

def option_price_call_black_scholes(S, K, r, sigma, time):
    time_sqrt = math.sqrt(time)
    d1 = (math.log(S/K)+r*time)/(sigma*time_sqrt)+0.5*sigma*time_sqrt
    d2 = d1-(sigma*time_sqrt)
    return S*N(d1) - K*math.exp(-r*time)*N(d2)

if __name__=="__main__":
    # Test
    print('Test for Black&Scholes formula')
    print('Price for an European Call Option (p. 57 manual).')
    print()
    S = 50.0
    K = 50.0
    r = 0.10
    sigma = 0.30
    time = 0.50
    style = 'european'
    type = 'call'
    value = option_price_call_black_scholes(S, K, r, sigma, time)
    print('The result should be according to the manual: %6.5f.' % (5.45325))
    print('The theoretical price for a %s %s option with strike %4.2f is: %6.5f' \
          % (style, type, K, value) )

    print()
    print('Price for an European Call Option (p. 244 Hull).')
    print()
    S = 42.0
    K = 40.0
    r = 0.10
    sigma = 0.20
    time = 0.50
    style = 'european'
    type = 'call'
    value = option_price_call_black_scholes(S, K, r, sigma, time)
    print('The result should be according to the manual: %6.2f.' % (4.76))
    print('The theoretical price for a %s %s option with strike %4.2f is: %6.5f' \
          % (style, type, K, value) )

    print()
    print('Price for an European Call Option (p. 3/23 AZEK Derivatives).')
    print()
    S = 280
    K = 260
    r = 0.0029955
    sigma = 0.3
    time = 0.24657
    style = 'european'
    type = 'call'
    value = option_price_call_black_scholes(S, K, r, sigma, time)
    print('The result should be according to the manual: %6.2f.' % (0.93))
    print('The theoretical price for a %s %s option with strike %4.2f is: %6.5f' \
          % (style, type, K, value) )
