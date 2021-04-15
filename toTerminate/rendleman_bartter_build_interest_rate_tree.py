""" ******************************************************

    Interest rate tree (nach Rendleman-Bartter).

    Beschreibung:   Funktion zur Konstruktion eines Interest
                    rate trees (nach Rendleman-Bartter).

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

                    Beide Indices i, j starten bei 0!!!!
                    

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    r0              float       r0, Short rate zum Zeitpunkt
                                null
    u               float       u (Faktor u des Trees)
    d               float       d (Faktor d des Trees)
    no_steps        integer     Anzahl Steps des Trees

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       --
    Testprogramm    --
    Literatur-Ref   --
*******************************************************"""
import math

def build_interest_rate_tree_rendleman_bartter(r0, u, d, no_steps):
    tree = []
    for i in range(no_steps):
        r = [ 0.0 for j in range(i)]
        for j in range(i):
            r[j] = r0*math.pow(u,j)*math.pow(d,i-j-1)
        tree.append(r)
    return tree


