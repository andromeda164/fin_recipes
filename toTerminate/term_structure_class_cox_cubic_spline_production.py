""" ******************************************************

    Termstruktur-Klasse Produktivversione, mit Cubic
    Splines interpoliert.
    Es werden die Discount Factors interpoliert und daraus
    die Yields wieder berechnet!

    Eigene Version nach Cox, S. 297 Kursunterlagen Beilage
    Cubic Splines.
    
    KONTINUIERLICH verzinste Version!

    Beschreibung:   Termstruktur-Klasse, mit Cubic Splines
                    interpoliert. Es werden die Discount
                    Factors interpoliert und daraus die
                    Yields wieder berechnet!

                    Cubic Splines nach Unterlagen vom Kurs
                    Cox, S. 297.

                    Es muessen KONTINUIERLICH verzinste
                    Zinsen eingegeben werden!!!

                    Siehe S. 149 des Manuals fuer Zinsbe-
                    rechnungen.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    t               List        Laufzeiten-Vektor
    i               list        annually compounded
                                interest rate vector
    r               list        continuously compounded
                                interest rate vector
    d               List        Diskontfaktoren-Vektor
    T               Float       Laufzeit T fuer Diskontfaktor

    Status
    -----------------------------------------------------
    Syntax          --
    Numerisch       --
    Testprogramm    --
    Literatur       --
*******************************************************"""
import fin_recipes, Numeric
from termstru_discfact_cubic_spline import spline3_coef, spline3_eval
from term_structure_class import *
import copy

class term_structure_class_cox_cubic_spline_production(term_structure_class):
    def __init__(self, t, i=[], r=[], d=[]):
        if len(i)==0:
            if len(r)==0:
                if len(d)==0:
                    raise Exception, 'No termstructure furnished in term_structure_class_cox_cubic_spline_production!'
                else:
                    self.d = copy.copy(d)
            else:
                self.d = []
                for index in range(len(r)):
                    self.d.append(term_structure_discount_factor_from_yield(r[index], t[index]))
        else:
            self.d = []
            for index in range(len(i)):
                r_rate = term_structure_yield_simple_to_compounded(t[index],i[index])
                self.d.append(term_structure_discount_factor_from_yield(r_rate, t[index]))
        self.t = copy.copy(t)
        if len(self.t)!=len(self.d):
            raise Exception, 'Lenght of f and knots in term_structure_class_cox_cubic_spline not equal!'
        self.z = spline3_coef(self.t, self.d)
        pass

    def discount_factor(self, T):
        return spline3_eval(self.t, self.d, self.z, T)
    
    def discount_factor_simple(self, T):
        d = spline3_eval(self.t, self.d, self.z, T)
        r = term_structure_yield_from_discount_factor(d, T)
        i = term_structure_yield_compounded_to_simple(T, r)
        if T<1.0:
            return 1.0/(1.0+i*T)
        else:
            return math.pow(1.0+i,-T)

    def yield_simple(self, T):
        d = spline3_eval(self.t, self.d, self.z, T)
        r = term_structure_yield_from_discount_factor(d, T)
        return term_structure_yield_compounded_to_simple(T, r)

if __name__=='__main__':
    # Testing

    print 'Test program for the calculations'
    print 'See p. 297 of course instructions Cox.'
    t = [0.01, 0.1, 0.5, 1.0, 2.0]
    knots = [0.05, 0.06, 0.065, 0.0675, 0.07]
    ##knots = [1.0, 0.9965, 0.985, 0.97, 0.95]
    cs = term_structure_class_cox_cubic_spline_production(t,i=knots)
    for i in Numeric.arange(0.1, 2.1,0.1):
        print 'Using a term structure class: yield (t=%1.1f) = %1.6f' % (i, cs.Yield(i))
        print 'Discount factor (t=%1.1f) = %1.6f' % (i, cs.discount_factor(i))
        print 'Forward (t1=%1.1f, t2=%1.1f) = %1.6f' % (i, i + 0.5, cs.forward_rate(i,i+0.5))
    print
    print 'numeric values for Excel (in F:\Lavori\Business\FinancialModels\...)'
    for i in Numeric.arange(0.1, 2.1,0.1):
        print '%1.1f;%1.6f;%1.6f;%1.6f;%1.6f' \
              % (i,cs.discount_factor(i),cs.discount_factor_simple(i), \
                 cs.yield_simple(i), cs.forward_rate(i,i+0.5))

