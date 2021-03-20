""" ******************************************************

    Simulierte Lognormalverteilte Zufallsvariable
    Start bei S.

    Beschreibung:   Aehnlich wie simulate_lognormal_random_
                    variable(...), nur werden alle Zahlen
                    automatisch mit Hilfe der Anzahl Steps
                    automatisch berechnet.

                    Die zweite Version der Funktion gibt einen
                    um Delta abweichenden Zufallszahlenstrom
                    zurueck
                    (basierend auf denselben Zufallszahlen).
                   
                    Es wird das Python-Standardmodul random
                    benuetzt.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    S               float       current value of underlying
    r               float       Zinssatz
    sigma           float       Volatility
    time            float       Zeit bis Payoff
    no_steps        integer     Anzahl Steps (time UND S!)
    delta           float       Delta fuer die 2. Serie
                                zur Deltaberechnung des
                                Derivats.
    
    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur       --          
*******************************************************"""
import math, random

def simulate_lognormally_distributed_sequence(S, r, sigma, time, no_steps):
    prices = []
    delta_t = float(time)/float(no_steps)
    R = (r-0.5*math.pow(sigma,2))*delta_t
    SD = sigma * math.sqrt(delta_t)
    S_t = S  # initialize at current price
    for i in range(no_steps):
        rand = random.normalvariate( 0.0, 1.0)
        S_t = S_t * math.exp(R + SD * rand)
        prices.append(S_t)
    return prices

def simulate_lognormally_distributed_sequence_with_greeks( \
    S, r, sigma, time, no_steps, delta=0.001, vega=0.001, rho=0.001):
    prices = []
    delta_pos_prices = []
    delta_neg_prices = []
    vega_prices = []
    rho_prices = []
    delta_t = float(time)/float(no_steps)

    R = (r-0.5*math.pow(sigma,2))*delta_t
    R_rho = (r*(1.0+rho)-0.5*math.pow(sigma,2))*delta_t

    SD = sigma * math.sqrt(delta_t)
    SD_vega = sigma*(1.0+vega) * math.sqrt(delta_t)

    S_t = S  # initialize at current price
    # initialize delta (positive deviation) at current price
    S_delta__pos_t = S*(1.0+delta)
    # initialize delta (negative deviation) at current price
    S_delta__neg_t = S*(1.0-delta) 
    S_vega_t = S
    S_rho_t = S
    for i in range(no_steps):
        rand = random.normalvariate( 0.0, 1.0)

        S_t = S_t * math.exp(R + SD * rand)
        S_delta__pos_t = S_delta__pos_t * math.exp(R + SD * rand)
        S_delta__neg_t = S_delta__neg_t * math.exp(R + SD * rand)
        S_vega_t = S_vega_t * math.exp(R + SD_vega * rand)
        S_rho_t = S_rho_t * math.exp(R_rho + SD * rand)
        
        prices.append(S_t)
        delta_pos_prices.append(S_delta__pos_t)
        delta_neg_prices.append(S_delta__neg_t)
        vega_prices.append(S_vega_t)
        rho_prices.append(S_rho_t)
    
    return prices, delta_pos_prices, delta_neg_prices, \
           vega_prices, rho_prices

