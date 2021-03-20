""" ******************************************************

    Bond-Konvexitaet.

    Beschreibung:   Funktion zur Berechnung der Konvexitaet
                    eines Bonds.
                    
                    Der Zinssatz r muss vorgaengig
                    kontinierlich verzinst worden sein.
                    Siehe S. 28 des Manuals fuer die
                    Berechnungsformeln.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    times           List        Liste aller Zahlungs-
                                zeitpunkte
    cashflows       List        Liste aller Cash Flows
    r               Float       Zinssatz, 0.05 fuer 5%,
                                IRR, kontinuierlich ver-
                                zinst.

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK          Nach Testprogramm p. 46
    Literatur-Ref   OK
*******************************************************"""
import math
from bonds_price import *

def bonds_convexity(times, cashflows, r):
    C = 0.0
    B = 0.0
    for i in range(len(times)):
	C += cashflows[i] * math.pow(times[i],2.0) * math.exp(-r*times[i])
    B = bonds_price(times, cashflows,r)
    return C/B

if __name__=='__main__':
    # Testing

    print 'Test program for the calculations'
    print 'See p. 44-46 of manual.'
    coupon = 0.1
    times = [1.0, 2.0]
    cashflows = [coupon, 1.0+coupon]
    r = 0.1
    r_cont = math.log(1.0+r/100.0)*100.0
    print
    print 'Interest rate %2.2f, continuously compounded %2.6f' \
          %  (r*100.0, r_cont*100.0)
    print 'Coupon rate of Bond: %2.2f' % (coupon*100.0)
    print 'Convexity: %3.5f' % bonds_convexity(times, cashflows, r_cont)

