""" ******************************************************

    Macauley Duration mit kontinuierlichen Zinsen.

    Praktische Bedeutung dieser alternativen Formel ueberhaupt
    nicht klar!
    
    KONTINUIERLICHE Verzinsung.

    Beschreibung:   Funktion zur Berechnung der Macauley
                    Duration eines Bonds.

                    KONTINUIERLICHE Verzinsung der IRR.

                    Nicht fuer Produktiveinsaetze!
                    
                    Der Zinssatz r muss vorgaengig
                    KONTINUIERLICH verzinst worden sein.
                    Siehe S. 28 des Manuals fuer die
                    Berechnungsformeln.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    cashflow_times  List        Liste aller Zahlungs-
                                zeitpunkte
    cashflows       List        Liste aller Cash Flows
    r               Float       Zinssatz, 0.05 fuer 5%,
                                IRR, KONTINUIERLICH verzinst.

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   OK          Mit Literatur verifiziert.
*******************************************************"""
import math
from bonds_yield import *

def bonds_duration(cashflow_times, cashflows, r):
    S = 0.0
    D1 = 0.0
    for i in range(len(cashflow_times)):
        S  +=                     cashflows[i] * math.exp(-r*cashflow_times[i])
        D1 += cashflow_times[i] * cashflows[i] * math.exp(-r*cashflow_times[i])
    return D1 / S

if __name__=='__main__':
    # Testing
    print 'Test program for the calculations'
    print 'Duration (continuously compounded), NOT equal to Macauley or'
    print 'Modified Duration, see page 21 of manual.'
    cflow_times = [1.0, 2.0, 3.0, 4.0]
    cflow_amounts = [50.0,50.0,50.0,1050.0]
    zins = 0.05
    zins_cont = math.log(1.0 + zins)
    result = bonds_duration(cflow_times, cflow_amounts, zins_cont)
    print 'Interest rate: Annually %1.6f, Continuously %1.6f' % \
          (zins, zins_cont)
    print 'Cash Flows:'
    for i in range(len(cflow_times)):
        print 'CF at %2.1f:\t%9.1f, \tPV: %9.2f, \tt * PV(CF): %9.2f' \
              % (cflow_times[i], cflow_amounts[i], \
                 cflow_amounts[i] * math.exp(-zins_cont*cflow_times[i]), \
                cflow_amounts[i] * math.exp(-zins_cont*cflow_times[i]) * cflow_times[i])
    print 'Result should be 3.72324!'
    print 'Result calculated with continously compounded rate of %1.6f: %2.5f' % (zins_cont, result)

    print
    print 'Test program 2 with data from literature'
    print 'FIN 509. Duration and Convexity - Prof. Jonathan M. Karpoff.'
    cflow_times = [1.0, 2.0, 3.0]
    cflow_amounts = [100.0,100.0,1100.0]
    price = 1078.7
    zins_cont = bonds_yield_to_maturity(cflow_times, cflow_amounts, price)
    zins = 0.07
    result_compare = bonds_duration(cflow_times, cflow_amounts, zins)
    result = bonds_duration(cflow_times, cflow_amounts, zins_cont)
    print 'Interest rate: Annually %1.6f, Continuously %1.6f' % \
          (zins, zins_cont)
    print 'Bond Price %3.2f' % (price)
    print 'Cash Flows:'
    for i in range(len(cflow_times)):
        print 'CF at %2.1f:\t%9.1f, \tPV: %9.2f, \tt * PV(CF): %9.2f' \
              % (cflow_times[i], cflow_amounts[i], \
                 cflow_amounts[i] * math.exp(-zins_cont*cflow_times[i]), \
                cflow_amounts[i] * math.exp(-zins_cont*cflow_times[i]) * cflow_times[i])
    print 'Result should be %2.4f!' % 2.7458
    print 'Result calculated with discretely compounded rate of %1.6f: %2.5f' % (zins, result)

