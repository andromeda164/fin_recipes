""" ******************************************************

    Put Option-Preis basieren auf Black&Scholes mit
    kontinuierlicher Dividendenrendite.

    Beschreibung:   Funktion zur Berechnung des theoretischen
                    Preises einer Put-Option mittels
                    klassischer Black&Scholes-Formel mit
                    kontinuierlicher Dividendenrendite

                    Der Zinssatz r (auch b!) muss vorgaengig
                    KONTINUIERLICH verzinst worden sein.
                    Siehe S. 28 des Manuals fuer die
                    Berechnungsformeln.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    S               float       Spot (Underlying) price
    K               float       Strike price
    r               float       interest rate
                                (continuously compounded!)
    q               float       yield on underlying
                                (continuously compounded!)
    sigma           float       volatility
    time            float       time to maturity

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       --
    Testprogramm    --
    Literatur-Ref   --
*******************************************************"""
import math
import fin_recipes
import normdist
import cum_normal

def option_price_european_put_payout(S, K, r, q, sigma, time):
    sigma_sqr = math.pow(sigma,2.0)
    time_sqrt = math.sqrt(time)
    d1 = (math.log(S/K) + (r-q + 0.5*sigma_sqr)*time)/(sigma*time_sqrt)
    d2 = d1-(sigma*time_sqrt)
    put_price = K * math.exp(-r*time)*cum_normal.N(-d2)-S*math.exp(-q*time)*cum_normal.N(-d1)
    return put_price

if __name__=="__main__":
    print 'Test of Put-Option - european style with continuous dividend yield.'
    S = 100.0
    K = 100.0
    r = 0.1
    sigma = 0.25
    time = 1.0
    q = 0.05
    value = option_price_european_put_payout(S, K, r, q, sigma, time)
    print 'The value of a european call option with a continuous dividend yield of %6.2f should be %6.6f.' % (q, value)
    print 'Derivagem gives %6.6f.' % 0.0

