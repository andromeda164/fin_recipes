""" ******************************************************

    Termstruktur-Klasse, mit Cubic Splines interpoliert.
    Es werden die Discount Factors interpoliert und daraus
    die Yields wieder berechnet!
    KONTINUIERLICH verzinste Version!

    Beschreibung:   Termstruktur-Klasse, mit Cubic Splines
                    interpoliert. Es werden die Discount
                    Factors interpoliert und daraus die
                    Yields wieder berechnet!

                    Es muessen KONTINUIERLICH verzinste
                    Zinsen eingegeben werden!!!

                    Siehe S. 149 des Manuals fuer Zinsbe-
                    rechnungen.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    b               Float       Parameter b Cubic Splines
    c               Float       Parameter c Cubic Splines
    d               Float       Parameter d Cubic Splines
    f               List        Parameter-Array f Cubic Splines
    knots           List        Knotenpunkte der Laufzeit t
    T               Float       Zinssatz fuer Laufzeit T

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       --
    Testprogramm    --          Noch selber mit eigenen Daten testen,
                                das 'offizielle Testprogramm ist unsinnig!
    Literatur       --
*******************************************************"""
from termstru_discfact_cubic_spline import *
from term_structure_class import *
import copy

class term_structure_class_cubic_spline(term_structure_class):
    def __init__(self, b, c, d, f, knots):
        self.b_ = b
        self.c_ = c
        self.d_ = d
        if len(f)!=len(knots):
            raise Exception('Lenght of f and knots in term_structure_class_cubic_spline not equal!')
        self.f_ = copy.copy(f)
        self.knots_ = copy.copy(knots)
        pass

    def discount_factor(self, T):
        return term_structure_discount_factor_cubic_spline( \
            T,self.b_,self.c_,self.d_,self.f_,self.knots_)

if __name__=='__main__':
    # Testing

    # vielleicht sind die Beispiele auf Seite 150 falsch
    # oder zumindest unsinnig!!!
    print('Test program for the calculations')
    print('See p. 150 of manual.')
    b = 0.1
    c = 0.1
    d = -0.1
    f = [0.01, 0.01, -0.01]
    knots = [2.0, 7.0, 12.0]
    print('Direct calculations, discount factor (t=1) %1.6f' \
          % term_structure_discount_factor_cubic_spline(1,b,c,d,f,knots))
    cs = term_structure_class_cubic_spline(b,c,d,f,knots)
    print('Using a term structure class: yield (t=1) = %1.6f' % cs.Yield(1.0))
    print('Discount factor (t=1) = %1.6f' % cs.discount_factor(1.0))
    print('Forward (t1=1, t2=2) = %1.6f' % cs.forward_rate(1.0,2.0))

    print()
    print('Test with more sense...')
    print('to do...')
    b = 0.1
    c = 0.1
    d = -0.1
    f = [0.01, 0.01, -0.01]
    knots = [2.0, 7.0, 12.0]
    print('Direct calculations, discount factor (t=1) %1.6f' \
          % term_structure_discount_factor_cubic_spline(1,b,c,d,f,knots))
    cs = term_structure_class_cubic_spline(b,c,d,f,knots)
    print('Using a term structure class: yield (t=1) = %1.6f' % cs.Yield(1.0))
    print('Discount factor (t=1) = %1.6f' % cs.discount_factor(1.0))
    print('Forward (t1=1, t2=2) = %1.6f' % cs.forward_rate(1.0,2.0))
