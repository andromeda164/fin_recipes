""" ******************************************************

    Abstrakte Basis-Klasse fuer Termstruktur

    Beschreibung:   Klasse fuer Termstruktur
                    (abstrakte Base Class) fuer alle
                    vererbten Klassen.
                    
                    WICHTIG:
                    Es muss jeweils die Funktion discount_factor
                    'overridden' werden, die anderen beiden
                    werden dann automatisch wie hier
                    definiert berechnet.

                    ACHTUNG : die Funktion yield() musste
                    wegen Namenskollision mit dem Python-
                    keyword yield in Yield umbenannt werden.
                    
                    Siehe S. 36 des Manuals fuer Zinsbe-
                    rechnungen.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    t               Float       CashFlow-Zeitpunkt
    t1              Float       Erster CashFlow-Zeitpunkt
    t2              Float       Zweiter CashFlow-Zeitpunkt

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur       --
*******************************************************"""
from termstru_transforms import *

class term_structure_class:
    """ Virtual base class for all term structures """
    def __init__(self):
        pass
        
    def forward_rate(self, t1, t2):
        d1 = self.discount_factor(t1)
        d2 = self.discount_factor(t2)
        return term_structure_forward_rate_from_discount_factors(d1,d2,t2-t1)

    def Yield(self, t):
        return term_structure_yield_from_discount_factor(self.discount_factor(t),t)

    def discount_factor(self, t):
        return term_structure_discount_factor_from_yield(self.Yield(t),t)


