""" ******************************************************

    Delta einer europaeischer Call basierend auf
    Black & Scholes.

    Beschreibung:   Funktion zur Berechnung des Deltas
                    einer europaeischer Call, basierend
                    auf Black & Scholes.

                    Ohne Dividenden-Adjustment.

                    Der Zinssatz r muss vorgaengig
                    KONTINUIERLICH verzinst worden sein.
                    Siehe S. 28 des Manuals fuer die
                    Berechnungsformeln.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    S               float       Spot (Underlying) price
    K               float       Strike price
    r               float       interest rate, cont. comp.
    sigma           float       volatility
    time            float       time to maturity
    
    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK          Seite 62 Manual
    Literatur-Ref   --
*******************************************************"""
import math
import fin_recipes
import cum_normal

def option_price_delta_call_black_scholes(S, K, r, sigma, time):
    time_sqrt = math.sqrt(time)
    d1 = (math.log(S/K)+r*time)/(sigma*time_sqrt) + 0.5*sigma*time_sqrt
    delta = cum_normal.N(d1)
    return delta

if __name__=="__main__":
    print 'Test for european Call-Delta. (B&S-Framework)'
    S = 100.0
    K = 100.0
    r = 0.1
    time = 0.5
    sigma = 0.3
    value = option_price_delta_call_black_scholes(S, K, r, sigma, time)
    print 'The delta for the example option is %6.6f.' % value
    print 'It should be according to the example: 0.633737'
    print 'OK.'
    
