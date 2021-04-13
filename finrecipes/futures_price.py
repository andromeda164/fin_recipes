""" ******************************************************

    Bewertungsfunktion fuer Futures-Preis.

    Beschreibung:   Bewertungsfunktion fuer Futures-Preis,
                    aus Spot-Preis berechnet.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    S               float       Spot price
    r               float       interest rate, continuously
                                compounded
    time_to_maturity float      time to maturity (years)

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK          p. 48 OK
    Literatur-Ref   --
*******************************************************"""
import math

def futures_price(S, r, time_to_maturity):
    return math.exp(r*time_to_maturity)*S

if __name__=="__main__":
    print('Test for Futures pricing formula (without dividend yield):')
    print('The price for a futures should be 105.127. The formula yields %6.3f.' \
          % (futures_price(100.0, 0.1, 0.5)))
    print('OK')

