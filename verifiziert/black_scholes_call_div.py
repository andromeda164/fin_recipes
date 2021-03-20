""" ******************************************************

    Europaeischer Call Option-Preis basieren auf Black & Scholes
    mit diskreten Dividenden.

    Beschreibung:   Funktion zur Berechnung des theoretischen
                    Preises einer europaeischen Call-Option mit
                    klassischer Black & Scholes-Formel.

                    Diskrete Dividenden.

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
    time_to_maturity float      time to maturity
    dividend_times   float      Dividend times
    dividend_amounts float      Dividend amounts in monetaeren
                                Betraegen.
    
    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK          Manual p. 69
    Literatur-Ref   --
*******************************************************"""
import math
from black_scholes_call import option_price_call_black_scholes

def option_price_european_call_dividends( \
            S, K, r, sigma, time_to_maturity, dividend_times, dividend_amounts):
    """ To adjust the price of an European option for known dividends,
        we merely subtract the present value of the dividends from the
        current price of the underlying asset in calculating the
        Black Scholes value. """
    adjusted_S = S
    for i in range(len(dividend_times)):
        if dividend_times[i]<=time_to_maturity:
            adjusted_S = adjusted_S - dividend_amounts[i] * math.exp(-r*dividend_times[i])
    return option_price_call_black_scholes(adjusted_S,K,r,sigma,time_to_maturity)

if __name__=="__main__":
    print 'Test for Black&Scholes with discrete dividends formula'
    print 'Price for an European Call Option (p. 69 manual).'
    print
    S = 100.0
    K = 100.0
    r = 0.10
    sigma = 0.25
    time = 1.0
    dividend_yield = 0.05
    dividend_times   = [0.25, 0.75]
    dividend_amounts = [2.5,   2.5]
    style = 'european'
    type = 'call'
    value = option_price_european_call_dividends( \
        S, K, r, sigma, time, dividend_times, dividend_amounts)
    print 'The result should be according to the manual: %6.5f.' % (11.8094)
    print 'The theoretical price for a %s %s option with strike %4.2f is: %6.5f' \
          % (style, type, K, value)
    print 'OK.'
