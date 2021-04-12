""" ******************************************************

    Klasse fuer eine FLACHE Termstruktur (nominaler Zinssatz
    fuer alle Laufzeiten gleich)

    Beschreibung:   Klasse fuer eine FLACHE Termstruktur
                    (nominaler Zinssatz fuer alle Lauf-
                    zeiten gleich). Es muss ein nominaler,
                    jaehrlicher Zinssatz eingegeben werden.

                    Nur fuer Rechnungsuebungen!!!!
                    Fuer Produktiveinsaetze nicht geeignet.

                    ACHTUNG : die Funktion yield() musste
                    wegen Namenskollision mit dem Python-
                    keyword yield in Yield umbenannt werden.
                    
                    Siehe S. 38 des Manuals fuer Zinsbe-
                    rechnungen.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    T               Float       CashFlow-Zeitpunkt
    r               Float       Zinssatz nominal jaehrlich

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK          S. 38 Manual
    Literatur       --
*******************************************************"""
from term_structure_class import *

class term_structure_class_flat(term_structure_class):
    def __init__(self, r):
        term_structure_class.__init__(self)
        self.R_ = r    # interest rate
        pass

    def Yield(self, T):
        if T >= 0.0: return self.R_
        else: return 0.0
        
    def set_int_rate(self, r):
        self.R_ = r
        pass

if __name__=='__main__':
    # Testing
    print('Test program for the calculations')
    print('See p. 38 of manual for results.')
    ts = term_structure_class_flat(0.05)
    t1 = 1.0
    t2 = 2.0
    print('Discount factor at t1 = %1.1f: %1.6f with spot rate of %1.4f' \
          % (t1, ts.discount_factor(t1), ts.Yield(t1)))
    print('Discount factor at t2 = %1.1f: %1.6f with spot rate of %1.4f' \
          % (t2, ts.discount_factor(t2), ts.Yield(t2)))
    print('The corresponding forward rate from t1 = %1.1f to t2 = %1.1f is %1.6f' \
          % (t1, t2, ts.forward_rate(t1, t2)))
