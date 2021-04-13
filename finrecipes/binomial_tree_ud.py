""" ******************************************************

    Binomial-Tree fuer Preise.

    Beschreibung:   Funktion zur Konstruktion eines
                    Binomial-Trees (recombining).

                    ACHTUNG: wahrscheinlich Bug im
                    Original-Programm: Anzahl Nodes ist
                    gleich no_steps+1!!!

                    NUR Preis-Tree!

                        Su
                        /
                    S0<
                        \
                        Sd

                    u, d muessen geliefert werden!

                    Die zusaetzliche Funktion
                    binomial_tree_optimized() sollte fuer
                    sehr grosse Trees einen kleinen
                    Performance-Gewinn bringen!

                    Beide Indices i, j starten bei 0!!!!
                    

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    S0              float       S0, Underlying zum Zeitpunkt
                                null
    u               float       u (Faktor u des Trees)
    d               float       d (Faktor d des Trees)
    no_steps        integer     Anzahl Steps des Trees

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK          siehe pdf-Test-Output
    Literatur-Ref   OK
*******************************************************"""
import math

def binomial_tree(S0, u, d, no_steps):
    tree = []
    for i in range(no_steps+1):     # Achtung: wahrscheinlich Bug im Original-Programm: Anzahl Nodes ist gleich no_steps+1!!!
        S = [0.0 for x in range(i+1)]
        for j in range(i+1):
            S[j] = S0*math.pow(u,j)*math.pow(d,i-j)
        tree.append(S)
    return tree

def binomial_tree_optimized(S0, u, d, no_steps):
    urange = []
    drange = []
    us = 1.0
    ds = 1.0
    for k in range(no_steps+1):
        urange.append(us)
        drange.append(ds)
        us *= u
        ds *= d
    tree = []
    for i in range(no_steps+1):     # Achtung: wahrscheinlich Bug im Original-Programm: Anzahl Nodes ist gleich no_steps+1!!!
        S = [0.0 for x in range(i+1)]
        for j in range(i+1):
            S[j] = S0*urange[j]*drange[i-j]
        tree.append(S)
    return tree


if __name__=="__main__":
    from finrecipes.gen_tree_pdf import *
    from reportlab.pdfgen import *
    print('Test for function binomial_tree.')
    print('This test prints 2 pdf files in the current directory:')
    print('binomial_tree.pdf and binomial_tree_optimized.pdf')
    no_steps = 10
    u = 1.05
    d = 1.0 / u
    S0 = 100.0

    c = canvas.Canvas("binomial_tree.pdf")
    tr = binomial_tree(S0, u, d, no_steps)
    drawBinomialTree(c,1.0*cm,1.0*cm,28*cm,19*cm,tr)
    c.showPage()
    c.save()    

    c = canvas.Canvas("binomial_tree_optimized.pdf")
    tr = binomial_tree_optimized(S0, u, d, no_steps)
    drawBinomialTree(c,1.0*cm,1.0*cm,28*cm,19*cm,tr)
    c.showPage()
    c.save()    
