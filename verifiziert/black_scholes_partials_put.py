""" ******************************************************

    Greeks einer europaeischen Put, basierend auf
    Black & Scholes.

    Beschreibung:   Funktion zur Berechnung der Greeks
                    einer europaeischen Put, basierend
                    auf Black & Scholes.

                    Gibt saemtliche Greeks auf einmal
                    zurueck (via return-Tupel)

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
    Testprogramm    --
    Literatur-Ref   OK          DERIVAGEM (Hull)
*******************************************************"""
import math
import fin_recipes
import cum_normal
import normdist

def option_price_partials_put_black_scholes(S, K, r, sigma, time):
    time_sqrt = math.sqrt(time)
    d1 = (math.log(S/K)+r*time)/(sigma*time_sqrt) + 0.5*sigma*time_sqrt
    d2 = d1-(sigma*time_sqrt)
    Delta = -cum_normal.N(-d1)
    Gamma = normdist.n(d1)/(S*sigma*time_sqrt)
    Theta = - (S*sigma*normdist.n(d1))/(2*time_sqrt) + r*K*math.exp( -r*time)*cum_normal.N(-d2)
    Vega  = S * time_sqrt*normdist.n(d1)
    Rho   = -K*time*math.exp(-r*time)*cum_normal.N(-d2)
    return Delta, Gamma, Theta, Vega, Rho

if __name__=="__main__":
    print('Test for european Put Greeks. (B&S-Framework)')
    S = 50.0
    K = 50.0
    r = 0.1
    time = 0.5
    sigma = 0.3
    delta, gamma, theta, vega, rho = option_price_partials_put_black_scholes(S, K, r, sigma, time)
    print('Option price partial derivatives, Put option using Black Scholes.')
    print('Delta: shold be %6.6f. Calculated: %6.6f.' % (-0.366262722, delta))
    print('Gamma: shold be %6.6f. Calculated: %6.6f.' % (0.035478872, gamma))
    print('Theta: shold be %6.6f. Calculated: %6.6f.' % (-0.005092021*365.0, theta))
    print('Vega: shold be %6.6f. Calculated: %6.6f.' % (13.3045769, vega))
    print('Rho: shold be %6.6f. Calculated: %6.6f.' % (-0.106639263*100.0, rho))
    print('OK.')

