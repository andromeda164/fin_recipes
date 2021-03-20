""" ******************************************************

    Simulierte Lognormalverteilte Zufallsvariable
    Start bei S.


    

    Beschreibung:   Die Funktion gibt simulierte Lognormal-
                    verteilte Zahlen zurueck (mit Zins be-
                    rechnet!)
                    Es wird das Python-Standardmodul random
                    benuetzt.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    S               Float       current value of variable
    r               Float       Zinssatz
    sigma           Float       Volatility
    time            Float       Zeitschritt fuer 1 step
    
    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur       --          
*******************************************************"""
import math, random

def simulate_lognormal_random_variable(S,r, sigma, time):
    R = (r - 0.5 * math.pow(sigma,2) )*time
    SD = sigma * math.sqrt(time)
    return S * math.exp(R + SD * random.normalvariate( 0.0, 1.0)) 


if __name__=="__main__":
    print 'Testing of random Log-normal-distributed Series'
    numtrials = 10000
    numsteps = 1000
    S = 100.0
    r = 0.02
    sigma = 0.20
    time = 0.001
    value = 0.0
    i = 0
    values = []
    mean = 0.0
    cumsum = 0.0
    for j in range(numtrials):
        value = S
        for i in range(numsteps):
            value = simulate_lognormal_random_variable(value,r,sigma,time)
        values.append(value)
    mean = sum(values) / len(values)
    for ele in values:
        cumsum += (ele - mean) ** 2.0
    print 'Testing a simulation path, starting at %4.2f, growing at %4.2f percent/y.' % (S, r*100.0)
    print 'Volatility (annualized) is %4.2f percent. Simulation over %4.2f years.' \
          % (sigma*100.0, time*numsteps)
    print 'The mean is %5.4f. At theoretical growth should be %5.4f.' \
          % (mean, S*math.exp(r*time*numsteps))
    print 'The standard-deviation, calculated from %d samples is %6.4f.' \
          % (numtrials, math.sqrt(cumsum / (float(numtrials - 1))))

