""" ******************************************************

    Funktionen fuer die Transformation von Zinssaetzen
    in Diskountfactors und Forward-Rates, bzw. vice versa.
    KONTINUIERLICH verzinste Version!

    Beschreibung:   Funktionen fuer die Transformation von
                    Zinssaetzen, wird von der Klasse
                    Termstruktur verwendet.

                    Es muessen KONTINUIERLICH verzinste
                    Zinsen eingegeben werden!!!

                    Siehe S. 34 des Manuals fuer Zinsbe-
                    rechnungen.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    d_t             float       Discount Factor
                                KONTINUIERLICH verzinst
    d_t1            float       Discount Factor zur Zeit 1
                                KONTINUIERLICH verzinst
    d_t2            float       Discount Factor zur Zeit 2
                                KONTINUIERLICH verzinst
    t               float       Laufzeit t
    t1              float       Laufzeit t1
    t2              float       Laufzeit t2
    r               float       Zinssatz nominal jaehrlich
                                KONTINUIERLICH verzinst
    i               float       Zinssatz nominal jaehrlich
                                EINFACH verzinst

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur       --
*******************************************************"""
import math

def term_structure_yield_simple_to_compounded(t, i):
    if t==0.0:
        return i
    r_eff = math.pow(1.0+i*t,1.0/t)-1
    return math.log(1.0+r_eff)

def term_structure_yield_compounded_to_simple(t, r):
    if t==0.0:
        return r
    r_eff = math.exp(r)-1
    return (math.pow(1.0+r_eff, t) - 1.0)*(1.0/t)

def term_structure_yield_from_discount_factor(d_t, t):
    return -math.log(d_t)/t

def term_structure_discount_factor_from_yield(r, t): 
    return math.exp(-r*t)

def term_structure_forward_rate_from_discount_factors(d_t1, d_t2, time):
    return (math.log(d_t1/d_t2))/time

def term_structure_forward_rate_from_yields(r_t1, r_t2, t1, t2):
    return r_t2*t2/(t2-t1)-r_t1*t1/(t2-t1)

if __name__=='__main__':
    print 'Test program for the calculations'
    t1 = 1.0
    r_t1 = 0.05
    d_t1 = term_structure_discount_factor_from_yield(r_t1, t1)
    print 'A %1.1f period spot rate of %1.2f corresponds to a discount factor of %1.6f' \
          % (t1, r_t1, d_t1)
    t2 = 2.0
    d_t2 = 0.9
    r_t2 = term_structure_yield_from_discount_factor(d_t2, t2)
    print d_t1, d_t2
    print 'A %1.1f period discount factor of %1.6f corresponds to a spot rate of %1.6f' \
          % (t2, d_t2, r_t2)
    print 'The forward rate between %1.1f and %1.1f is %1.6f using discount factors and is %1.6f using yields.' \
          % (t1, t2, term_structure_forward_rate_from_discount_factors(d_t1, d_t2, t2-t1), \
             term_structure_forward_rate_from_yields(r_t1, r_t2, t1, t2))
    print 'A simple yield of %4.2f for %4.2f years corresponds to a compounded yield of %6.4f' \
          % (0.05, 0.5, term_structure_yield_simple_to_compounded(0.5, 0.05))
    print 'Converted back this corresponds to a simple rate of %4.2f.' \
          % term_structure_yield_compounded_to_simple(0.5, term_structure_yield_simple_to_compounded(0.5, 0.05))
