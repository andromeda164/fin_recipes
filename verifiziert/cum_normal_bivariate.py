""" ******************************************************

    Kumulierte, bivariate Normalverteilung. Numerische
    Naeherungsformel (wahrscheinlich nach Abramowiz und
    Stegun [1964]).




    Noch mit Literatur verifizieren!!!!!!!!!!!!!!!!!!




    Beschreibung:   Die Funktion gibt die angenaeherte,
                    bivariate, kumulative Normalverteilung
                    zurueck.
                    Siehe S. 163 des Manuals.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    a               float       obere Grenze Dichtefunktion 1
    b               float       obere Grenze Dichtefunktion 2
    rho             float       Korrelationsfaktor zwischen
                                1 und 2

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    --
    Literatur       --          noch nicht mit unabhaengigen
                                Werten verifiziert. To do!!!
*******************************************************"""
import math
import cum_normal

PI = 3.141592653589793238462643

def f(x, y, aprime, bprime, rho):
    """ Hilfsfunktion """
    r = aprime*(2.0*x-aprime) + bprime*(2.0*y-bprime) + 2.0*rho*(x-aprime)*(y-bprime)
    return math.exp(r)

def sgn(x):
    """ sign function """
    if x >= 0.0: return 1.0
    else: return -1.0

def N(a, b, rho):
    if (a<=0.0) and (b<=0.0) and (rho<=0.0):
        aprime = a/math.sqrt(2.0*(1.0-rho*rho))
        bprime = b/math.sqrt(2.0*(1.0-rho*rho))
        A = [0.3253030, 0.4211071, 0.1334425, 0.006374323]
        B = [0.1337764, 0.6243247, 1.3425378, 2.2626645]
        sum = 0.0
        for i in range(4):
            for j in range(4):
                sum += A[i]*A[j]* f(B[i],B[j],aprime,bprime,rho)
        sum = sum * (math.sqrt(1.0-rho*rho)/PI)
        return sum
    else:
        if a * b * rho <= 0.0:
            if ( a<=0.0 ) and ( b>=0.0 ) and (rho>=0.0):
                return cum_normal.N(a) - N(a, -b, -rho)
            else:
                if (a>=0.0) and (b<=0.0) and (rho>=0.0):
                    return cum_normal.N(b) - N(-a, b, -rho)
                else:
                    if (a>=0.0) and (b>=0.0) and (rho<=0.0):
                        return cum_normal.N(a) + cum_normal.N(b) - 1.0 + N(-a, -b, rho)
        else:
            if a * b * rho >= 0.0:
                denum = math.sqrt(a*a - 2.0*rho*a*b + b*b)
                rho1 = ((rho * a - b) * sgn(a))/denum
                rho2 = ((rho * b - a) * sgn(b))/denum
                delta=(1.0-sgn(a)*sgn(b))/4.0
                return N(a,0.0,rho1) + N(b,0.0,rho2) - delta
    raise Exception, 'Program error in N(a,b,rho) in cum_normal_bivariate!'
    # should never get here...

if __name__ == "__main__":
    print 'Test program for cumulative, normal bivariate Distribution'
    print 'N(0.0,0.0,0.0) should be 0.25: %6.6f' % N(0.0,0.0,0.0)
    print 'N(0.0,0.0,0.999999999) should be 0.50: %6.6f' % N(0.0,0.0,0.999999999999)
