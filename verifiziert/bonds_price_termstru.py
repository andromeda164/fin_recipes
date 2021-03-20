""" ******************************************************

    Theoretischer Bond-Preis, gegeben eine Zinsstruktur.
    Berechnung mit diskreten Cashflow-Payments.
    
    Funktioniert mit ALLEN Zinsstruktur-Klassen!

    Beschreibung:   Funktion zur Berechnung des Preises
                    eines Bonds, gegegeben eine komplette
                    Zinsstruktur (Termstruktur-Klasse!)

                    Unabhaengig von der Compounding
                    Frequency.

                    Fuer Produktiveinsaetze einsetzbar!
                    
    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    cashflow_times  List        Liste aller Zahlungs-
                                zeitpunkte
    cashflows       List        Liste aller Cash Flows
    d               Klasse term_structure_class und vererbte
                    Klassen, am besten geeignet
                    term_structure_class_cox_cubic_spline

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   OK
*******************************************************"""
from term_structure_class import *
from term_structure_class_cox_cubic_spline import *
from term_structure_class_cubic_spline import *

def bonds_price(cashflow_times, cashflows, d):
    p = 0.0
    for i in range(len(cashflow_times)):
        p += d.discount_factor(cashflow_times[i])*cashflows[i]
    return p

if __name__=='__main__':
    # Testing
    print 'Test program for the calculations'
    print 'bonds price (with Term structure)'
    cflow_times = [1.0, 2.0, 3.0, 4.0]
    cflow_amounts = [50.0,50.0,50.0,1050.0]
    times = [0.0, 1.5, 2.5, 3.5]
    discount_factors = [1.0, 0.97, 0.92, 0.89]
    ts = term_structure_class_cox_cubic_spline(times, discount_factors)
    result = bonds_price(cflow_times, cflow_amounts, ts)
    print 'Cash Flows:'
    for index in range(len(cflow_times)):
        print 'CF at %f:\t%9.2f,\tDF %1.6f, \tPV %9.2f' \
              % (cflow_times[index], cflow_amounts[index], \
                 ts.discount_factor(cflow_times[index]), \
                 ts.discount_factor(cflow_times[index])*cflow_amounts[index])
    print 'Result should be 1063.01!'
    print 'Result calculated: %4.2f' % result


