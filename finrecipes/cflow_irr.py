# -*- coding: cp1252 -*-
""" ******************************************************

    Internal Rate of Return f�r einen Cash Flow Stream
    (IRR). Kontinuierlich verzinste Version.
    (NICHT Bond-IRR-Standard-Formel!)

    Beschreibung:   Internal Rate of Return (IRR)
                    Der Zinssatz wird durch numerische
                    Annaeherung berechnet.
                    Es wird von einer kontinuierlichen
                    Verzinsung mit entsprechendem Compounding
                    ausgegangen. Nicht f�r Bond-Berechnungen
                    einsetzbar!
                    Siehe S. 28 des Manuals fuer Zinsbe-
                    rechnungen.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    cflow_times     List        Liste aller Zahlungs-
                                zeitpunkte
    cflow_amounts   List        Liste aller Cash Flows

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur       --
*******************************************************"""
from finrecipes.cflow_pv import *
import math

def cash_flow_irr(cflow_times, cflow_amounts):
    # simple minded irr function.  Will find one root (if it exists.)
    # adapted from routine in Numerical Recipes in C.
    if len(cflow_times)!=len(cflow_amounts):
        raise Exception('Lenght of cflow_times and cflow_amounts not equal in cflow_irr!')
    ACCURACY = 1.0e-5
    MAX_ITERATIONS = 50
    x1 = 0.0
    x2 = 0.2
    
    # create an initial bracket, with a root somewhere between bot,top
    f1 = cash_flow_pv(cflow_times, cflow_amounts, x1)
    f2 = cash_flow_pv(cflow_times, cflow_amounts, x2)
    i = 0
    for i in range(MAX_ITERATIONS):
        if (f1*f2) < 0.0: break
        if abs(f1) < abs(f2):
            x1 += 1.6*(x1-x2)
            f1 = cash_flow_pv(cflow_times,cflow_amounts, x1)
        else:
            x2 += 1.6*(x2-x1)
            f2 = cash_flow_pv(cflow_times,cflow_amounts, x2)
    if f2*f1 > 0.0:
        raise Exception('well-known exception in cflow_irr (1)')
    f = cash_flow_pv(cflow_times,cflow_amounts, x1)
    rtb = 0.0
    dx=0.0
    if f < 0.0:
        rtb = x1
        dx=x2-x1 
    else:
        rtb = x2
        dx = x1-x2
    for i in range(MAX_ITERATIONS):
        dx *= 0.5
        x_mid = rtb+dx
        f_mid = cash_flow_pv(cflow_times,cflow_amounts, x_mid)
        if f_mid<=0.0:
            rtb = x_mid
        if (abs(f_mid)<ACCURACY) | (abs(dx)<ACCURACY):
            return x_mid
    raise Exception('well-known exception in cflow_irr (2)')

if __name__=='__main__':
    # Testing
    print('Test program for the calculations')
    cflow_times = [0.0, 1.0, 2.0, 3.0, 4.0]
    cflow_amounts = [-100.0, 5.0,5.0,5.0,105.0]
    result = cash_flow_irr(cflow_times, cflow_amounts)
    result = (math.exp(result) - 1.0) * 100.0
    print('Cash Flows:')
    for index in range(len(cflow_times)):
        print('CF at %f:\t%9.2f' % (cflow_times[index], cflow_amounts[index]))
    print('Result should be 5.0!')
    print('Result calculated: %1.4f' % result)

