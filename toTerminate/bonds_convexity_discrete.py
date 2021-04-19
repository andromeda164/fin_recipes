""" ******************************************************

    Bond-Konvexitaet.

    Beschreibung:   Funktion zur Berechnung der Konvexitaet
                    eines Bonds.

                    Normale Bond-Konvexitaets-Formel fuer
                    den produktiven Einsatz
                    
                    Der Zinssatz r (IRR) muss vorgaengig
                    DISKRET verzinst worden sein.
                    Siehe S. 28 des Manuals fuer die
                    Berechnungsformeln.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    times           List        Liste aller Zahlungs-
                                zeitpunkte
    cashflows       List        Liste aller Cash Flows
    r               Float       Zinssatz, 0.05 fuer 5%,
                                IRR, DISKRET ver-
                                zinst.

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       --
    Testprogramm    --
    Literatur-Ref   --
*******************************************************"""
import math
from bonds_price_discrete import *
from Numeric import *

def bonds_convexity_discrete(times, cashflows, r):
    B = 0.0
    Cx = 0.0
    for i in range(len(times)):
        Cx += cashflows[i]*times[i]*(times[i]+1.0) / (math.pow((1.0+r),times[i]))
    B = bonds_price_discrete(times, cashflows, r)
    print(B , 'FALSCH HIER!!!')
    
    return (Cx/(math.pow(1.0+r, 2.0))) / B

if __name__=='__main__':
    # Testing

    print('Test program for the calculations')
    print('See p. 44-46 of manual.')
    coupon = 0.1
    times = [1.0, 2.0]
    cashflows = [coupon, 1.0+coupon]
    r = 0.1
    r_cont = math.log(1.0+r/100.0)*100.0
    print()
    print('Interest rate %2.2f, continuously compounded %2.6f' \
          %  (r*100.0, r_cont*100.0))
    print('Coupon rate of Bond: %2.2f' % (coupon*100.0))
    print('Convexity: %3.5f' % bonds_convexity_discrete(times, cashflows, r))

    print()
    print('Test program 2 with data from literature')
    print('FIN 509. Duration and Convexity - Prof. Jonathan M. Karpoff.')
    cflow_times = arange(0.5, 20.5,0.5)
    cflow_amounts = zeros((40), Float) + 90.0
    cflow_amounts[39] = 1090.0
    price = 1346.722
    zins = 0.06
    zins_cont = math.log(1.0 + zins)
    result = bonds_convexity_discrete(cflow_times, cflow_amounts, zins)
    print('Interest rate: Annually %1.6f, Continuously %1.6f' % \
          (zins, zins_cont))
    print('Cash Flows:')
    for i in range(len(cflow_times)):
        print('CF at %2.1f:\t%9.1f, \tPV: %9.2f, \tt * PV(CF): %9.2f' \
              % (cflow_times[i], cflow_amounts[i], \
                 cflow_amounts[i] * math.pow(1+zins, -cflow_times[i]), \
                cflow_amounts[i] * math.pow(1+zins, -cflow_times[i]) * cflow_times[i]))
    print('Result should be 164.106!')
    print('Result calculated with discretely compounded rate of %1.6f: %3.5f' % (zins, result))
