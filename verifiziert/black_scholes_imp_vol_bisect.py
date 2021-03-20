""" ******************************************************

    Implizite Volatilitaet einer europaeischen Call/Put-Option.
    Berechnung mit Hilfe der klassischen Black & Scholes-
    Formel mit dem Bisection-Algorithmus.

    Beschreibung:   Funktion zur Berechnung der impliziten
                    Volatilitaet einer europaeischen Call,
                    bzw. Put Option.
                    
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
                                Preis, verifiziert mit Hull
*******************************************************"""
import math
import fin_recipes
import black_scholes_call
import black_scholes_put

def option_price_implied_volatility_call_black_scholes_bisections( \
                S, X, r, time, option_price):
    # check for arbitrage violations: 
    sigma_low = 0.0001
    price = black_scholes_call.option_price_call_black_scholes( \
                                            S,X,r,sigma_low,time)
    if price>option_price:
        # if price at almost zero volatility greater than price, return 0
        return 0.0
  
    # simple binomial search for the implied volatility.
    # relies on the value of the option increasing in volatility
    # make this smaller for higher accuracy
    ACCURACY = 1.0e-5
    MAX_ITERATIONS = 100
    HIGH_VALUE = 1e10
    ERROR = -1e40
    
    # want to bracket sigma. first find a maximum sigma by finding a sigma
    # with a estimated price higher than the actual price.
    sigma_high = 0.3
    price = black_scholes_call.option_price_call_black_scholes( \
                                            S,X,r,sigma_high,time)
    while price < option_price:
        # keep doubling.
        sigma_high = 2.0 * sigma_high 
        price = black_scholes_call.option_price_call_black_scholes( \
                                                S,X,r,sigma_high,time)
        if sigma_high>HIGH_VALUE:
            # panic, something wrong.
            return ERROR
    for i in range(MAX_ITERATIONS):
        sigma = (sigma_low+sigma_high)*0.5
        price = black_scholes_call.option_price_call_black_scholes( \
                                                    S,X,r,sigma,time)
        test =  (price-option_price)
        if abs(test)<ACCURACY: return sigma
        if test < 0.0: sigma_low = sigma
        else: sigma_high = sigma
    return ERROR

def option_price_implied_volatility_put_black_scholes_bisections( \
            S, X, r, time, option_price):
    # check for arbitrage violations: 
    sigma_low = 0.0001
    price = black_scholes_put.option_price_put_black_scholes( \
                                            S,X,r,sigma_low,time)
    if price>option_price:
        # if price at almost zero volatility greater than price, return 0
        return 0.0
  
    # simple binomial search for the implied volatility.
    # relies on the value of the option increasing in volatility
    # make this smaller for higher accuracy
    ACCURACY = 1.0e-5
    MAX_ITERATIONS = 100
    HIGH_VALUE = 1e10
    ERROR = -1e40
    
    # want to bracket sigma. first find a maximum sigma by finding a sigma
    # with a estimated price higher than the actual price.
    sigma_high = 0.3
    price = black_scholes_put.option_price_put_black_scholes( \
                                            S,X,r,sigma_high,time)
    while price < option_price:
        # keep doubling.
        sigma_high = 2.0 * sigma_high 
        price = black_scholes_put.option_price_put_black_scholes( \
                                                S,X,r,sigma_high,time)
        if sigma_high>HIGH_VALUE:
            # panic, something wrong.
            return ERROR
    for i in range(MAX_ITERATIONS):
        sigma = (sigma_low+sigma_high)*0.5
        price = black_scholes_put.option_price_put_black_scholes( \
                                                    S,X,r,sigma,time)
        test =  (price-option_price)
        if abs(test)<ACCURACY: return sigma
        if test < 0.0: sigma_low = sigma
        else: sigma_high = sigma
    return ERROR


if __name__=="__main__":
    from black_scholes_imp_vol_newt import option_price_implied_volatility_call_black_scholes_newton
    print('Test for european Call Implied Volatility. (B&S-Framework)')
    S = 50.0
    K = 50.0
    r = 0.1
    time = 0.5
    #sigma = 0.3
    current_price = 2.5
    sigma = 0.0
    sigma = option_price_implied_volatility_call_black_scholes_bisections( \
                                                S, K, r, time, current_price)
    print('Implied volatility calculated by means of the Bisection-Algorithm.')
    print('Sigma: should be %6.8f. Calculated: %6.8f.' % (0.0500427, sigma))
    sigma = 0.0
    sigma = option_price_implied_volatility_call_black_scholes_newton( \
                                                S, K, r, time, current_price)
    print('Implied volatility calculated by means of the Newton-Raphson-Algorithm.')
    print('Sigma: should be %6.8f. Calculated: %6.8f.' % (0.0500414, sigma))
    print('OK.')

    print()
    from black_scholes_imp_vol_newt import option_price_implied_volatility_put_black_scholes_newton
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

