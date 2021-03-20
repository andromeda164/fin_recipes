""" ******************************************************

    Binomial-Tree fuer Europaeische Call-Option.

    Beschreibung:   Funktion zur Konstruktion eines
                    Binomial-Trees (recombining) fuer
                    die Bewertung einer Europaeischen
                    Call-Option.

                    Preis- und Optionswerts-Tree.

                        Su
                        /
                    S<
                        \
                        Sd

                    u, d muessen geliefert werden!
                    p, bzw. (1 - p) werden automatisch
                    aus u, d und r berechnet!

                    Kontinuierliche Zinsen fuer r verwenden!

                    r pro Zeitschritt eingeben!!!

                    Fuer DEBUG: Beide Indices des
                    Result-Trees i, j starten bei 0!!!!
                    

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    S               float       Spot price, Underlying
                                zum Zeitpunkt null
    K               float       strike
    r               float       interest rate, continuously
                                compounded
    u               float       Faktor u - Preis-Bewegung up
    d               float       Faktor d - Preis-Bewegung down
    no_periods      integer     Anzahl Steps des Trees, nicht
                                Knotenanzahl, sondern direkt Anzahl
                                Schritte des Trees!!!

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK          siehe pdf-Test-Output, verifiziert
    Literatur-Ref   OK
*******************************************************"""
import math

def option_price_call_european_binomial_multi_period_given_ud( \
    S, K, r, u, d, no_periods):
    # inverse of interest rate
    Rinv = math.exp(-r)
    uu = u*u
    p_up = (math.exp(r)-d)/(u-d)
    p_down = 1.0-p_up
    if DEBUG:
        print('p_up:\t%6.6f, p down:\t%6.6f, exp(-r):\t%6.6f' \
              % (p_up, p_down, math.exp(-r)))
    # price of underlying
    # am linken Ende des Trees 1 Node mehr als No. Steps!
    prices = [0.0 for i in range(no_periods+1)]
    # fill in the endnodes.
    prices[0] = S * math.pow(d, no_periods)
    for i in range(1,no_periods+1):
        prices[i] = uu*prices[i-1]
        
    if DEBUG:
        # construct debug tree
        tree = []
        for i in range(no_periods+1):
            list = [(0.0, 0.0) for i in range(i+1)]
            tree.append(list)
        # fill in values in debug tree, final asset value
        for i in range(no_periods+1):
            tree[no_periods][i] = (prices[i], 0.0)
        # calculate also other values for debug purposes
        for j in range(no_periods):
            debug_prices = [0.0 for i in range(j+1)]
            debug_prices[0] = S * math.pow(d, j)
            for k in range(1,j+1):
                debug_prices[k] = uu*debug_prices[k-1]
            for k in range(j+1):
                tree[j][k] = (debug_prices[k], 0.0)
                
    # value of corresponding call 
    call_values = [0.0 for i in range(no_periods+1)]
    for i in range(no_periods+1):
        # call payoffs at maturity
        call_values[i] = max(0.0, (prices[i]-K))
        if DEBUG:
            # final payoff at time 'no_periods'
            tree[no_periods][i] = (tree[no_periods][i][0],call_values[i])
    for step in range(no_periods-1,-1,-1):
        for i in range(step+1):
            call_values[i] = (p_up*call_values[i+1]+p_down*call_values[i])*Rinv
            if DEBUG:
                tree[step][i] = (tree[step][i][0], call_values[i])
    if DEBUG:
        return call_values[0], tree
    else:
        return call_values[0]

if __name__=="__main__":
    DEBUG = 1
    from gen_tree_pdf import *
    from reportlab.pdfgen import *
    print('Test for function binomial_tree.')
    print('This test prints 3 pdf files in the current directory:')
    print('option_price_call_european_1.pdf, option_price_call_european_2.pdf and option_price_call_european_3.pdf')
    c1 = canvas.Canvas("option_price_call_european_1.pdf")
    c2 = canvas.Canvas("option_price_call_european_2.pdf")
    c3 = canvas.Canvas("option_price_call_european_3.pdf")
    no_steps = 1
    u = 1.05
    d = 1.0 / u
    S = 100.0
    K = 100.0
    r_initial = 0.025 # r per period!!!
    r = r_initial / float(no_steps)
    tree = []
    value, tree = option_price_call_european_binomial_multi_period_given_ud( \
        S, K, r, u, d, no_steps)
    print('The value for %d periods is %6.5f.' % (no_steps, value))
    drawBinomialTree(c1,5.0*cm,5.0*cm,22*cm,15*cm,tree)
    c1.showPage()
    c1.save()

    no_steps = 2
    r = r_initial
    value, tree = option_price_call_european_binomial_multi_period_given_ud( \
        S, K, r, u, d, no_steps)
    print('The value for %d periods is %6.5f.' % (no_steps, value))
    drawBinomialTree(c2,5.0*cm,5.0*cm,22*cm,15*cm,tree)
    c2.showPage()
    c2.save()

    no_steps = 8
    r = r_initial / float(no_steps)
    value, tree = option_price_call_european_binomial_multi_period_given_ud( \
        S, K, r, u, d, no_steps)
    print('The value for %d periods is %6.5f.' % (no_steps, value))
    drawBinomialTree(c3,2.0*cm,2.0*cm,26*cm,17*cm,tree)
    c3.showPage()
    c3.save()
