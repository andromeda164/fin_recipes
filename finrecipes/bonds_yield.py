""" ******************************************************

    Theoretische Bond Yield-to-maturity, gegeben den Markt-
    preis. Berechnung mit diskreten Cashflow-Payments.
    
    Beschreibung:   Theoretische Bond Yield-to-maturity,
                    gegeben den Marktpreis. Berechnung
                    mit diskreten Cashflow-Payments.

                    Falls der Nominalwert 1000 ist, muss
                    ein Preis von ca. 1000 eingegeben
                    werden!

                    KONTINUIERLICHE Abzinsungsformel

                    NICHT fuer Produktiveinsaetze einsetzbar!
                    Insbesondere nicht mit der normalen IRR
                    eines Bonds vergleichbar!
                    
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
from finrecipes.bonds_price import *
import math

def bonds_yield_to_maturity(cashflow_times, cashflow_amounts, bondprice):
    ACCURACY = 0.001 # in percent
    MAX_ITERATIONS = 200
    bot=0.0
    top= 0.01
    diff = 0.0
    while bonds_price(cashflow_times, cashflow_amounts, top) > bondprice:
        top *= 1.5
    r = 0.5 * (top + bot)
    for i in range(MAX_ITERATIONS):
        diff = bonds_price(cashflow_times, cashflow_amounts,r) - bondprice
        if abs(diff)<ACCURACY/100.0: return r
        if diff > 0.0: bot=r
        else: top = r
        r = 0.5 * (top+bot)
    return r

if __name__=='__main__':
    # Testing
    print('Test program for the calculations')
    coupon = 5.0  # in percent
    price = 100.0 # in percent
    nominal = 10000.0
    coupon_payment = coupon * nominal / 100.0
    cflow_times = [1.0, 2.0, 3.0, 4.0]
    cflow_amounts = [coupon_payment,coupon_payment, \
                     coupon_payment,nominal+coupon_payment]
    result = bonds_yield_to_maturity(cflow_times, cflow_amounts, \
                                     nominal * price / 100.0)
    print('Bond yield calculation, %1.2f percent bond, price %3.2f' % \
          (coupon, price))
    print('Coupon continuously compounded: %1.6f percent' % \
          (math.log(1.0+coupon/100.0)*100.0))
    print('Cash Flows:')
    for index in range(len(cflow_times)):
        print('CF at %f:\t%9.2f' % (cflow_times[index], cflow_amounts[index]))
    print('Result should be %1.4f percent!' % (math.log(1.0+coupon/100.0)*100.0))
    print('Result calculated: %1.4f percent' % (result * 100.0))