def simulate_lognormally_distributed_sequence_with_greeks_and_randoms( \
    randomNumbers, S, r, sigma, time, no_steps, delta=0.001, vega=0.001, rho=0.001):
    prices = []
    delta_pos_prices = []
    delta_neg_prices = []
    vega_prices = []
    rho_prices = []
    delta_t = float(time)/float(no_steps)

    R = (r-0.5*math.pow(sigma,2))*delta_t
    R_rho = (r*(1.0+rho)-0.5*math.pow(sigma,2))*delta_t

    SD = sigma * math.sqrt(delta_t)
    SD_vega = sigma*(1.0+vega) * math.sqrt(delta_t)

    S_t = S  # initialize at current price
    # initialize delta (positive deviation) at current price
    S_delta__pos_t = S*(1.0+delta)
    # initialize delta (negative deviation) at current price
    S_delta__neg_t = S*(1.0-delta) 
    S_vega_t = S
    S_rho_t = S
    for i in range(no_steps):
        rand = randomNumbers[i] #random.normalvariate( 0.0, 1.0)

        S_t = S_t * math.exp(R + SD * rand)
        S_delta__pos_t = S_delta__pos_t * math.exp(R + SD * rand)
        S_delta__neg_t = S_delta__neg_t * math.exp(R + SD * rand)
        S_vega_t = S_vega_t * math.exp(R + SD_vega * rand)
        S_rho_t = S_rho_t * math.exp(R_rho + SD * rand)
        
        prices.append(S_t)
        delta_pos_prices.append(S_delta__pos_t)
        delta_neg_prices.append(S_delta__neg_t)
        vega_prices.append(S_vega_t)
        rho_prices.append(S_rho_t)
    
    return prices, delta_pos_prices, delta_neg_prices, \
           vega_prices, rho_prices

if __name__=="__main__":
    print 'Testing of random Log-normal-distributed Series'
    def add(a,b): return a+b
    numsteps = 200
    numtrials = 10000
    S = 100.0
    r = 0.02
    sigma = 0.20
    time = 1.0
    values = []
    mean = 0.0
    cumsum = 0.0
    for j in range(numtrials):
        prices = simulate_lognormally_distributed_sequence( \
            S,r,sigma,time,numsteps)
        values.append(prices[len(prices)-1])
    mean = float(reduce(add,values)) / float(len(values))
    for ele in values:
        cumsum += (ele - mean) ** 2.0
    print 'Testing a simulation path, starting at %4.2f, growing at %4.2f percent/y.' % (S, r*100.0)
    print 'Volatility (annualized) is %4.2f percent. Simulation over %4.2f years.' \
          % (sigma*100.0, time)
    print 'The mean is %5.4f. At theoretical growth should be %5.4f.' \
          % (mean, S*math.exp(r*time))
    print 'The standard-deviation, calculated from %d samples is %6.4f.' \
          % (numtrials, math.sqrt(cumsum / (float(numtrials - 1))))
    print

    
    print 'Testing of greek series produced'
    delta = 0.01
    vega = 0.01
    rho = 0.01
    values = []
    values_vega = []
    values_rho = []
    mean = 0.0
    mean_vega = 0.0
    mean_rho = 0.0
    cumsum = 0.0
    cumsum_vega = 0.0
    cumsum_rho = 0.0
    for j in range(numtrials):
        prices, delta_pos_prices, delta_neg_prices, vega_prices, rho_prices = \
                simulate_lognormally_distributed_sequence_with_greeks( \
                    S,r,sigma,time,numsteps,delta,vega,rho)
        values.append(prices[len(prices)-1])
        values_vega.append(vega_prices[len(vega_prices)-1])
        #values_rho.append(values_rho[len(values_rho)-1])
    mean = float(reduce(add,values)) / float(len(values))
    mean_vega = float(reduce(add,values_vega)) / float(len(values_vega))
    #mean_rho = float(reduce(add,values_rho)) / float(len(values_rho))
    for ele in values: cumsum += (ele - mean) ** 2.0
    for ele in values_vega: cumsum_vega += (ele - mean_vega) ** 2.0
    #for ele in values_rho: cumsum_rho += (ele - mean_rho) ** 2.0
    print 'Testing the simulation path, starting at %4.2f, growing at %4.2f percent/y.' % (S, r*100.0)
    print 'Volatility (annualized) is %4.2f percent. Simulation over %4.2f years.' \
          % (sigma*100.0, time)
    print 'The mean is %5.4f. At theoretical growth should be %5.4f.' \
          % (mean, S*math.exp(r*time))
    print 'The standard-deviation, calculated from %d samples is %6.4f.' \
          % (numtrials, math.sqrt(cumsum / (float(numtrials - 1))))
    print 'Vega mean is %5.4f. Std dev is %6.5f.' \
          % (mean_vega, math.sqrt(cumsum_vega / (float(numtrials - 1)))) 
