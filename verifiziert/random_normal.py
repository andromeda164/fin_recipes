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
import math, functools, numpy, pytest

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

def test_random_normal():
    # pytest unittest
    MAXINDEX = 1000000
    # run a statistical test with MAXINDEX runs
    results = numpy.zeros((MAXINDEX))
    for i in range(MAXINDEX):
        results[i] = random_normal()
    # mean of a random normal variable should be 0
    assert round(numpy.average(results), 2) == 0.0
    # variance of a random normal variable should be 1
    assert round(numpy.var(results), 2) == 1.0
    return

if __name__=='__main__':
    # Testing
    MAXINDEX = 1000000
    print('Test program for the calculations')
    print('%d random numbers generated:' % MAXINDEX)
    results = numpy.zeros((MAXINDEX))
    for i in range(MAXINDEX):
        results[i] = random_normal()
    print('Mean %1.6f, Variance %1.6f' \
          % (numpy.average(results), numpy.var(results)))

