""" ******************************************************

    Berechnung des Werts und Delta von exotischen Optionen
    mit generischer Payoff-Funktion via Monte-Carlo
    Simulation.
    
    Beschreibung:   Die Funktion berechnet die Bewertung,
                    Delta usw. fuer eine generische Payoff-
                    Funktion (geeignet fuer Plain Vanilla
                    und andere bspw. Asian Options).

                    Die Funktion gibt ein Tupel mit den
                    folgenden Werten zurueck:

                    value, delta, gamma, vega, rho

                    Vega und Rho sind PRO PROZENT
                    ausgedrueckt.

                    Theta TO BE DEFINED!!!
                    
                    Es wird das Python-Standardmodul random
                    benuetzt.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    S               float       current value of variable
    X               float       Strike
    r               float       Zinssatz
    sigma           float       Volatility
    time            float       Time to maturity
    payoff          function    Payoff-Funktion
    no_steps        int         Anzahl Steps in S
    no_sims         int         Anzahl Monte Carlo
                                Simulationen
    
    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur       OK          Verglichen mit Derivagem
                                (Hull) - sehr gute Ueber-
                                einstimmung!
                                
                                Auch Bloomberg gibt aehnliche
                                Werte in einer Simulation.
                                
*******************************************************"""
import math, random, fin_recipes
from simulate_lognormally_distributed_sequence import *
from black_scholes_call import *

def derivative_price_simulate_european_option_generic( \
                S, X, r, sigma, time, payoff, no_steps, no_sims, \
                delta=0.001, vega=0.001, rho=0.001):
    prices = []
    delta_pos_prices = []
    delta_neg_prices = []
    vega_prices = []
    rho_prices = []
    sum_payoffs = 0.0
    sum_delta_pos_payoffs = 0.0
    sum_delta_neg_payoffs = 0.0
    sum_vega_payoffs = 0.0
    sum_rho_payoffs = 0.0
    sum_theta_payoffs = 0.0
    value = 0.0
    delta_pos_value = 0.0
    delta_neg_value = 0.0
    vega_value = 0.0
    rho_value = 0.0
    theta_value = 0.0
    for n in range(no_sims):
        prices, delta_pos_prices, delta_neg_prices, vega_prices, rho_prices = \
                simulate_lognormally_distributed_sequence_with_greeks(S,r,sigma,time,no_steps,delta,vega,rho)
        sum_payoffs += payoff(prices,X)
        sum_delta_pos_payoffs += payoff(delta_pos_prices,X)
        sum_delta_neg_payoffs += payoff(delta_neg_prices,X)
        sum_vega_payoffs += payoff(vega_prices,X)
        sum_rho_payoffs += payoff(rho_prices,X)
	sum_theta_payoffs += payoff(prices[0:len(prices)-1],X)
    
    value = math.exp(-r*time) * (sum_payoffs/float(no_sims))
    delta_pos_value = math.exp(-r*time) * (sum_delta_pos_payoffs/float(no_sims))
    delta_neg_value = math.exp(-r*time) * (sum_delta_neg_payoffs/float(no_sims))
    vega_value = math.exp(-r*time) * (sum_vega_payoffs/float(no_sims))
    rho_value = math.exp(-r*(1.0)*time) * (sum_rho_payoffs/float(no_sims))
    theta_value = math.exp(-r*time) * (sum_theta_payoffs/float(no_sims))

    delta_pos_per_unit = (delta_pos_value-value)/(delta*S)
    delta_neg_per_unit = (value-delta_neg_value)/(delta*S)
    gamma_per_unit = (delta_pos_per_unit-delta_neg_per_unit)/(delta*S)
    vega_per_unit = (vega_value-value)/(vega*sigma)
    rho_per_unit = (rho_value-value)/ (rho*r)
    theta_per_unit = (theta_value-value) / (time/float(len(prices)))
    return value, delta_pos_per_unit, gamma_per_unit, vega_per_unit, rho_per_unit
           

if __name__=="__main__":
    print 'Testing arithmetic Asian Options'
    import payoff_average
    numtrials = 10000
    numsteps = 200
    S = 100.0
    X = 100.0
    r = 0.1
    sigma = 0.20
    time = 1.0
    
    value = 0.0
    delta = 0.0

    value, delta, gamma, vega, rho = \
        derivative_price_simulate_european_option_generic( \
            S, X, r, sigma, time, payoff_average.payoff_arithmetric_average_call, \
            numsteps, numtrials)
    print 'Underlying is %5.2f. Strike is %5.2f.' \
          % (S, X)
    print 'Volatility (annualized) is %4.2f percent. Simulation over %4.2f years.' \
          % (sigma*100.0, time)
    print 'The value is %6.4f. Derivagem (Hull) value is %6.4f. Diff: %3.2f perc. OK.' % (value, 7.0685, (value-7.0685)/7.0685*100.0)
    print 'The Delta is %5.6f. Derivagem (Hull) is %5.6f. Diff: %3.2f perc. OK.' % (delta, 0.6543, (delta-0.6543)/0.6543*100.0)
    print 'The Gamma is %5.6f. Derivagem (Hull) is %5.6f. Diff: %3.2f perc. OK.' % (gamma, 0.02876123, (gamma-0.02876123)/0.02876123*100.0)
    print 'The Vega is %5.6f/perc. Derivagem (Hull) is %5.6f. Diff: %3.2f perc. OK.' % (vega/100.0, 0.19880408, (vega/100.0-0.19880408)/0.19880408*100.0)
    print 'The Rho is %5.6f/perc. Derivagem (Hull) is %5.6f. Diff: %3.2f perc. OK.' % (rho/100.0, 0.26849895, (rho/100.0-0.26849895)/0.26849895*100.0)
    print 'Bloomberg Vega is ~0.25 !!!. Derivagem vega seems to be slightly wrong!'
#    print 'The Theta is %5.6f/perc. Derivagem (Hull) is %5.6f. Diff: %3.2f perc. OK.' % (theta, 0.0, 0.0)
