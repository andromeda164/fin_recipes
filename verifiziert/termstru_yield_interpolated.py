""" ******************************************************

    Klasse fuer eine FLACHE Termstruktur (nominaler Zinssatz
    fuer alle Laufzeiten gleich)

    Beschreibung:   Klasse fuer eine FLACHE Termstruktur
                    (nominaler Zinssatz fuer alle Lauf-
                    zeiten gleich). Es muss ein nominaler,
                    jaehrlicher Zinssatz eingegeben werden.

                    Nur fuer Rechnungsuebungen!!!!
                    Fuer Produktiveinsaetze nicht geeignet.

                    ACHTUNG : die Funktion yield() musste
                    wegen Namenskollision mit dem Python-
                    keyword yield in Yield umbenannt werden.
                    
                    Siehe S. 38 des Manuals fuer Zinsbe-
                    rechnungen.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    T               Float       CashFlow-Zeitpunkt
    r               Float       Zinssatz nominal jaehrlich

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur       OK
*******************************************************"""

def term_structure_yield_linearly_interpolated(time, obs_times, obs_yields):
    # assume the yields are in increasing time to maturity order.
    no_obs = len(obs_times)
    if no_obs<1: return 0
    t_min = obs_times[0]
    if time <= t_min: return obs_yields[0]  # earlier than lowest obs.

    t_max = obs_times[no_obs-1]
    if time >= t_max: return obs_yields[no_obs-1]  # later than latest obs

    t = 1  # find which two observations we are between
    while (t<no_obs) & (time>obs_times[t]):
        t+=1
    Lambda = (obs_times[t]-time)/(obs_times[t]-obs_times[t-1])
    # by ordering assumption, time is  between t-1,t
    r = obs_yields[t-1] * Lambda + obs_yields[t] * (1.0-Lambda)
    return r

if __name__=='__main__':
    print 'Test program for the calculations'
    obs_times = [0.1, 0.5, 1.0, 5.0, 10.0]
    obs_yields = [0.1, 0.2, 0.3, 0.4, 0.5]
    times = [0.1, 0.5, 1.0, 3.0, 5.0, 10.0]
    print 'Yields at times:'
    for index in range(len(times)):
        print 'time %1.1f: yield %1.2f' \
              % (times[index], term_structure_yield_linearly_interpolated(times[index], obs_times, obs_yields))
