""" ******************************************************

    Dichtefunktion der Standard-Normalverteilung.

    Beschreibung:   Dichtefunktion der Standard-Normalverteilung.
                    Verifizierung mit Werten von Excel.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    z               float       Quantil der Standard-
                                Normalverteilung
    
    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   OK          Verifiziert mit Werten be-
                                rechnet mit Excel.
*******************************************************"""
import math

PI = 3.141592653589793238462643

def n(z):
    """ normal distribution function """
    return (1.0/math.sqrt(2.0*PI))*math.exp(-0.5*z*z)

if __name__=="__main__":
    print "Test for normal distribution."
    print 'Values taken from Excel.'
    print
    X = [-3, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    norm = [0.004431848,0.0175283,0.053990967,0.129517596,0.241970725, \
            0.352065327,0.39894228,0.352065327,0.241970725,0.129517596, \
            0.053990967,0.0175283,0.004431848]
    for i in range(len(X)):
        print 'n(%3.2f) should be %6.6f. Calculated value: %6.6f.' \
              % (X[i], norm[i], n(X[i]))
    print 'OK.'

