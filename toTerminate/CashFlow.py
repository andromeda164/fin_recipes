""" ******************************************************

    CashFlow-Klasse. Berechnung mit diskreten
    Cashflow-Payments.
    
    DISKRETE Verzinsung.

    Beschreibung:   CashFlow-Klasse

                    DISKRETE Verzinsung.

                    Fuer Produktiveinsaetze
                    geeignet, da mit Termstruktur
                    berechnet!

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    cashflow_times  List        Liste aller Zahlungs-
                                zeitpunkte

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       --
    Testprogramm    --
    Literatur-Ref   --
*******************************************************"""
from Leg import *
from day_count import *
import dates

class ACf:
    def __init__(self, type, nominal, pay_day, rate, leg):
        self.type = type
        self.nominal = nominal
        self.pay_day = dates.date('autodetect',pay_day)
        self.rate = rate
        self.leg = leg
        pass

class FixedAmount(ACf):
    """ Fixed Amount PRIME """
    def __init__(self, nominal, pay_day, rate, leg):
        ACf.__init(self, 'FixedAmount', nominal, pay_day, rate, leg)
        pass

    def projected_cf(self):
        return self.nominal

    def PV(self, ts):
        # Berechnung Fraktion des Datums
        return self.nominal * ts.discount_factor(self.payment_fraction)

    def accrued(self, settle_date):
        """ returns the accrued fraction of
            the coupon which contains spot_date """
        return 0.0        
            
class FixedRate(ACf):
    """ Fixed Rate PRIME """
    def __init__(self, nominal, start_day, end_day, pay_day, rate, leg):
        ACf.__init(self, 'FixedRate', nominal, pay_day, rate, leg)
        self.start_day = dates.date('autodetect',start_day)
        self.end_day = dates.date('autodetect',end_day)
        self.days = self.end_day - self.start_day
        pass

    def projected_cf(self):
        return self.nominal * \
            AI_Factor(self.leg.daycount, self.start_day, self.end_day, self.end_day, \
                      self.leg.rollfreq, self.leg.maturity, self.leg.coupon/100.0,self.leg.non_verse)

    def PV(self, ts):
        # Berechnung Fraktion des Datums
        return self.nominal * \
            AI_Factor(self.leg.daycount, self.start_day, self.end_day, self.end_day, \
                      self.leg.rollfreq, self.leg.maturity, self.leg.coupon/100.0,self.leg.non_verse) \
            * ts.discount_factor(self.payment_fraction)

    def accrued(self, settle_date):
        """ returns the accrued fraction of
            the coupon which contains spot_date """
        return self.nominal * \
            AI_Factor(self.leg.daycount, self.start_day, settle_date, self.end_day, \
                      self.leg.rollfreq, self.leg.maturity, self.leg.coupon/100.0,self.leg.non_verse)


class FloatingRate(ACf):
    """ Floating Rate PRIME """
    def __init__(self, nominal, start_day, end_day, pay_day, spread, leg, factor = 1.0, offset = 0.0):
        ACf.__init(self, 'FloatingRate', nominal, pay_day, 0.0, leg)
        self.start_day = dates.date('autodetect',start_day)
        self.end_day = dates.date('autodetect',end_day)
        self.days = self.end_day - self.start_day
        self.spread = spread
        self.factor = factor
        self.offset = offset
        self.resets = 0 # to do: Resets('single'
        pass

    def projected_cf(self):
        return self.nominal * \
            AI_Factor(self.leg.daycount, self.start_day, self.end_day, self.end_day, \
                      self.leg.rollfreq, self.leg.maturity, self.leg.coupon/100.0,self.leg.non_verse)

    def PV(self, ts):
        # Berechnung Fraktion des Datums
        return self.nominal * \
            AI_Factor(self.leg.daycount, self.start_day, self.end_day, self.end_day, \
                      self.leg.rollfreq, self.leg.maturity, self.leg.coupon/100.0,self.leg.non_verse) \
            * ts.discount_factor(self.payment_fraction)

    def accrued(self, settle_date):
        """ returns the accrued fraction of
            the coupon which contains spot_date """
        return self.nominal * \
            AI_Factor(self.leg.daycount, self.start_day, settle_date, self.end_day, \
                      self.leg.rollfreq, self.leg.maturity, self.leg.coupon/100.0,self.leg.non_verse)


# Floating Rate
# type
# nominal
# start_day
# end_day
# days
# pay_day
# rate
# offset
# factor
# spread

        
