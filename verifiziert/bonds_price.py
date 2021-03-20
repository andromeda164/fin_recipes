""" ******************************************************

    Theoretischer Bond-Preis, gegeben ein EINZIGER Zinssatz
    (IRR).

    Beschreibung:   Funktion zur Berechnung des Preises
                    eines Bonds, gegegeben ein EINZIGER,
                    kontinuierlich verzinster Zinssatz
                    (IRR!).

                    Nur fuer die Verifikation der IRR
                    einsetzbar, nicht fuer andere
                    Produktiveinsaetze!
                    
                    Der Zinssatz r muss vorgaengig
                    kontinierlich verzinst worden sein.
                    Siehe S. 28 des Manuals fuer die
                    Berechnungsformeln.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    cashflow_times  List        Liste aller Zahlungs-
                                zeitpunkte
    cashflows       List        Liste aller Cash Flows
    r               Float       Zinssatz, 0.05 fuer 5%,
                                IRR, kontinuierlich ver-
                                zinst.

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   OK
*******************************************************"""
import math

def bonds_price(cashflow_times, cashflows, r):
    DEBUG = 0
    p = 0.0
    if DEBUG: print 'bonds_price (continuously compounded version):'
    for i in range(len(cashflow_times)):
	p += math.exp(-r*cashflow_times[i])*cashflows[i]
        if DEBUG: print 'Cashflow %d at time %2.2f: \t%6.4f, \tPV: %6.4f' \
                  % (i, cashflow_times[i], cashflows[i], math.exp(-r*cashflow_times[i])*cashflows[i])
    if DEBUG:
        print 'Theoretical price: %4.4f' % p
    return p

if __name__=='__main__':
    # Testing
    print 'Test program for the calculations'
    print 'bonds price (continuously compounded)'
    cflow_times = [1.0, 2.0, 3.0, 4.0]
    cflow_amounts = [50.0,50.0,50.0,1050.0]
    zins = 0.05
    zins_cont = math.log(1.0 + zins)
    result = bonds_price(cflow_times, cflow_amounts, zins_cont)
    print 'Interest rate: Annually %1.6f, Continuously %1.6f' % \
          (zins, zins_cont)
    print 'Cash Flows:'
    for index in range(len(cflow_times)):
        print 'CF at %f:\t%9.2f' % (cflow_times[index], cflow_amounts[index])
    print 'Result should be 1000.0!'
    print 'Result calculated with continously compounded rate of %1.6f: %4.2f' % (zins_cont, result)

