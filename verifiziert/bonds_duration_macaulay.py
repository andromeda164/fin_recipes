""" ******************************************************

    Macaulay Bond Duration.
    
    KONTINUIERLICHE Verzinsung.

    Beschreibung:   Funktion zur Berechnung der
                    Macaulay Duration eines Bonds.

                    KONTINUIERLICHE Verzinsung der IRR.

                    Nicht fuer Produktiveinsaetze!
                    
    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    cashflow_times  List        Liste aller Zahlungs-
                                zeitpunkte
    cashflows       List        Liste aller Cash Flows
    bond_price      Float       Preis des Bonds, bezogen
                                auf den Nominalwert (100.0
                                fuer 100 Nominalwert, 1000.0
                                fuer 1000 Nominalwert)

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   OK          Mit Literatur geprueft.
*******************************************************"""
import math
from bonds_yield import *
from bonds_duration import *

def bonds_duration_macaulay(cashflow_times, cashflows, bond_price):
    # use YTM in duration 
    y = 0.0
    y = bonds_yield_to_maturity(cashflow_times, cashflows, bond_price)
    print y, bonds_duration(cashflow_times, cashflows, y)
    return bonds_duration(cashflow_times, cashflows, y)

if __name__=='__main__':
    # Testing
    print 'Test program for the calculations'
    print 'Macaulay Duration (continuously compounded), see page 21 of manual.'
    cflow_times = [1.0, 2.0, 3.0, 4.0]
    cflow_amounts = [50.0,50.0,50.0,1050.0]
    price = 1000.0
    zins_cont = bonds_yield_to_maturity(cflow_times, cflow_amounts, price)
    zins = math.exp(zins_cont*1.0) - 1.0
    result = bonds_duration_macaulay(cflow_times, cflow_amounts, price)
    print 'Interest rate: Annually %1.6f, Continuously %1.6f' % \
          (zins, zins_cont)
    print 'Bond Price %3.2f' % (price)
    print 'Cash Flows:'
    t_PV = 0.0
    PV = 0.0
    for i in range(len(cflow_times)):
        t_PV += cflow_amounts[i] * math.exp(-zins_cont*cflow_times[i]) * cflow_times[i]
        PV += cflow_amounts[i] * math.exp(-zins_cont*cflow_times[i])
        print 'CF at %2.1f:\t%9.1f, \tPV: %9.2f, \tt * PV(CF): %9.2f' \
              % (cflow_times[i], cflow_amounts[i], \
                 cflow_amounts[i] * math.exp(-zins_cont*cflow_times[i]), \
                cflow_amounts[i] * math.exp(-zins_cont*cflow_times[i]) * cflow_times[i])
    print 'Result should be %2.5f!' % (t_PV / PV)
    print 'Result calculated with discretely compounded rate of %1.6f: %2.5f' % (zins, result)

    print
    print 'Test program 2 with data from literature'
    print 'FIN 509. Duration and Convexity - Prof. Jonathan M. Karpoff.'
    cflow_times = [1.0, 2.0, 3.0]
    cflow_amounts = [100.0,100.0,1100.0]
    price = 1078.7
    zins = bonds_yield_to_maturity(cflow_times, cflow_amounts, price)
    zins_cont = math.log(1.0 + zins)
    result_compare = bonds_duration(cflow_times, cflow_amounts, zins)
    result = bonds_duration_macaulay(cflow_times, cflow_amounts, price)
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

