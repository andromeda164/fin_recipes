""" ******************************************************

    Implizite Volatilitaet einer europaeischen Call/Put-Option.
    Berechnung mit Hilfe der klassischen Black & Scholes-
    Formel mit dem Newton-Raphson-Algorithmus.

    Beschreibung:   Funktion zur Berechnung der impliziten
                    Volatilitaet einer europaeischen Call/
                    Put Option.
                    
                    Berechnung mit Hilfe der klassischen
                    Black & Scholes - Formel mit dem
                    Bisection-Algorithmus.

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
    time            float       time to maturity
    option_price    float       Option price
    
    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK          page 65 Manual
    Literatur-Ref   OK          verglichen mit analyt. Put-
                                Preis, verifiziert mit Hull.
*******************************************************"""
import math
import fin_recipes
import black_scholes_call
import black_scholes_put
import normdist

def option_price_implied_volatility_call_black_scholes_newton( \
        S, K, r, time, option_price):
    # check for arbitrage violations:
    sigma_low = 1e-5
    price = black_scholes_call.option_price_call_black_scholes( \
                                            S,K,r,sigma_low,time)
    if price>option_price:
        # if price at almost zero volatility greater than price, return 0
        return 0.0

    MAX_ITERATIONS = 100
    ACCURACY    = 1.0e-6
    t_sqrt = math.sqrt(time)

    # find initial value
    sigma = (option_price/S)/(0.398*t_sqrt)
    for i in range(MAX_ITERATIONS):
        price = black_scholes_call.option_price_call_black_scholes( \
                                                    S,K,r,sigma,time)
        diff = option_price - price
        if abs(diff)<ACCURACY:
            return sigma
        d1 = (math.log(S/K)+r*time)/(sigma*t_sqrt) + 0.5*sigma*t_sqrt
        vega = S * t_sqrt * normdist.n(d1)
        sigma = sigma + diff/vega
    raise Exception('something screwy happened in option_price_implied_volatility_call_black_scholes_newton')

def option_price_implied_volatility_put_black_scholes_newton( \
        S, K, r, time, option_price):
    # check for arbitrage violations:
    sigma_low = 1e-5
    price = black_scholes_put.option_price_put_black_scholes( \
                                            S,K,r,sigma_low,time)
    if price>option_price:
        # if price at almost zero volatility greater than price, return 0
        return 0.0

    MAX_ITERATIONS = 100
    ACCURACY    = 1.0e-7
    t_sqrt = math.sqrt(time)

    # find initial value
    sigma = (option_price/S)/(0.398*t_sqrt)
    for i in range(MAX_ITERATIONS):
        price = black_scholes_put.option_price_put_black_scholes( \
                                                    S,K,r,sigma,time)
        diff = option_price - price
        if abs(diff)<ACCURACY:
            return sigma
        d1 = (math.log(S/K)+r*time)/(sigma*t_sqrt) + 0.5*sigma*t_sqrt
        vega = S * t_sqrt * normdist.n(d1)
        sigma = sigma + diff/vega
    raise Exception('something screwy happened in option_price_implied_volatility_put_black_scholes_newton')


if __name__=="__main__":
    from black_scholes_imp_vol_bisect import option_price_implied_volatility_call_black_scholes_bisections
    print('Test for european Call-Delta. (B&S-Framework)')
    S = 50.0
    K = 50.0
    r = 0.1
    time = 0.5
    #sigma = 0.3
    current_price = 2.5
    sigma = option_price_implied_volatility_call_black_scholes_bisections( \
                                                S, K, r, time, current_price)
    print('Implied volatility calculated by means of the Bisection-Algorithm.')
    print('Sigma: should be %6.8f. Calculated: %6.8f.' % (0.0500427, sigma))
    sigma = option_price_implied_volatility_call_black_scholes_newton( \
                                                S, K, r, time, current_price)
    print('Implied volatility calculated by means of the Newton-Raphson-Algorithm.')
    print('Sigma: should be %6.8f. Calculated: %6.8f.' % (0.0500414, sigma))
    print('OK.')

    print()
    from black_scholes_imp_vol_bisect import option_price_implied_volatility_put_black_scholes_bisections
    print('Test for european Put Implied Volatility. (B&S-Framework)')
    S = 42.0
    K = 40.0
    r = 0.10
    time = 0.50
    #sigma = 0.20
    current_price = 0.81
    sigma = 0.0
    sigma = option_price_implied_volatility_put_black_scholes_bisections( \
                                                S, K, r, time, current_price)
    print('Implied volatility calculated by means of the Bisection-Algorithm.')
    print('Sigma: should be %6.8f. Calculated: %6.8f.' % (0.2, sigma))
    sigma = 0.0
    sigma = option_price_implied_volatility_put_black_scholes_newton( \
                                                S, K, r, time, current_price)
    print('Implied volatility calculated by means of the Newton-Raphson-Algorithm.')
    print('Sigma: should be %6.8f. Calculated: %6.8f.' % (0.2, sigma))
    print('OK.')

