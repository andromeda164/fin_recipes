""" ******************************************************

    Klasse currency zur Modellierung einer Waehrung.

    Beschreibung:   Klasse zur Modellierung
                    einer Waehrung.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    ISOCode         string      ISO code der Waehrung
    name            string      Name der Waehrung
    cal             instance of
                    calendars.calendar
                                Instanz der Klasse
                                calendars.calendar
    decimalpos      integer     (10^-decimalpos) ergibt
                                die Minimum-
                                Dezimalstellen der
                                Waehrung,
                                bspw. 2 fuer CHF -> 0.05
    minrounding     integer     Minimale Rounding-Unit,
                                bspw. 5 fuer CHF 0.05

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   --
*******************************************************"""
import math, calendars

class currency:
    """ Class for modelling a single currency."""
    def __init__(self, ISOCode, name, cal = calendars.CHF(),
                 decimalpos = 2, minrounding = 1):
        self.__ISOCode = ISOCode
        self.__name = name
        self.__cal = cal
        self.__decimalpos = float(decimalpos)
        self.__minrounding = float(minrounding)
        pass

    def ISOCode(self): return self.__ISOCode
    def name(self): return self.__name
    def calendar(self): return self.__cal
    def minDecimalPositionExponent(self): return self.__decimalpos
    def minRoundingUnit(self): return self.__minrounding
    def __str__(self): return 'Currency %s (ISO code %s)' % (self.__name, self.__ISOCode)
    def __repr__(self): return 'Currency %s (ISO code %s)' % (self.__name, self.__ISOCode)


if __name__=="__main__":
    print 'Test for class currency'
    CHF = currency('CHF', 'Swiss Franc', calendars.CHF(), 2, 5)
    print CHF
    print 'OK'

