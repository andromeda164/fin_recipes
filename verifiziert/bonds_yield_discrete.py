""" ******************************************************

    Theoretische Bond Yield-to-maturity, gegeben den Markt-
    preis. Berechnung mit diskreten Cashflow-Payments.
    DISKRETE Abzinsung!
    
    Beschreibung:   Theoretische Bond Yield-to-maturity,
                    gegeben den Marktpreis. Berechnung
                    mit diskreten Cashflow-Payments.

                    Falls der Nominalwert 1000 ist, muss
                    ein Preis von ca. 1000 eingegeben
                    werden!

                    DISKRETE Abzinsung!

                    Fuer Produktiveinsaetze einsetzbar!
                    IRR-Berechnung von Bonds.
                    
    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    cashflow_times  List        Liste aller Zahlungs-
                                zeitpunkte
    cashflow_amounts List       Liste aller Cash Flows
    bondprice       Float       Bond-Marktpreis. Falls die
                                CashFlows einen Nominalwert
                                von z.B. 1000 haben, muss
                                der Preis (ca.) 1000 sein!

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   OK
*******************************************************"""
from bonds_price_discrete import *
import math

def bonds_yield_to_maturity_discrete(times, cashflows, bondprice):
    ACCURACY = 1e-5
    MAX_ITERATIONS = 200
    bot=0.0
    top=0.01
    r = 0.0
    while bonds_price_discrete(times, cashflows, top) > bondprice:
        top *= 1.5
    r = 0.5 * (top + bot)
    for i in range(MAX_ITERATIONS):
        diff = bonds_price_discrete(times, cashflows,r) - bondprice
        if abs(diff)<ACCURACY: return r
        if diff>0.0: bot=r
        else: top=r
        r = 0.5 * (top+bot)
    return r

if __name__=='__main__':
    # Testing
    print('Test program for the calculations')
    coupon = 5.0  # in percent
    price = 98.0 # in percent
    nominal = 10000.0
    coupon_payment = coupon * nominal / 100.0
    cflow_times = [1.0, 2.0, 3.0, 4.0]
    cflow_amounts = [coupon_payment,coupon_payment, \
                     coupon_payment,nominal+coupon_payment]
    result = bonds_yield_to_maturity_discrete(cflow_times, cflow_amounts, \
                                     nominal * price / 100.0)
    print('Bond yield calculation, %1.2f percent bond, price %3.2f' % \
          (coupon, price))
    print('Cash Flows:')
    for index in range(len(cflow_times)):
        print('CF at %f:\t%9.2f' % (cflow_times[index], cflow_amounts[index]))
    print('Result should be %1.6f percent (HP)!' % (5.5715305))
    print('Result calculated: %1.6f percent' % (result * 100.0))


