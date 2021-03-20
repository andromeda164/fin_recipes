""" ******************************************************

    Bond Duration. Berechnung mit diskreten
    Cashflow-Payments.
    
    DISKRETE Verzinsung.

    Beschreibung:   Funktion zur Berechnung der
                    Duration eines Bonds.

                    DISKRETE Verzinsung der IRR.

                    Nicht fuer Produktiveinsaetze
                    geeignet, da mit Termstruktur
                    berechnet!

                    Formel <> Modified Duration und
                    Macauley Duration!
                    
                    Der Zinssatz r muss vorgaengig
                    DISKRET verzinst worden sein.
                    Siehe S. 28 des Manuals fuer die
                    Berechnungsformeln.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    cashflow_times  List        Liste aller Zahlungs-
                                zeitpunkte
    cashflow_amounts List       Liste aller Cash Flows
    d               Klasse       Termstruktur-Klasse, am
                                besten geeignet ist die Klasse
                     term_structure_class_cox_cubic_spline
                                des Kurses von Cox

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       --
    Testprogramm    --
    Literatur-Ref   --
*******************************************************"""
import math
from term_structure_class_cox_cubic_spline import *
from bonds_duration_modified import *

def bonds_duration(cashflow_times, cashflow_amounts, d):
    S = 0.0
    D1 = 0.0
    for i in range(len(cashflow_times)):
        S += cashflow_amounts[i] * d.discount_factor(cashflow_times[i])
        D1 += cashflow_times[i] * cashflow_amounts[i] * d.discount_factor(cashflow_times[i])
    return D1/S

if __name__=='__main__':
    # Testing
    print 'Test program for the calculations'
    print 'Duration (discretely compounded), see page 21 of manual.'
    times = [0.0, 1.0, 2.0, 3.0]
    discount_factors = [1.0, 0.97, 0.92, 0.89]
    ts = term_structure_class_cox_cubic_spline(times, discount_factors)
    price = 1000.0
    cflow_times = [1.0, 2.0, 3.0, 4.0]
    cflow_amounts = [50.0,50.0,50.0,1050.0]
    zins = bonds_yield_to_maturity_discrete(cflow_times, cflow_amounts, price)
    zins_cont = math.log(1.0 + zins)
    result = bonds_duration(cflow_times, cflow_amounts, ts)
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
    print 'Result calculated with continuously compounded rate of %1.6f: %2.5f' % (zins_cont, result)

