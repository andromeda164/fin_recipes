""" ******************************************************

    Zufallsvariablen-Generator mit Standard-Normalverteilung.
    Basierend auf random_uniform_0_1().

    Beschreibung:   Die Funktion gibt fuer jeden Funktions-
                    aufruf eine neue, normalverteilte
                    Zufallszahl zurueck.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur       OK          
*******************************************************"""
from random_uniform import *
import math, functools, numpy

def random_normal():
    U1 = 0.0
    U2 = 0.0
    V1 = 0.0
    V2 = 0.0
    S = 2.0
    X1 = 0.0
    while S >= 1.0:
        U1 = random_uniform_0_1()
        U2 = random_uniform_0_1()
        V1 = 2.0*U1-1.0
        V2 = 2.0*U2-1.0
        S = math.pow(V1,2) + math.pow(V2,2)
    X1 = V1 * math.sqrt((-2.0 * math.log(S)) / S)
    return X1

if __name__=='__main__':
    #import Numeric
    # Testing
    MAXINDEX = 100000
    print('Test program for the calculations')
    print('%d random numbers generated:' % MAXINDEX)
    results = numpy.zeros((MAXINDEX))
    for i in range(MAXINDEX):
        results[i] = random_normal()
    print('Mean %1.6f, Variance %1.6f' \
          % (numpy.average(results), numpy.var(results)))
    #functools.reduce(functools.add,pow(results-Numeric.average(results),2.0)) / (len(results)-1) ))
