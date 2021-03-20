""" ******************************************************

    Theoretischer Bond-Preis, gegeben ein EINZIGER Zinssatz
    (IRR). Berechnung mit diskreten Cashflow-Payments und
    DISKRETEM Zinssatz.
    
    DISKRETE Verzinsung.

    Beschreibung:   Funktion zur Berechnung des Preises
                    eines Bonds, gegegeben ein EINZIGER,
                    DISKRET verzinster Zinssatz
                    (IRR!).

                    Nur fuer die Verifikation der IRR
                    einsetzbar, nicht fuer andere
                    Produktiveinsaetze!
                    
                    Der Zinssatz r muss vorgaengig
                    DISKRET verzinst worden sein.
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
    Literatur-Ref   OK
*******************************************************"""
import math

def bonds_price_discrete(times, cashflows, r):
    p = 0.0
    for i in range(len(times)):
	p += cashflows[i]/(math.pow((1+r),times[i]))
    return p

if __name__=='__main__':
    # Testing
    print 'Test program for the calculations'
    print 'bonds price (discretely compounded)'
    cflow_times = [1.0, 2.0, 3.0, 4.0]
    cflow_amounts = [50.0,50.0,50.0,1050.0]
    zins = 0.05
    zins_cont = math.log(1.0 + zins)
    result = bonds_price_discrete(cflow_times, cflow_amounts, zins)
    print 'Interest rate: Annually %1.6f, Continuously %1.6f' % \
          (zins, zins_cont)
    print 'Cash Flows:'
    for index in range(len(cflow_times)):
        print 'CF at %f:\t%9.2f' % (cflow_times[index], cflow_amounts[index])
    print 'Result should be 1000.0!'
    print 'Result calculated with discretely compounded rate of %1.6f: %4.2f' % (zins, result)

