""" ******************************************************

    Klasse fx_pair zur Modellierung eines FX Paars.

    Beschreibung:   Klasse zur Modellierung
                    eines FX Paars.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    base_curr       class instance
                                Instanz der Klasse
                                currency.currency
    counter_curr    class instance
                                Instanz der Klasse
                                currency.currency
    basis           integer     Basis des Waehrungspaars
                                (1 oder 100)

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   OK
*******************************************************"""
import math
from finrecipes.currency import *
from finrecipes.calendars import *

class fx_pair:
    """ Class for modelling an fx pair."""
    def __init__(self, base_curr, counter_curr, basis):
        self.__base_curr = base_curr
        self.__counter_curr = counter_curr
        self.__basis = basis
        pass

    def baseCurr(self): return self.__base_curr
    def counterCurr(self): return self.__counter_curr
    def basis(self): return self.__basis
    def calendarList(self): return [self.__base_curr.calendar(), self.__counter_curr.calendar()]
    def FXpairDescription(self): return self.__base_curr.ISOCode()+'/'+self.__counter_curr.ISOCode()
    def __str__(self): return 'Currency pair %s with basis %d.' \
        % (self.__base_curr.ISOCode()+'/'+self.__counter_curr.ISOCode(), self.__basis)
    def __repr__(self): return 'Currency pair %s with basis %d.' \
        % (self.__base_curr.ISOCode()+'/'+self.__counter_curr.ISOCode(), self.__basis)

if __name__=="__main__":
    print('Test for class fx_pair')
    print('----------------------')
    CHF = currency.currency('CHF', 'Swiss Franc', CHF(), 2, 5)
    EUR = currency.currency('EUR', 'Euro', TARGET(), 2, 1)
    USD = currency.currency('USD', 'US Dollar', USD(), 2, 1)
    JPY = currency.currency('JPY', 'Japanese Yen', USD(), 0, 1)
    ITL = currency.currency('ITL', 'Lire Italiane', TARGET(), -1, 5)
    EURCHF = fx_pair(EUR, CHF, 1)
    USDCHF = fx_pair(USD, CHF, 1)
    CHFJPY = fx_pair(CHF, JPY, 100)
    print(EURCHF)
    print(USDCHF)
    print(CHFJPY)
    print('OK')

