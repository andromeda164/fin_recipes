""" ******************************************************

    Klasse currency_option_price_put_european
    fuer europaeische FX Optionen.

    Beschreibung:   Klasse zur Modellierung
                    von europaeischen FX Optionen.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    fx_pair         class instance
                                Instanz der Klasse
                                fx_pair
    

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   OK
*******************************************************"""

from fin_recipes import *
import math, cum_normal

## const double& S       // exchange_rate,
## const double& X       // exercise,
## const double& r       // r_domestic,
## const double& r_f     // r_foreign,
## const double& sigma   // volatility,
## const double& time    // time to maturity

def currency_option_price_put_european(S,X,r,r_f,sigma,time):
    sigma_sqr = sigma*sigma
    time_sqrt = math.sqrt(time)
    d1 = (math.log(S/X) + (r-r_f+(0.5*sigma_sqr)) * time)/(sigma*time_sqrt)
    d2 = d1 - sigma * time_sqrt
    return X*math.exp(-r*time)*cum_normal.N(-d2) - S * math.exp(-r_f*time)*cum_normal.N(-d1)

if __name__=="__main__":
    # Test european FX Option (Put)
    nominale = 200000
    S = 1.6010
    X = 1.5800
    r = 0.027
    r_f = 0.042
    sigma = 0.0515
    sigmas = [x*0.005+0.03 for x in range(10)]
    targets = [x*0.01+1.53 for x in range(10)]
    time = 0.5
    target_horizon = 0.25
    price = -currency_option_price_put_european(S,X,r,r_f,sigma,time)
    print 'Simulation of results - European FX Option'
    print '------------------------------------------'
    print 'Initial premium %d' % int(price*nominale)
    print '\t',
    for sigma in sigmas:
        print '%1.3f\t' % sigma ,
    print '\n',
    print '-------------------------------------------------------------------------------------'
    for target in targets:
        print '%1.4f\t' % target ,
        for sigma in sigmas:
            target_price = -currency_option_price_put_european(target,X,r,r_f,sigma,target_horizon)
            payout = max(nominale * (X-target), 0)
            print str(int((price-target_price)*nominale + payout))+'\t' ,
        print '\n',
    print '\n',
    #print int(price*nominale), int(target_price*nominale), int(nominale * (Xs-target)), int((price-target_price)*nominale + nominale * (X-target))


    # Test european FX Option (Put)
    base = 'USD'
    counter = 'CHF'
    nominale = 100000
    S = 1.0633
    X = 1.08
    r = 0.03
    r_f = 0.04
    sigma = 0.095
    sigmas = [x*0.005+sigma for x in range(-5,5)]
    targets = [x*X/200.0+X for x in range(-5.0,5.0)]
    time = 1.0
    target_horizon = 0.25
    price = -currency_option_price_put_european(S,X,r,r_f,sigma,time)
    print 'Simulation of results - European FX Option %d %s/%s' % (nominale, base, counter)
    print '------------------------------------------'
    print
    print 'Initial premium %d %s - %d %s' % (int(price*nominale), counter, int(price*nominale/S), base)
    print '\t',
    for sigma in sigmas:
        print '%1.3f\t' % sigma ,
    print '\n',
    print '-------------------------------------------------------------------------------------'
    for target in targets:
        print '%1.2f\t' % target ,
        for sigma in sigmas:
            target_price = -currency_option_price_put_european(target,X,r,r_f,sigma,target_horizon)
            payout = max(nominale * (X-target), 0)
            print str(int(((price-target_price)*nominale + payout)/S))+'\t' ,
        print '\n',
    print '\n',
    #print int(price*nominale), int(target_price*nominale), int(nominale * (Xs-target)), int((price-target_price)*nominale + nominale * (X-target))
