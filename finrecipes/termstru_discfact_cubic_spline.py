""" ******************************************************

    Funktionen fuer die Interpolation von Discount Factors
    via Cubic Splines. Das Fitting der Splines ist in der
    Funktion term_structure_discount_factor_cubic_spline
    nicht inbegriffen!
    KONTINUIERLICH verzinste Version!

    Beschreibung:   Funktion fuer die Interpolation von
                    Zinssaetzen via Cubic Splines.

                    Das Fitting der Splines ist in der Funktion
                    term_structure_discount_factor_cubic_spline
                    nicht inbegriffen!

                    Es muessen KONTINUIERLICH verzinste
                    Zinsen eingegeben werden!!!

                    Siehe S. 149 des Manuals.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    t               Float       Laufzeit t fuer die Berechnung
    b1              Float       Parameter b1
    c1              Float       Parameter c1
    d1              Float       Parameter d1
    f               List        Array von Parametern
    knots           List        Knotenpunkte der Zeitpunkte t

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur       --
*******************************************************"""
import math
import numpy

def term_structure_discount_factor_cubic_spline(t, b1, c1, d1, f, knots):
    d = 0.0
    d = 1.0 + b1*t + c1*(math.pow(t,2.0)) + d1*(math.pow(t,3.0))
    for i in range(len(knots)):
        if t >= knots[i]:
            d += f[i] * math.pow((t-knots[i]),3.0)
        else:
            break
    return d

def spline3_coef(t, y):
    """ Funktion nach Manual vom Kurs Cox, S. 297 """
    n = len(t) - 1
    h = numpy.zeros((n+1))
    b = numpy.zeros((n+1))
    u = numpy.zeros((n+1))
    v = numpy.zeros((n+1))
    z = numpy.zeros((n+1))
    i = 0
    if len(t)!=len(y):
        raise Exception('knot points not of equal length with values furnished!')
    for i in range(n):
        h[i] = t[i+1] - t[i]
        b[i] = (y[i+1] - y[i]) / h[i]
    u[1] = 2 * (h[0] + h[1])
    v[1] = 6 * (b[1] - b[0])
    for i in range(2,n):
        u[i] = 2 * (h[i] + h[i-1]) - h[i-1]*h[i-1] / u[i-1]
        v[i] = 6 * (b[i] - b[i-1]) - h[i-1] * v[i-1] / u[i-1]
    z[n] = 0.0
    for i in range(n-1, 0, -1):
        z[i] = (v[i] - h[i] * z[i+1]) / u[i]
    z[0] = 0.0
    return z

def spline3_eval(t, y, z, x):
    """ Funktion nach Manual vom Kurs Cox, S. 297 """
    n = len(t) - 1
    i = 0
    h = 0.0
    tmp = 0.0
    for i in range(n-1,0,-1):
        if x - t[i] >= 0.0: break
    h = t[i+1] - t[i]
    tmp = (z[i] / 2.0) + (x - t[i]) * (z[i+1] - z[i]) / (6.0 * h)
    tmp = -(h / 6.0) * (z[i+1] + 2.0 * z[i]) + (y[i+1] - y[i]) / h + (x - t[i]) * tmp
    return y[i] + (x - t[i]) * tmp

if __name__=='__main__':
    # Testing

    print('Test program for the calculations')
    print('See p. 299 of manual course Cox GE.')
    print('Test of well-known serpentine-curve: f(x/(0.25 + x*x))')
    def serpentine_curve(x):
        return x/(0.25 + x*x)
    t = [-1.25,-1.15,-1.05,-0.95,-0.85,-0.75,-0.65,-0.55,-0.45,-0.35,-0.25,
         -0.15,-0.05,0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95,1.05,1.15,1.25]
    
    y = [-0.689655172414,-0.731319554849,-0.776340110906,-0.824295010846,-0.874035989717, \
         -0.923076923077,-0.966542750929,-0.995475113122,-0.994475138122,-0.939597315436, \
         -0.8,-0.550458715596,-0.19801980198,0.19801980198,0.550458715596,0.8, \
         0.939597315436,0.994475138122,0.995475113122,0.966542750929,0.923076923077, \
         0.874035989717,0.824295010846,0.776340110906,0.731319554849,0.689655172414]
    n = len(t) - 1
    
    z = spline3_coef(t, y)
    
    for i in numpy.arange(-1.25,1.3,0.05):
        print('x = %1.2f,\twith cubic splines: %1.6f,\tanalytic: %1.6f' \
              % (i, spline3_eval(t,y,z,i), serpentine_curve(i)))

