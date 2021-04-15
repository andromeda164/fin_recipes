""" ******************************************************

    Interest rate tree (nach Kurs D. Cox).

    Beschreibung:   Funktion zur Konstruktion eines Interest
                    rate trees (nach Kursunterlagen D. Cox).

                    Es werden 2 mit der Termstruktur kalibrierte
                    Trees zurueckgegeben:
                    1. Short rate tree
                    2. Node price tree
                       (Sum(t)=Discount Factor i)

                    Beide Indices i, j starten bei 0!!!!
                    

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    r0              float       r0, Short rate zum Zeitpunkt
                                null
    sigma           float       volatility
    lognormal       logical     Normal or Lognormal tree
    termstructure   class       Klasse term_structure_class
                                oder davon vererbte Klasse.
    no_steps        integer     Anzahl Steps des Trees
                                Dies bezieht sich auf den
                                Short rate tree!
                                (Node price tree + 1 !)

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       --
    Testprogramm    --
    Literatur-Ref   --
*******************************************************"""
import math

def build_interest_rate_tree_cox_course(r0, sigma, termstructure, \
                                        lognormal, no_steps):
    
    rate_tree = []
    for i in range(no_steps):
        r = [ 0.0 for j in range(i)] # muss das nicht eher j anstelle von 0.0 sein ????
        for j in range(i):
            r[j] = r0*math.pow(u,j)*math.pow(d,i-j-1)
        rate_tree.append(r)
    return tree


