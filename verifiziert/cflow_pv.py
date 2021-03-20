""" ******************************************************

    Kontinuierlich verzinste Version der PV-Formel.

    Beschreibung:   Kontinuierlich verzinste Present-Value-Formel
                    fuer Cash Flows mit Laufzeiten
                    > 1 Jahr!!
                    
                    Verwendete Formel:
                    PV = CF * exp(-r*t)

                    Der Zinssatz r muss vorgaengig
                    kontinierlich verzinst worden sein.
                    Siehe S. 28 des Manuals fuer die
                    Berechnungsformeln.

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

def cash_flow_pv(cflow_times, cflow_amounts, r):
    PV = 0.0
    PV_cf = 0.0
    t = 0
    for t in range(len(cflow_times)):
        PV_cf = cflow_amounts[t] * math.exp(-r*cflow_times[t])
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
    zins = 0.05
    zins_cont = math.log(1.0 + zins)
    result = cash_flow_pv(cflow_times, cflow_amounts, zins_cont)
    print 'Interest rate: Annually %1.6f, Continuously %1.6f' % \
          (zins, zins_cont)
    print 'Cash Flows:'
    for index in range(len(cflow_times)):
        print 'CF at %f:\t%9.2f' % (cflow_times[index], cflow_amounts[index])
    print 'Result should be 0.0!'
    print 'Result calculated: %1.4f' % result

