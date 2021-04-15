""" ******************************************************

    Zufallsvariablen-Generator mit Uniform-Verteilung.
    Basierend auf random_uniform_0_1().

    Beschreibung:   Die Funktion gibt fuer jeden Funktions-
                    aufruf eine neue, uniform verteilte
                    Zufallszahl zurueck [0, 1].

                    Basierend auf dem Python-Standardmodul
                    random.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK          Python-Standardmodul
    Testprogramm    OK          Verifiziert indirekt ueber
                                random_normal()
    Literatur       OK          
*******************************************************"""

import random

def random_uniform_0_1():
    return random.random() 

