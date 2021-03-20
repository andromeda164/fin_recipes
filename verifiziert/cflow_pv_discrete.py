""" ******************************************************

    Diskret verzinste Version der PV-Formel.

    Beschreibung:   Diskret verzinste Present-Value-Formel
                    fuer Cash Flows mit Laufzeiten
                    > 1 Jahr!!
                    
                    Verwendete Formel:
                    PV = 1 / (1 + r) ^ t

                    Der Zinssatz r muss vorgaengig
                    annualisiert worden sein.
                    Siehe S. 28 des Manuals.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    cflow_times     List        Liste aller Zahlungs-
                                zeitpunkte
    cflow_amounts   List        Liste aller Cash Flows

    r               Float       Zinssatz, 0.05 fuer 5%

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   --
*******************************************************"""
import math

DEBUG = 0

def cash_flow_pv_discrete(cflow_times, cflow_amounts, r):
    PV = 0.0
    PV_cf = 0.0
    t = 0
    for t in range(len(cflow_times)):
	PV_cf = cflow_amounts[t]/pow(1.0+r,cflow_times[t])
        if DEBUG:
            print 'Cash Flow %d:\tTime:\t%2.4f\tAmount:\t%8.2f\tDiscount Factor:\t%1.6f\tPV:\t%9.2f' \
                  % (t, cflow_times[t], cflow_amounts[t], math.exp(-r*cflow_times[t]), PV_cf)
	PV += PV_cf
    return PV

if __name__=='__main__':
    # Testing
    print 'Test program for the calculations'
    cflow_times = [0.0, 1.0, 2.0, 3.0, 4.0]
    cflow_amounts = [-100.0, 5.0,5.0,5.0,105.0]
    result = cash_flow_pv_discrete(cflow_times, cflow_amounts, 0.05)
    print 'Cash Flows:'
    for index in range(len(cflow_times)):
        print 'CF at %f:\t%9.2f' % (cflow_times[index], cflow_amounts[index])
    print 'Result should be 0.0!'
    print 'Result calculated: %1.4f' % result
