""" ******************************************************

    Put Option-Preis basieren auf Black&Scholes.

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
from finrecipes.cum_normal import N # the calculation of the cumularive normal distribution

def option_price_put_black_scholes(S, K, r, sigma, time):
    time_sqrt = math.sqrt(time)
    d1 = (math.log(S/K)+r*time)/(sigma*time_sqrt)+0.5*sigma*time_sqrt
    d2 = d1-(sigma*time_sqrt)
    return K*math.exp(-r*time)*N(-d2) - S*N(-d1)
#    return K*exp(-r*time)*N(-d2) - S*N(-d1);

if __name__=="__main__":
    # Test
    print('Test for Black&Scholes formula')
    print('Price for an European Call Option (p. 57 manual).')
    print()
    S = 42.0
    K = 40.0
    r = 0.10
    sigma = 0.20
    time = 0.50
    style = 'european'
    type = 'put'
    value = option_price_put_black_scholes(S, K, r, sigma, time)
    print('noch das ausrechnen!!!')
    print('The result should be according to the manual: %6.2f.' % (0.81))
    print('The theoretical price for a %s %s option with strike %4.2f is: %6.5f' \
          % (style, type, K, value) )
