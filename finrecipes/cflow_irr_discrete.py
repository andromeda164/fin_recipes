# -*- coding: cp1252 -*-

# Noch �berpr�fen a = function(b+=b-c,2.0); ob das das gleiche ist wie
# b+=b-c; a=function(b,2.0);


""" ******************************************************

    Internal Rate of Return f�r einen Cash Flow Stream
    (IRR). Annualisierte Version.
    (Bond-IRR-Standard-Formel!)

    Beschreibung:   Internal Rate of Return (IRR)
                    Der Zinssatz wird durch numerische
                    Annaeherung berechnet.
                    Es wird von einer jaehrlichen Verzinsung
                    mit entsprechendem Compounding ausge-
                    gangen (wie Standard-IRR-Bond-Formel!).

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
from finrecipes.cflow_pv_discrete import *

def cash_flow_irr_discrete(cflow_times, cflow_amounts):
    # simple minded irr function.  Will find one root (if it exists.)
    # adapted from routine in Numerical Recipes in C.
    if len(cflow_times)!=len(cflow_amounts):
        raise Exception('Not equal length cashflow times and amounts in cflow_irr_discrete!')
    ACCURACY = 1.0e-5
    MAX_ITERATIONS = 50
    x1 = 0.0
    x2 = 0.2
    
    # create an initial bracket, with a root somewhere between bot,top
    f1 = cash_flow_pv_discrete(cflow_times, cflow_amounts, x1)
    f2 = cash_flow_pv_discrete(cflow_times, cflow_amounts, x2)
    i = 0
    for i in range(MAX_ITERATIONS):
        if (f1*f2) < 0.0: break
        if abs(f1)<abs(f2):
            x1 += 1.6*(x1-x2)
            f1 = cash_flow_pv_discrete(cflow_times,cflow_amounts, x1)
        else:
            x2 += 1.6*(x2-x1)
            f2 = cash_flow_pv_discrete(cflow_times,cflow_amounts, x2)
    if (f2*f1>0.0): raise Exception('Well know error (1) in cflow_irr_discrete!')
    f = cash_flow_pv_discrete(cflow_times,cflow_amounts, x1)
    rtb = 0.0
    dx = 0.0
    if f<0.0:
        rtb = x1
        dx = x2-x1
    else:
        rtb = x2
        dx = x1-x2 
    for i in range(MAX_ITERATIONS):
        dx *= 0.5
        x_mid = rtb+dx
        f_mid = cash_flow_pv_discrete(cflow_times,cflow_amounts, x_mid)
        if f_mid <= 0.0:
            rtb = x_mid
        if (abs(f_mid)<ACCURACY) | (abs(dx)<ACCURACY):
            return x_mid
    raise Exception('Well know error (2) in cflow_irr_discrete!')


if __name__=='__main__':
    # Testing
    print('Test program for the calculations')
    cflow_times = [0.0, 1.0, 2.0, 3.0, 4.0]
    cflow_amounts = [-100.0, 5.0,5.0,5.0,105.0]
    print('Cash Flows:')
    for index in range(len(cflow_times)):
        print('CF at %f:\t%9.2f' % (cflow_times[index], cflow_amounts[index]))
    print('Result should be 5.0!')
    print('Result calculated: ', cash_flow_irr_discrete(cflow_times, cflow_amounts)*100.0)
