""" ******************************************************

    Bewertungsfunktion fuer europaeische Put-Optionen
    via Binomial Tree (normaler Cox-Ross Tree).

    Beschreibung:   Bewertungsfunktion fuer europaeische
                    Put-Optionen via Binomial Tree
                    (recombining). Es handelt sich um einen
                    normalen Cox-Ross Tree.

                    Alle Parameter (u, d, p) werden aus S,X,
                    r, sigma, t und Anzahl Steps des Trees
                    berechnet.
                    
                    u = exp(sigma*sqrt(dt))
                    d = 1 / u
                    
                        exp(r*dt) - d
                    p = -------------
                         u - d

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    S               float       Spot price, Underlying
                                zum Zeitpunkt null
    X               float       strike
    r               float       interest rate, continuously
                                compounded
    sigma           float       volatility, 0.20 fuer 20%
    t               float       time to maturity (years)
    steps           integer     Anzahl Steps des Trees

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK          Wird im Testprogramm mit analy-
                                tischer B&S Formel verglichen!
    Literatur-Ref   OK          Kreuzvergleich mit analytischer
                                B&S Formel Hull OK.
*******************************************************"""
import math

def option_price_put_european_binomial(S, X, r, sigma, t, steps):
    # interest rate for each step
    R = math.exp(r*(t/steps))
    # inverse of interest rate
    Rinv = 1.0/R
    # up movement
    u = math.exp(sigma*math.sqrt(t/float(steps)))
    uu = u*u
    d = 1.0/u
    p_up = (R-d)/(u-d)
    p_down = 1.0-p_up
    if DEBUG and 0:
        print('u: %6.5f, d: %6.5f' % (u, d))
        print('p: %6.5f, (1-p): %6.5f' % (p_up, p_down))
        print('R: %6.5f, Rinv: %6.5f' % (R, Rinv))
    # price of underlying
    prices = [0.0 for j in range(steps+1)]
    # fill in the endnodes.
    prices[0] = S * math.pow(d, steps)
    for i in range(1,steps+1):
        prices[i] = uu*prices[i-1]
    # value of corresponding call
    put_values = [0.0 for j in range(steps+1)]
    # print_values = [[] for j in range(steps+1)]
    for i in range(steps+1):
        # PUT payoffs at maturity
        put_values[i] = max(0.0, (X-prices[i]))
    for step in range(steps-1,-1,-1):
        for i in range(steps):
            put_values[i] = (p_up*put_values[i+1]+p_down*put_values[i])*Rinv
    return put_values[0]

if __name__=="__main__":
    DEBUG = 1
    from finrecipes.black_scholes_put import *
    print('Test for function option_price_put_european_binomial.')
    print()
    no_steps = 10
    S = 100.0
    X = 100.0
    r = 0.025
    sigma = 0.2
    t = 1.0
    print('comparison of accuracy for different strikes.')
    for K in range(X-20.0,X+21.0,5.0):
        print('Strike price %3.1f:' % K)
        bs_value = option_price_put_black_scholes(S, K, r, sigma, t)
        for steps in range(5,201,5):
            value = option_price_put_european_binomial(S, K, r, sigma, t, steps)
            print('Cox-Ross Tree with %d nodes: %9.6f, analytically %9.6f. Accuracy %1.6f percent.' \
                  % (steps, value, bs_value, (value-bs_value)/bs_value*100.0))
        print()
        print()
