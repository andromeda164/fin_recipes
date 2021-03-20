""" ******************************************************

    Klassische Bond Duration. Berechnung mit diskreten
    Cashflow-Payments.
    
    DISKRETE Verzinsung.

    Beschreibung:   Funktion zur Berechnung der
                    Duration eines Bonds. Klassische
                    Formel

                    DISKRETE Verzinsung der IRR.

                    Fuer Produktiveinsaetze!
                    
                    Der Zinssatz r muss vorgaengig
                    DISKRET, jaehrlich verzinst worden sein.
                    Siehe S. 28 des Manuals fuer die
                    Berechnungsformeln.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    times           List        Liste aller Zahlungs-
                                zeitpunkte
    cashflows       List        Liste aller Cash Flows
    r               Float       Zinssatz, 0.05 fuer 5%,
                                IRR, DISKRET verzinst.

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   OK          Verifiziert mit Literatur.
*******************************************************"""
import math

def bonds_duration_discrete(times, cashflows,r):
    B = 0.0
    D = 0.0
    for i in range(len(times)):
        D += times[i] * cashflows[i] / math.pow(1+r,times[i])
        B += cashflows[i] / math.pow(1+r,times[i])
    return D/B

if __name__=='__main__':
    # Testing
    print('Test program for the calculations')
    print('Duration (discretely compounded), classic formula, see page 21 of manual.')
    cflow_times = [1.0, 2.0, 3.0, 4.0]
    cflow_amounts = [50.0,50.0,50.0,1050.0]
    zins = 0.05
    zins_cont = math.log(1.0 + zins)
    result = bonds_duration_discrete(cflow_times, cflow_amounts, zins)
    print('Interest rate: Annually %1.6f, Continuously %1.6f' % \
          (zins, zins_cont))
    print('Cash Flows:')
    for i in range(len(cflow_times)):
        print('CF at %2.1f:\t%9.1f, \tPV: %9.2f, \tt * PV(CF): %9.2f' \
              % (cflow_times[i], cflow_amounts[i], \
                 cflow_amounts[i] * math.pow(1+zins, -cflow_times[i]), \
                cflow_amounts[i] * math.pow(1+zins, -cflow_times[i]) * cflow_times[i]))
    print('Result should be 3.72324!')
    print('Result calculated with discretely compounded rate of %1.6f: %2.5f' % (zins, result))

    print()
    print('Test program 2 with data from literature')
    print('FIN 509. Duration and Convexity - Prof. Jonathan M. Karpoff.')
    cflow_times = [1.0, 2.0, 3.0]
    cflow_amounts = [100.0,100.0,1100.0]
    price = 1078.7
    zins = 0.07
    zins_cont = math.log(1.0 + zins)
    result = bonds_duration_discrete(cflow_times, cflow_amounts, zins)
    print('Interest rate: Annually %1.6f, Continuously %1.6f' % \
          (zins, zins_cont))
    print('Cash Flows:')
    for i in range(len(cflow_times)):
        print('CF at %2.1f:\t%9.1f, \tPV: %9.2f, \tt * PV(CF): %9.2f' \
              % (cflow_times[i], cflow_amounts[i], \
                 cflow_amounts[i] * math.pow(1+zins, -cflow_times[i]), \
                cflow_amounts[i] * math.pow(1+zins, -cflow_times[i]) * cflow_times[i]))
    print('Result should be 2.7458!')
    print('Result calculated with discretely compounded rate of %1.6f: %2.5f' % (zins, result))
