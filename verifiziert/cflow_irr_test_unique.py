""" ******************************************************

    Test auf Definiertheit der Internal Rate of Return
    (IRR). Kann zur Verifizierung eingesetzt werden,
    ob die eingesetzten Funktionen gueltige Werte zurueck-
    geben koennen.

    Beschreibung:   Die Internal Rate of Return (IRR)
                    wird durch numerische Annaeherung
                    berechnet (Tangenten-Methode oder
                    anderes). Da es sich bei der IRR-
                    Berechnung um die numerische Annaeherung
                    eines mehrdimensionalen Polynomials
                    handelt, kann es gut sein, dass
                    imaginaere Loesungen vorhanden sind.

                    Es ist deshalb vorteilhaft, einen
                    Cash-Flow-Stream vorgaengig auf die
                    Definiertheit zu pruefen.
                    
                    Siehe S. 20 des Manuals fuer Zinsbe-
                    rechnungen.

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
import copy
DEBUG = 1

def sgn(r):
    """ Sign """
    if r>=0:
        return 1
    else:
        return -1

def cash_flow_unique_irr(cflow_times, cflow_amounts):
    sign_changes = 0     # first check Descartes rule
    for t in range(len(cflow_times)):
        if (sgn(cflow_amounts[t-1]) !=sgn(cflow_amounts[t])): sign_changes+=1
    if DEBUG:
        print 'Sign changes (Descartes): %d' % sign_changes
    if sign_changes==0: return False  # can not find any irr
    if sign_changes==1: return True

    A = 0.0
    A = cflow_amounts[0] # check the aggregate cash flows, due to Norstrom
    sign_changes = 0
    for t in range(1,len(cflow_times)):
        A_prima = copy.copy(A)
        A += cflow_amounts[t]
        if sgn(A_prima) != sgn(A):
            sign_changes += 1
    if DEBUG:
        print 'Sign changes (aggregate): %d' % sign_changes
    if sign_changes<=1:
        return True
    return False

if __name__=='__main__':
    # Testing
    print 'Test program for the calculations'
    cflow_times = [0.0, 1.0, 2.0, 3.0, 4.0]
    cflow_amounts = [-100.0, 5.0,5.0,5.0,105.0]
    result = cash_flow_unique_irr(cflow_times, cflow_amounts)
    print 'Cash Flows:'
    for index in range(len(cflow_times)):
        print 'CF at %f:\t%9.2f' % (cflow_times[index], cflow_amounts[index])
    print 'Result should be True!'
    print 'Result calculated: %s' % str(result)
    print
    print 'Next test program'
    cflow_amounts = [-100.0, 5.0,-5.0,10.0,105.0]
    result = cash_flow_unique_irr(cflow_times, cflow_amounts)
    print 'Cash Flows:'
    for index in range(len(cflow_times)):
        print 'CF at %f:\t%9.2f' % (cflow_times[index], cflow_amounts[index])
    print 'Result should be True!'
    print 'Result calculated: %s' % str(result)
    print
    print 'Next test program'
    cflow_amounts = [-20.0, 25.0,-10.0,10.0,-20.0]
    result = cash_flow_unique_irr(cflow_times, cflow_amounts)
    print 'Cash Flows:'
    for index in range(len(cflow_times)):
        print 'CF at %f:\t%9.2f' % (cflow_times[index], cflow_amounts[index])
    print 'Result should be False!'
    print 'Result calculated: %s' % str(result)

