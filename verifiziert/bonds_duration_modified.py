""" ******************************************************

    Modified Bond Duration. Berechnung mit diskreten
    Cashflow-Payments.
    
    DISKRETE Verzinsung.

    Beschreibung:   Funktion zur Berechnung der
                    Modified Duration eines Bonds.

                    DISKRETE Verzinsung der IRR.

                    Fuer Produktiveinsaetze geeignet.
                    
    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    times           List        Liste aller Zahlungs-
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
    Literatur-Ref   OK          Verifiziert mit Literatur.
*******************************************************"""
import math
from bonds_yield_discrete import *
from bonds_duration_discrete import *

def bonds_duration_modified_discrete(times, cashflows, bond_price):
    y = 0.0
    D = 0.0
    y = bonds_yield_to_maturity_discrete(times, cashflows, bond_price)
    D = bonds_duration_discrete(times, cashflows, y)
    return D/(1+y)

if __name__=='__main__':
    # Testing
    print 'Test program for the calculations'
    print 'Modified Duration (discretely compounded), see page 21 of manual.'
    cflow_times = [1.0, 2.0, 3.0, 4.0]
    cflow_amounts = [50.0,50.0,50.0,1050.0]
    price = 1000.0
    zins = bonds_yield_to_maturity_discrete(cflow_times, cflow_amounts, price)
    zins_cont = math.log(1.0 + zins)
    result = bonds_duration_modified_discrete(cflow_times, cflow_amounts, price)
    print 'Interest rate: Annually %1.6f, Continuously %1.6f' % \
          (zins, zins_cont)
    print 'Bond Price %3.2f' % (price)
    print 'Cash Flows:'
    t_PV = 0.0
    PV = 0.0
    for i in range(len(cflow_times)):
        t_PV += cflow_amounts[i] / math.pow(1.0+zins,cflow_times[i]) * cflow_times[i]
        PV += cflow_amounts[i] / math.pow(1.0+zins,cflow_times[i])
        print 'CF at %2.1f:\t%9.1f, \tPV: %9.2f, \tt * PV(CF): %9.2f' \
              % (cflow_times[i], cflow_amounts[i], \
                 cflow_amounts[i] / math.pow(1.0+zins,cflow_times[i]), \
                cflow_amounts[i] / math.pow(1.0+zins,cflow_times[i]) * cflow_times[i])
    print 'Result should be %2.5f!' % (t_PV / PV / (1.0 + zins))
    print 'Result calculated with discretely compounded rate of %1.6f: %2.5f' % (zins, result)

    print
    print 'Test program 2 with data from literature'
    print 'FIN 509. Duration and Convexity - Prof. Jonathan M. Karpoff.'
    cflow_times = [1.0, 2.0, 3.0]
    cflow_amounts = [100.0,100.0,1100.0]
    price = 1078.7
    zins = 0.07
    zins_cont = math.log(1.0 + zins)
    result = bonds_duration_modified_discrete(cflow_times, cflow_amounts, price)
    print 'Interest rate: Annually %1.6f, Continuously %1.6f' % \
          (zins, zins_cont)
    print 'Cash Flows:'
    for i in range(len(cflow_times)):
        print 'CF at %2.1f:\t%9.1f, \tPV: %9.2f, \tt * PV(CF): %9.2f' \
              % (cflow_times[i], cflow_amounts[i], \
                 cflow_amounts[i] * math.pow(1+zins, -cflow_times[i]), \
                cflow_amounts[i] * math.pow(1+zins, -cflow_times[i]) * cflow_times[i])
    print 'Result should be 2.5661!'
    print 'Result calculated with discretely compounded rate of %1.6f: %2.5f' % (zins, result)

