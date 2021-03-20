""" ******************************************************

    Reset-Klasse.
    
    Beschreibung:   Reset-Klasse

                    DISKRETE Verzinsung.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    cashflow_times  List        Liste aller Zahlungs-
                                zeitpunkte

    Status
    -----------------------------------------------------
    Syntax          --
    Numerisch       --
    Testprogramm    --
    Literatur-Ref   --
*******************************************************"""
from Leg import *
from CashFlow import *
import dates

class Resets:
    def __init__(self,cashflow,type,daycount,period,day_offset, \
                 rounding,decimals=5,in_arrears,*calendar):
        self.type = type
        self.daycount = daycount
        self.period = period
        self.day_offset = day_offset
        self.rounding = rounding
        self.decimals = decimals
        self.in_arrears = in_arrears
        self.calendar = calendar
        pass
