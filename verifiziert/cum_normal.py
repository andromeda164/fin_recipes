# -*- coding: cp1252 -*-
""" ******************************************************

    Kumulierte Normalverteilung. Numerische Naeherungs-
    formel (wahrscheinlich nach Abramowiz and Stegun [1964]).

    Beschreibung:   Die Funktion gibt die angenaeherte,
                    kumulative Normalverteilung zurueck.
                    Siehe S. 163 des Manuals.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    z               Float       Dichtefunktion der
                                Normalverteilung
    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur       OK          Verifiziert mit Formeltafel
                                Werte im Testprogramm!
*******************************************************"""
import math

def N(z):
    if z >  6.0:  return 1.0  # this guards against overflow 
    if z < -6.0:  return 0.0

    b1 =  0.31938153 
    b2 = -0.356563782 
    b3 =  1.781477937
    b4 = -1.821255978
    b5 =  1.330274429 
    p  =  0.2316419 
    c2 =  0.3989423 

    a = abs(z) 
    t = 1.0/(1.0+a*p) 
    b = c2*math.exp((-z)*(z/2.0)) 
    n = ((((b5*t+b4)*t+b3)*t+b2)*t+b1)*t 
    n = 1.0-b*n 
    if z < 0.0: n = 1.0 - n 
    return n 

if __name__=='__main__':
    # Testing
    print 'Test program for the calculations'
    args = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    results = [0.5, 0.5+0.19146, 0.5+0.34134, 0.5+0.43319, 0.5+0.47725, \
               0.5+0.49379, 0.5+0.49865, 0.5+0.49977, 0.5+0.49997]
    for index in range(len(args)):
        print 'N(%1.2f):\t%1.6f\tagainst %1.6f' % (args[index], results[index],N(args[index]))
    print 'all negative:'
    for index in range(len(args)):
        print 'N(%1.2f):\t%1.6f\tagainst %1.6f' % (-args[index], 1.0-results[index],N(-args[index]))

