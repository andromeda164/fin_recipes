""" ******************************************************

    Bond-Konvexitaets-Funktion basierend auf Termstruktur.

    Beschreibung:   Funktion zur Berechnung der Konvexitaet
                    eines Bonds.

                    Normale Bond-Konvexitaets-Formel fuer
                    den produktiven Einsatz
                    
                    Der Zinssatz r (IRR) muss vorgaengig
                    DISKRET verzinst worden sein.
                    Siehe S. 28 des Manuals fuer die
                    Berechnungsformeln.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    cashflow_times  List        Liste aller Zahlungs-
                                zeitpunkte
    cashflow_amounts List       Liste aller Cash Flows
    d               Klasse      Termstruktur-Klasse,
                                DISKRET verzinst. Am besten
                                geeignet ist die Klasse
                    term_structure_class_cox_cubic_spline

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       --
    Testprogramm    --
    Literatur-Ref   --
*******************************************************"""
import math
from term_structure_class_cox_cubic_spline import *
from term_structure_class_cubic_spline import *
from term_structure_class_interpolated import *
from term_structure_class_flat import *
from term_structure_class import *

def bonds_convexity(cashflow_times, cashflow_amounts, d):
    B = 0.0
    Cx = 0.0
    for i in len(cashflow_times):
	B += cashflow_amounts[i] * d.discount_factor(cashflow_times[i])
	Cx += math.pow(cashflow_times[i], 2.0) * cashflow_amounts[i] * d.discount_factor(cashflow_times[i])
    return Cx/B

if __name__=='__main__':
    # Testing

    print 'Test program for the calculations'
    print 'See p. 44-46 of manual.'
    r = 0.1106
    r_cont = math.log(1.0+r/100.0)*100.0
    cs = term_structure_class_flat(r)
    for i in Numeric.arange(0.1, 2.1,0.1):
        print 'Using a term structure class: yield (t=%1.1f) = %1.6f' % (i, cs.Yield(i))
        print 'Discount factor (t=%1.1f) = %1.6f' % (i, cs.discount_factor(i))
        print 'Forward (t1=%1.1f, t2=%1.1f) = %1.6f' % (i, i + 0.5, cs.forward_rate(i,i+0.5))
    print
    for i in Numeric.arange(0.1, 2.1,0.1):
        print '%1.1f;%1.6f;%1.6f;%1.6f' % (i,cs.discount_factor(i), cs.Yield(i), cs.forward_rate(i,i+0.5))
    coupon = 0.1
    times = [1.0, 2.0]
    cashflows = [coupon, 1.0+coupon]
    print
    print 'Interest rate %2.2f, continuously compounded %2.6f' \
          %  (r*100.0, r_cont*100.0)
    print 'Coupon rate of Bond: %2.2f' % (coupon*100.0)
    print 'Convexity: %3.5f' % bonds_convexity(times, cashflows, r_cont)

