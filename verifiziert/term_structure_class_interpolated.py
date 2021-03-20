""" ******************************************************

    Klasse fuer normale Termstrukturen (mit linearer
    Interpolation fuer die Laufzeit zwischen den einzelnen
    Zeitpunkten). KONTINUIERLICH verzinste Zinssaetze als
    Input und Output!

    Beschreibung:   Klasse fuer normale Termstrukturen
                    (mit Interpolation). Es handelt sich
                    bei den einzugebenden Zinssaetzen um
                    KONTINUIERLICH verzinste Zinssaetze,
                    dies ist absolut zu beachten!!!
                    
                    Fuer Produktiveinsaetze.

                    ACHTUNG : die Funktion yield() musste
                    wegen Namenskollision mit dem Python-
                    keyword yield in Yield umbenannt werden.
                    
                    Siehe S. 38 des Manuals fuer Zinsbe-
                    rechnungen.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    T               Float       CashFlow-Zeitpunkt
    in_times        List        Vektor der Zinslaufzeiten
    in_yields       List        Vektor der Zinssaetze
                                

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur       --
*******************************************************"""
from term_structure_class import *
from termstru_transforms import *
from termstru_yield_interpolated import *
import copy

class term_structure_class_interpolated(term_structure_class):
    def __init__(self, in_times, in_yields):
        term_structure_class.__init__(self)
        self.__clear()
        if len(in_times)!=len(in_yields):
            raise Exception, 'Cash flow times do not match with number of amounts in term_structure_class_interpolated!'
        self.times_= in_times
        self.yields_= in_yields
        pass

    def __clear(self):
        self.times_ = []
        self.yields_ = []
        pass

    def __copy__(self, other):
        self.times_ = copy.copy(other.times_)
        self.yields_ = copy.copy(other.yields_)
        pass

    def Yield(self, T):
        return term_structure_yield_linearly_interpolated(T, self.times_, self.yields_)
        pass

    def set_interpolated_observations(in_times, in_yields):
        """ Alternative zum Konstruktor der Klasse """
        self.__clear()
        if len(in_times)!=len(in_yields):
            raise Exception, 'Cash flow times do not match with number of amounts in term_structure_class_interpolated!'
        self.times_= in_times
        self.yields_= in_yields
        pass

if __name__=='__main__':
    # Testing
    print 'Test program for the calculations'
    print 'See p. 43 of manual for results.'
    in_times = [0.1, 1.0, 5.0]
    in_yields =  [0.05, 0.07, 0.08]
    ts = term_structure_class_interpolated(in_times, in_yields)
    t1 = 1.0
    t2 = 2.0
    print 'Discount factor at t1 = %1.1f: %1.6f with spot rate of %1.4f' \
          % (t1, ts.discount_factor(t1), ts.Yield(t1))
    print 'Discount factor at t2 = %1.1f: %1.6f with spot rate of %1.4f' \
          % (t2, ts.discount_factor(t2), ts.Yield(t2))
    print 'The corresponding forward rate from t1 = %1.1f to t2 = %1.1f is %1.6f' \
          % (t1, t2, ts.forward_rate(t1, t2))
    
