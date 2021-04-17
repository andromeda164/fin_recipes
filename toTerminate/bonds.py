""" ******************************************************

    Abstrakte Bond-Klasse. Berechnung mit diskreten Cashflow-Payments.
    
    DISKRETE Verzinsung.

    Beschreibung:   Abstrakte Bond-Klasse

                    DISKRETE Verzinsung der IRR.

                    Fuer Produktiveinsaetze
                    geeignet, da mit Termstruktur
                    berechnet!

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    cashflow_times  List        Liste aller Zahlungs-
                                zeitpunkte
    cashflow_amounts List       Liste aller Cash Flows
    d               Klasse       Termstruktur-Klasse, am
                                besten geeignet ist die Klasse
                     term_structure_class_cox_cubic_spline
                                des Kurses von Cox

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       --
    Testprogramm    --
    Literatur-Ref   --
*******************************************************"""
import math
from bonds_price_termstru import bonds_price

class ACFInstrument:
    def __init__(self, legs, curr, valgroup, contract_size = 1.0, \
                 quote_type = 'Pct of Nominal', exercises = None):
        self.valgroup = valgroup
        self.legs = legs
        self.curr = curr
        self.contract_size = contract_size
        self.quote_type = quote_type
        self.exercises = exercises
        self.accruedInArrears = accruedInArrears
        self.__status = 'FO Confirmed'
        pass

    def thPrice(self):
        """ gibt den theoretischen Marktpreis zurueck, basierend
            auf einer Termstruktur """
        ts = getTermstructure(self.valgroup)
        price = 0.0
        nominal = 0.0
        for leg in self.legs:
            nominal += leg.nominal_value
            price += leg.theoreticalPrice(ts)
        return market_price(self, price/nominal)
        

class ACf:
    def __init__(self, type, nominal, pay_day, rate):
        self.type = type
        self.nominal = nominal
        self.pay_day = pay_day
        self.rate = rate
        pass

# class FixedAmount(ACf):
#     """ Fixed Amount PRIME """
#     def __init__(self, 
