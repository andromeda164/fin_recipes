""" ******************************************************

    Bewertungsfunktion fuer amerikanische Call-Optionen
    via analytische Naeherungsformel (nur fuer EINE Dividende).

    Beschreibung:   Bewertungsfunktion fuer amerikanische 
                    Call-Optionen via analytische Naeherungs-
                    formel. Formel von Roll-Geske-Whaley.
                    (p. 70 im Manual).

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    S               float       Spot price, Underlying
                                zum Zeitpunkt null
    K               float       Strike
    r               float       interest rate, continuously
                                compounded
    sigma           float       volatility, 0.20 fuer 20%
    tau             float       time to maturity (years)
    tau1            float       time to dividend 1 (only one!)
    D1              float       amount of dividend

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK          Seite 73 Manual, OK, noch
                                mehr Vergleiche notwendig!
    Literatur-Ref   OK          DERIVAGEM (Hull)
*******************************************************"""
import fin_recipes
import math
from black_scholes_call import *
import cum_normal_bivariate
import cum_normal

def option_price_american_call_one_dividend(S,K,r,sigma,tau,D1,tau1):
    # check for no exercise
    if D1 <= K * (1.0-math.exp(-r*(tau-tau1))):
        return option_price_call_black_scholes( \
            S-math.exp(-r*tau1)*D1,K,r,sigma,tau)
    # decrease this for more accuracy
    ACCURACY = 1e-6
    sigma_sqr = sigma*sigma
    tau_sqrt = math.sqrt(tau)
    tau1_sqrt = math.sqrt(tau1)
    rho = - math.sqrt(tau1/tau)

    S_bar = 0.0         # first find the S_bar that solves c=S_bar+D1-K 
    S_low = 0.0         # the simplest: binomial search
    S_high = S          # start by finding a very high S above S_bar
    c = option_price_call_black_scholes(S_high,K,r,sigma,tau-tau1)
    test = c-S_high-D1+K
    while (test>0.0) and (S_high<=1e10):
        S_high *= 2.0
        c = option_price_call_black_scholes(S_high,K,r,sigma,tau-tau1)
        test = c-S_high-D1+K
    if S_high>1e10:     # early exercise never optimal, find BS value
        return option_price_call_black_scholes( \
            S-D1*exp(-r*tau1),K,r,sigma,tau)
    # now find S_bar that solves c=S_bar-D+K
    S_bar = 0.5 * S_high
    c = option_price_call_black_scholes(S_bar,K,r,sigma,tau-tau1)
    test = c-S_bar-D1+K
    while (abs(test)>ACCURACY) and ((S_high-S_low)>ACCURACY):
        if test<0.0: S_high = S_bar
        else: S_low = S_bar
        S_bar = 0.5 * (S_high + S_low)
        c = option_price_call_black_scholes(S_bar,K,r,sigma,tau-tau1)
        test = c-S_bar-D1+K
    a1 =  (math.log((S-D1*math.exp(-r*tau1))/K) +( r+0.5*sigma_sqr)*tau) / (sigma*tau_sqrt)
    a2 = a1 - sigma*tau_sqrt
    b1 = (math.log((S-D1*math.exp(-r*tau1))/S_bar)+(r+0.5*sigma_sqr)*tau1)/(sigma*tau1_sqrt)
    b2 = b1 - sigma * tau1_sqrt
    C = (S-D1*math.exp(-r*tau1)) * cum_normal.N(b1) + (S-D1*math.exp(-r*tau1)) * cum_normal_bivariate.N(a1,-b1,rho) \
      - (K*math.exp(-r*tau))*cum_normal_bivariate.N(a2,-b2,rho) - (K-D1)*math.exp(-r*tau1)*cum_normal.N(b2)
    return C

if __name__=="__main__":
    print('Test of Roll-Geske-Whaley-Formel for american Call-Options with')
    print('a single dividend.')
    S = 100.0
    K = 100.0
    r = 0.1
    sigma = 0.25
    tau = 1.0
    tau1 = 0.5
    D1 = 10.0
    value = option_price_american_call_one_dividend(S,K,r,sigma,tau,D1,tau1)
    print('The Roll-Geske-Whaley-Formula result for an example option should be 10.0166. It is %6.6f.' % value)
    print('Derivagem gives %6.6f.' % 10.00880)
