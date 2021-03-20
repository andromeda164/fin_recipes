""" ******************************************************

    Funktion zur Payoff-Berechnung von Asian Options.
    
    Beschreibung:   Berechnung des Payoffs fuer Plain Vanilla
                    Asian Options (arithmetic/geometric
                    average).

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    prices          list of     Preis-Sequenz
                    floats

    X               float       Strike
        
    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   --
*******************************************************"""
import fin_recipes, math

def add(x,y): return x+y

def payoff_arithmetric_average_call(prices, X):
    sum = float(reduce(add, prices))
    avg = sum/float(len(prices))
    return max(0.0,avg-X)

def payoff_geometric_average_call(prices, X):
    logsum = math.log(prices[0])
    for i in range(1,len(prices)):
        logsum += math.log(prices[i])
    avg = math.exp(logsum/len(prices))
    return max(0.0,avg-X)

def payoff_bermudan_arithmetic_average_call(sampling_indexes, prices, X):
    slice = []
    for i in sampling_indexes:
        slice.append(prices[i])
    sum = float(reduce(add, slice))
    avg = sum/float(len(slice))
    return max(0.0,avg-X)

def payoff_scaled_bermudan_arithmetic_average_call(sampling_indexes, \
                                                   prices, X, scale):
    slice = []
    for i in sampling_indexes:
        slice.append(prices[i])
    sum = float(reduce(add, slice))
    avg = sum/float(len(slice))
    return max(0.0,avg-X)*scale
   

if __name__=='__main__':
    print 'Testing Asian payoffs.'
    prices = range(20,41)
    fx_rates = range(0,21)
    X = 27.0
    scale = 0.1
    print 'The price sequence is %s.' % str(prices)
    print 'The arithmetic average is %5.3f.' % (float(reduce(add,prices))/float(len(prices)))
    print 'The arithmetic Asian call payoff for Strike %5.3f is %5.3f.' \
          % (X, payoff_arithmetric_average_call(prices, X))
    print 'The theoretical result is %5.3f.' % (float(reduce(add,prices))/float(len(prices))-X)
    print 'The difference is %5.3f.' \
          % (payoff_arithmetric_average_call(prices, X) - (float(reduce(add,prices))/float(len(prices))-X))
    print 'OK'
    print 'The same payoff geometrically calculated is %5.3f' \
          % (payoff_geometric_average_call(prices, X))
    sampling_indexes = [10,12,14,16]
    sampling_values = []
    for i in sampling_indexes:
        sampling_values.append(prices[i])
    value = payoff_scaled_bermudan_arithmetic_average_call(sampling_indexes, prices, X, 1.0)
    print 'The bermudan payoff for the sampling indexes %s \nwith the values %s is %5.3f' % (sampling_indexes, sampling_values, value)

    value = payoff_scaled_bermudan_arithmetic_average_call(sampling_indexes, prices, X, scale)
    print 'The bermudan payoff with scale %5.3f for the sampling indexes %s \nwith the values %s is %5.3f' % (scale, sampling_indexes, sampling_values, value)
    value = payoff_bermudan_arithmetic_average_call(sampling_indexes, prices, X)
    print 'This is the same as the payoff without scale times the scale (%5.3f).' % (value*scale)

    value = payoff_bermudan_arithmetic_average_call_single_asset( \
        sampling_indexes, prices, fx_rates, X*10.0)
    print 'The bermudan payoff for the sampling indexes %s \nwith the values %s is %5.3f' % (sampling_indexes, sampling_values, value)
