""" ******************************************************

    Theoretischer Bond-Preis, gegeben ein EINZIGER Zinssatz
    (IRR). Berechnung separiert nach Coupons und Principal
    payments.

    Beschreibung:   Funktion zur Berechnung des Preises
                    eines Bonds, gegegeben ein EINZIGER,
                    kontinuierlich verzinster Zinssatz
                    (IRR!).

                    Berechnung separiert nach Coupons
                    und Principal payments.

                    Nur fuer die Berechnung der IRR
                    einsetzbar, nicht fuer andere
                    Produktiveinsaetze!
                    
                    Der Zinssatz r muss vorgaengig
                    kontinierlich verzinst worden sein.
                    Siehe S. 28 des Manuals fuer die
                    Berechnungsformeln.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    coupon_times    List        Liste aller Zahlungs-
                                zeitpunkte der Coupons
    coupon_amounts  List        Liste aller Coupon-Amounts
    principal_times List        Liste aller Zahlungs-
                                zeitpunkte der Principals
    principal_amounts List      Liste aller Principal-
                                Amounts
    r               Float       Zinssatz, 0.05 fuer 5%,
                                IRR, kontinuierlich ver-
                                zinst.

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   OK
*******************************************************"""
import math

def bonds_price(coupon_times, coupon_amounts, \
                principal_times, principal_amounts, r):
    p = 0.0
    for i in range(len(coupon_times)):
        p += math.exp(-r*coupon_times[i])*coupon_amounts[i]
    for i in range(len(principal_times)):
	p += math.exp(-r*principal_times[i])*principal_amounts[i]
    return p

if __name__=='__main__':
    # Testing
    print 'Test program for the calculations'
    print 'bonds price (continuously compounded)'
    coupon_times = [1.0, 2.0, 3.0, 4.0]
    coupon_amounts = [50.0,50.0,50.0,50.0]
    principal_times = [4.0]
    principal_amounts = [1000.0]
    zins = 0.05
    zins_cont = math.log(1.0 + zins)
    result = bonds_price(coupon_times, coupon_amounts, \
                principal_times, principal_amounts, zins_cont)
    print 'Interest rate: Annually %1.6f, Continuously %1.6f' % \
          (zins, zins_cont)
    print 'Coupons:'
    for index in range(len(coupon_times)):
        print 'Coupon at %3.1f:\t%9.2f' % (coupon_times[index], coupon_amounts[index])
    print 'Principals:'
    for index in range(len(principal_amounts)):
        print 'Principal at %3.1f:\t%9.2f' % (principal_times[index], principal_amounts[index])
    print 'Result should be 1000.0!'
    print 'Result calculated with continously compounded rate of %1.6f: %4.2f' % (zins_cont, result)

