""" ******************************************************

    Klasse market_data zur Modellierung aller Marktdaten.

    Beschreibung:   Klasse market_data zur Modellierung
                    aller Marktdaten (eine einzige Klasse,
                    enthaelt alle Einzeldaten als Kompo-
                    nenten)

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    

    Status
    -----------------------------------------------------
    Syntax          --
    Numerisch       --
    Testprogramm    --
    Literatur-Ref   --
*******************************************************"""
import math, currency, calendars
from fx_pair import *

class market_data:
    """ Class for modelling all market data (its components)."""
    def __init__(self, ):
        pass

    def __str__(self): return 'Currency pair %s with basis %d.' \
        % (self.__base_curr.ISOCode()+'/'+self.__counter_curr.ISOCode(), self.__basis)
    def __repr__(self): return 'Currency pair %s with basis %d.' \
        % (self.__base_curr.ISOCode()+'/'+self.__counter_curr.ISOCode(), self.__basis)

if __name__=="__main__":
    print 'Test for class fx_pair'
    print '----------------------'
    CHF = currency.currency('CHF', 'Swiss Franc', calendars.CHF(), 2, 5)
    EUR = currency.currency('EUR', 'Euro', calendars.TARGET(), 2, 1)
    USD = currency.currency('USD', 'US Dollar', calendars.USD(), 2, 1)
    JPY = currency.currency('JPY', 'Japanese Yen', calendars.USD(), 0, 1)
    ITL = currency.currency('ITL', 'Lire Italiane', calendars.TARGET(), -1, 5)
    EURCHF = fx_pair(EUR, CHF, 1)
    USDCHF = fx_pair(USD, CHF, 1)
    CHFJPY = fx_pair(CHF, JPY, 100)
    print EURCHF
    print USDCHF
    print CHFJPY
    print 'OK'

