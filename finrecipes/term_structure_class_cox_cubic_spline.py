""" ******************************************************

    Termstruktur-Klasse, mit Cubic Splines interpoliert.
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
    d               List        Diskontfaktoren-Vektor
    T               Float       Laufzeit T fuer Diskontfaktor

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK          Auf Excel Beispiel getestet
    Literatur       --
*******************************************************"""
from finrecipes.termstru_discfact_cubic_spline import *
from finrecipes.term_structure_class import *
import copy, numpy

class term_structure_class_cox_cubic_spline(term_structure_class):
    def __init__(self, t, d):
        self.t = copy.copy(t)
        self.d = copy.copy(d)
        if t[0] != 0.0:
            raise Exception('First element of times t must be 0.0!')
        if len(t)!=len(d):
            raise Exception('Lenght of f and knots in term_structure_class_cox_cubic_spline not equal!')
        self.z = spline3_coef(t, d)
        pass

    def updateRates(self, d):
        """ eigene Funktion fuer das Updaten der Zinsen, ohne ein
            neues Objekt kreieren zu muessen! """
        self.d = copy.copy(d)
        if len(self.t)!=len(d):
            raise Exception('Lenght of f and knots in term_structure_class_cox_cubic_spline not equal!')
        self.z = spline3_coef(t, d)
        pass

    def discount_factor(self, T):
        return spline3_eval(self.t, self.d, self.z, T)
    

if __name__=='__main__':
    # Testing

    print('Test program for the calculations')
    print('See p. 297 of course instructions Cox.')
    t = [0.0, 0.1, 0.5, 1.0, 2.0]
    knots = [1.0, 0.9965, 0.985, 0.97, 0.95]
    cs = term_structure_class_cox_cubic_spline(t,knots)
    for i in numpy.arange(0.1, 2.1,0.1):
        print('Using a term structure class: yield (t=%1.1f) = %1.6f' % (i, cs.Yield(i)))
        print('Discount factor (t=%1.1f) = %1.6f' % (i, cs.discount_factor(i)))
        print('Forward (t1=%1.1f, t2=%1.1f) = %1.6f' % (i, i + 0.5, cs.forward_rate(i,i+0.5)))
    print()
    print('numeric values for Excel (in F:\Lavori\Business\FinancialModels\...)')
    for i in numpy.arange(0.1, 2.1,0.1):
        print('%1.1f;%1.6f;%1.6f;%1.6f' % (i,cs.discount_factor(i), cs.Yield(i), cs.forward_rate(i,i+0.5)))

