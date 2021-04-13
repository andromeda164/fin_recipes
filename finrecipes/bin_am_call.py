""" ******************************************************

    Bewertungsfunktion fuer amerikanische Call-Optionen
    via Binomial Tree (normaler Cox-Ross Tree).

    Beschreibung:   Bewertungsfunktion fuer amerikanische
                    Call-Optionen via Binomial Tree
                    (recombining). Es handelt sich um einen
                    normalen Cox-Ross Tree.

                    Alle Parameter (u, d, p) werden aus S, X,
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

def option_price_call_american_binomial(S, X, r, sigma, t, steps):
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
    call_values = [0.0 for j in range(steps+1)]
    # print_values = [[] for j in range(steps+1)]
    for i in range(steps+1):
        # CALL payoffs at maturity
        call_values[i] = max(0.0, (prices[i]-X))
    for step in range(steps-1,-1,-1):
        for i in range(steps):
            call_values[i] = (p_up*call_values[i+1]+p_down*call_values[i])*Rinv
            # check for early exercise possibility, condition for american valuation
            # condition: call value < intrinsic value
            prices[i] = d*prices[i+1]
            call_values[i] = max(call_values[i], prices[i]-X)
    return call_values[0]

if __name__=="__main__":
    DEBUG = 1
    from finrecipes.anal_price_am_call_div import *
    print('Test for function option_price_call_american_binomial.')
    print()
    no_steps = 10
    S = 100.0
    X = 100
    r = 0.025
    sigma = 0.2
    t = 1.0
    D1 = 0.0
    print('comparison of accuracy for different strikes.')
    for K in range(X-20,X+21,5):
        print('Strike price %3.1f:' % (K))
        bs_value = option_price_american_call_one_dividend(S,K,r,sigma,t,D1,t)
        for steps in range(5,201,5):
            value = option_price_call_american_binomial(S, K, r, sigma, t, steps)
            print('Cox-Ross Tree with %d nodes: %9.6f, analytically %9.6f. Accuracy %1.6f percent.' \
                  % (steps, value, bs_value, (value-bs_value)/bs_value*100.0))
        print()
        print()

