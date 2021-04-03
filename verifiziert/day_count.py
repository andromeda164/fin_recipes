# -*- coding: cp1252 -*-
""" ******************************************************

    Berechnung der Accrued Interest-Fraktion und des
    Coupons.
    
    Beschreibung:   Berechnung der Accrued Interest-Fraktion
                    in Prozent des naechsten Coupons, die der
                    Verkaeufer des Bonds erhaelt.

                    Code-Basis anhand der SWX-Spezifikation
                    "Accrued Interest & Yield Calculations
                    and Determination of Holiday Calendars"
                    SWX-SBD-MAN-AIC-202/E

                    Konvention fuer Date Ranges:
                    das erste Datum ist EXCLUDED
                    das letzte Datum ist INCLUDED

                    An einem Coupon-Datum sind Bonds "ex coupon"
                    per Konvention.

                    Fuer Produktiveinsaetze geeignet.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    D1M1Y1          string/date Datum, ab dem der Marchzins
                                berechnet werden soll. Das
                                Format kann entweder ein String
                                oder direkt vom Typ dates.date
                                sein (Datumstyp dieser Library!)
    D2M2Y2          string/date Datum, bis zu dem der Marchzins
                                berechnet werden soll (Settlement
                                date oder f�r Open Accrued Interest
                                auch Valuation date + Spot days).
    D3M3Y3          string/date Datum des naechsten, relevanten
                                Coupons.
    F               integer     Coupon frequency pro Jahr.
    maturity        string/date Maturity date des Bonds.
    coupon          float       Coupon in Prozent des Bonds
                                (0,1 fuer 10%).
    non_verse       float       Fraktion noch nicht bezahlter
                                Nominalwert - fuer diese %-Quote
                                wird natuerlich kein Zins bezahlt.
                                (0,1 fuer 10%).
    method          string      einer der folgenden Werte fuer
                                die Day Count Rule:

    Name            kurz        3.Option
    -----------------------------------------------------
    GERMAN          30/360                      Alte Schweizer Konvention!
                                                Stimmt NICHT mit 30/360 in FA
                                                ueberein!
    SPEC_GERMAN     30S/360     30/360E
    ENGLISH         ACT/365
    FRENCH          ACT/360
    US              30U/360
    ISMA_YEAR       ACT/365L
    ISMA_99N        ACT/ACT     Act/ActISMA     Entspricht NICHT der Act/Act
                                                Konvention von FA (diese ist
                                                die Swap-Konvention 365/366!)
    ISMA_99U        ACT/ACTU
        
    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK          ausgiebiges Testprogramm durchge-
                                fuehrt, muss aber noch aus-
                                gedehnt werden.
    Literatur-Ref   OK
*******************************************************"""
import fin_recipes
import dates
DEBUG = 0

class DayCount:
    """ Klasse fuer DayCount-Bestimmung.
        Flexibel in den Namen! """
    def __init__(self, method):
        if method in ('GERMAN','30/360'):
            self.method = 'GERMAN'
        elif method in ('SPEC_GERMAN','30S/360','30/360E'):
            self.method = 'SPEC_GERMAN'
        elif method in ('ENGLISH', 'ACT/365'):
            self.method = 'ENGLISH'
        elif method in ('FRENCH', 'ACT/360'):
            self.method = 'FRENCH'
        elif method in ('US', '30U/360'):
            self.method = 'US'
        elif method in ('ISMA_YEAR', 'ACT/365L'):
            self.method = 'ISMA_YEAR'
        elif method in ('ISMA_99N', 'ACT/ACT','Act/ActISMA'):
            self.method = 'ISMA_99N'
        elif method in ('ISMA_99U', 'ACT/ACTU'):
            self.method = 'ISMA_99U'
        else:
            raise Exception('Day Count Method %s not supported in class DayCount!' \
                  % (method))
        pass

    def __call__(self):
        return self.method

    def __str__(self):
        return self.method

def AI_Factor(daycount, D1M1Y1, D2M2Y2, D3M3Y3, F, maturity, coupon = 0.0, non_verse = 0.0):
    """  DCM is day count method - via class DayCount
         D1M1Y1 is D1.M1.Y1 etc., siehe Modul-Docstring
         F: Coupon-Frequenz, Integer > 1
         maturity ist die Maturity date.
         Der Typ der Datuemer kann entweder ein String oder direkt
         vom Typ dates.date sein (Datumstyp dieser Library!)
         
         Alle Argument mit Ausnahme von F, coupon, non_verse sind vom Typ string!
         daycount kann auch direkt vom Typ DayCount sein!
    """
    try:
        # date reconstruction
        D1M1Y1 = dates.date('autodetect',D1M1Y1)
        D2M2Y2 = dates.date('autodetect',D2M2Y2)
        D3M3Y3 = dates.date('autodetect',D3M3Y3)
        maturity = dates.date('autodetect',maturity)
    except Exception(detail):
        raise Exception('Bad dates furnished in function AI_Factor (%s)!' % detail)
#    if type(F)!=int:
#        raise Exception, 'Wrong type for Frequency furnished (must be Integer)!'
    if F<0.0:
        raise Exception('Wrong frequency furnished: %d!' % F)
    
    # Day Count Method
    if isinstance(daycount):
        DCM = daycount
    else:
        DCM = DayCount(daycount)
    # temporary result
    ai_fact = 0.0
    # variables used to hold day, month and year
    D1 = 0  
    D1x = 0
    M1 = 0
    Y1 = 0
    # values separately
    D2 = 0
    D2x = 0
    M2 = 0
    Y2 = 0
    D3 = 0
    M3 = 0
    Y3 = 0
    #Dim Anchor As Date # "anchor" date: start date for notional...
    # ...periods
    AD = 0
    AM = 0
    AY = 0
    # "working dates" in notional period loop
    WM = 0
    WY = 0 
    #Dim Target As Date # end date for notional period loop
    # number of interest-bearing days
    N = 0
    Nx = 0
    # length of a year (ISMA-Year)
    Y = 0.0
    # regular coupon length in months
    L = 0
    # notional period length in days
    C = 0.0
    Cx = 0.0
    # applicable coupon frequency
    Fx = 0.0
    # various flags
    Periodic = False
    Regular = False
    Direction = 0
    #Dim CurrC, NextC, TempD As Date # used for temporary serial date values
    # temporary loop variable
    i = 0

    #
    # Determine Number of Interest-bearing days, N
    #
    if str(DCM)=='GERMAN':
        # RULE 1
        D1 = D1M1Y1.day()
        M1 = D1M1Y1.month()
        Y1 = D1M1Y1.year()
        D2 = D2M2Y2.day()
        M2 = D2M2Y2.month()
        Y2 = D2M2Y2.year()
        if D1==31:
            D1x = 30
        elif D1M1Y1.is_feb_ultimo():
            # end of February
            D1x = 30
        else:
            D1x = D1
        if D2==31:
            D2x = 30
        elif D2M2Y2.is_feb_ultimo():
            # end of February
            D2x = 30
        else:
            D2x = D2
        N = (D2x - D1x) + 30 * (M2 - M1) + 360 * (Y2 - Y1)

    elif str(DCM)=='SPEC_GERMAN':
        # RULE 2
        D1 = D1M1Y1.day()
        M1 = D1M1Y1.month()
        Y1 = D1M1Y1.year()
        D2 = D2M2Y2.day()
        M2 = D2M2Y2.month()
        Y2 = D2M2Y2.year()
        if D1==31:
            D1x = 30
        else:
            D1x = D1
        if D2==31:
            D2x = 30
        else:
            D2x = D2
        N = (D2x - D1x) + 30 * (M2 - M1) + 360 * (Y2 - Y1)

    elif str(DCM) in ('ENGLISH', 'FRENCH', 'ISMA_YEAR', 'ISMA_99N', \
                 'ISMA_99U'):
        # RULES 3, 4, 6, 7
        N = D2M2Y2 - D1M1Y1
        
    elif str(DCM)=='US': # RULE 5
        D1 = D1M1Y1.day()
        M1 = D1M1Y1.month()
        Y1 = D1M1Y1.year()
        D2 = D2M2Y2.day()
        M2 = D2M2Y2.month()
        Y2 = D2M2Y2.year()
        D1x = D1
        D2x = D2
        if D1M1Y1.is_feb_ultimo() and D2M2Y2.is_feb_ultimo():
            D2x = 30
        if D1M1Y1.is_feb_ultimo():
            D1x = 30
        if D2x==31 and D1x>=30:
            D2x = 30
        if D1x==31:
            D1x = 30
        N = (D2x - D1x) + 30 * (M2 - M1) + 360 * (Y2 - Y1)
    else:
        raise Exception('Unknown Day Count Rule for Interest calculations (%s)!' % str(DCM))

    # Determine Basic Accrued Interest Factor
    if str(DCM) in ['GERMAN', 'SPEC_GERMAN', 'FRENCH', 'US']:
        # RULES 8, 9, 11, 12
        ai_fact = float(N) / 360.0
    elif str(DCM)=='ENGLISH':
        # RULE 10
        ai_fact = float(N) / 365.0
    elif str(DCM)=='ISMA_YEAR':
        D1 = D1M1Y1.day()
        M1 = D1M1Y1.month()
        Y1 = D1M1Y1.year()
        D3 = D3M3Y3.day()
        M3 = D3M3Y3.month()
        Y3 = D3M3Y3.year()
        if F==1.0:
            # RULE 14
            i = D3M3Y3 - D1M1Y1
            if i==365 or i==366:
                Y = i
            else:
                Y = 365
                for i in range(Y1,Y3+1):
                    TempD = date('separated',1,2,Y3).ultimo() # last day in February
                    if (TempD.day()== 29) and (TempD>D1M1Y1) and \
                       (TempD<=D3M3Y3):
                        Y = 366
                        break
        else:
            # RULE 15
            if ((Y3 % 4 ==0) and (Y3 % 100 != 0)) or (Y3 % 400 == 0):
                Y = 366
            else:
                Y = 365

        # RULE 13
        ai_fact = float(N) / float(Y)

    
    elif str(DCM) in ['ISMA_99N', 'ISMA_99U']:
        D1 = D1M1Y1.day()
        M1 = D1M1Y1.month()
        Y1 = D1M1Y1.year()
        D3 = D3M3Y3.day()
        M3 = D3M3Y3.month()
        Y3 = D3M3Y3.year()
        # check whether the frequency is periodic or not and look if the period is regular
        # set up default values (assume aperiodic, irregular unless otherwise)
        Periodic = False # aperiodic
        L = 12 # regular period length in months
        Fx = 1.0 # applicable coupon frequency
        Regular = False
        if F >= 1.0:
            # RULE 21
            if int(12.0/F) == round(12.0/F,6):
                # RULES 19, 20
                Periodic = True # periodic
                L = int(12.0 / F) # regular period length in months
                Fx = F # applicable coupon frequency
                Regular = False # default: not regular
                if ((Y3 - Y1) * 12 + (M3 - M1)) == L:
                    # RULES 23, 24
                    if str(DCM) =='ISMA_99N':
                        # ISMA-99 Normal
                        if D1==D3:
                            Regular = True
                        elif dates.invalid_date(D3,M1,Y1) and D1M1Y1.is_ultimo():
                            Regular = True
                        elif dates.invalid_date(D1,M3,Y3) and D3M3Y3.is_ultimo():
                            Regular = True
                    else:
                        # ISMA-99 Ultimo
                        if D1M1Y1.is_ultimo() and D3M3Y3.is_ultimo():
                            Regular = True
        
        if Regular:
            # RULE 17
            C = D3M3Y3 - D1M1Y1
            ai_fact = (1.0 / float(Fx)) * (float(N) / float(C))
        else:
            # generate notional periods
            ai_fact = 0.0
            if D3M3Y3==maturity:
                # RULE 18
                if DEBUG:
                    print('generating notional periods forward...')
                Direction = 1 # ... forwards
                Anchor = D1M1Y1
                AY = Y1
                AM = M1
                AD = D1
                Target = D3M3Y3
            else:
                if DEBUG:
                    print('generating notional periods backward...')
                Direction = -1 # ... backwards
                Anchor = D3M3Y3
                AY = Y3
                AM = M3
                AD = D3
                Target = D1M1Y1

            CurrC = Anchor # start notional loop
            i = 0
            while Direction * (CurrC - Target) < 0:
                i += Direction
                WY = dates.date('separated',1,AM,AY).add_months(i*L).year()
                WM = dates.date('separated',1,AM,AY).add_months(i*L).month()
                if str(DCM)=='ISMA_99N':
                    # ISMA-99 Normal
                    if dates.invalid_date(AD,WM,WY):
                        # RULE 23
                        NextC = dates.date('separated',1,WM,WY).ultimo()
                    else:
                        NextC = dates.date('separated',AD,WM,WY)
                else:
                    # ISMA-99 Ultimo
                    NextC = dates.date('separated',1,WM,WY).ultimo() # RULE 24
                if DEBUG:
                    print('next notional period date: %s' % str(NextC))
                Nx = min(D2M2Y2, max(NextC, CurrC)) - max(D1M1Y1, min(CurrC, NextC))
                Cx = Direction * (NextC - CurrC)
                if float(Nx) > 0.0: # RULE 22
                    ai_fact = ai_fact + (float(Nx) / float(Cx)) # RULE 21
                CurrC = NextC
            # RULE 22
            ai_fact = ai_fact / float(Fx)
    else:
        pass
    if coupon:
        return ai_fact * coupon * (1.0 - non_verse)
    else:
        return ai_fact * (1.0 - non_verse)


if __name__=="__main__":
    # Unit test suite, tested with SWX-VB-Code and Book from R. Steiner
    
    from numpy import *
    #f = open(r'DayCount_Unittest.csv','w')
    #f.write('daycount code;daycount method;frequency;start date;settle date;maturity date;fraction\n')
    #basedate = dates.date('separated',1,1,1990)
    ## gemacht ('GERMAN',1),('SPEC_GERMAN',2)
    #for method in [('ENGLISH',3), ('FRENCH',4), \
    #               ('US',5),('ISMA_YEAR',6),('ISMA_99N',7),('ISMA_99U',8)]:
    #    for freq in [1]:  # payment frequencies [1,2,4,6,12]
    #        print 'processing now %s with frequency %d' % (method[0],freq)
    #        for date_diff in range(6000):
    #            #for date_diff_additional in [0, 14, 27]:
    #            start_date = basedate.add_months(date_diff) # +date_diff_additional
    #            maturity_date = start_date.add_months(12/freq)
    #            coupon_period = maturity_date - start_date
    #            for accr_period in range(coupon_period+1):
    #                settle_date = start_date + accr_period
    #                ai_fraction = ai_fact(method[0],str(start_date),str(settle_date),str(maturity_date), freq,str(maturity_date))
    #                f.write('%d;%d;%s;%s;%s;%f\n' % (method[1], freq, str(start_date), str(settle_date), str(maturity_date), ai_fraction))
    #f.close()
    freq = 2 # was not defined here yet, see code above
    print('Unit test Day count rules')
    print('Examples FA for testing:')
    print('Old Eurobonds convention (30/360E)')
    startdate = dates.date('separated',11,1,2000)
    enddate = dates.date('separated',31,3,2000)
    ai = AI_Factor('30/360E',str(startdate),str(enddate),str(enddate), freq,str(enddate))
    print('30/360E: %s to %s: %6.6f, should be %6.6f.' \
          % (startdate, enddate, ai, 79.0 / 360.0))
    startdate = dates.date('separated',11,1,2001)
    enddate = dates.date('separated',31,3,2001)
    ai = AI_Factor('30/360E',str(startdate),str(enddate),str(enddate), freq,str(enddate))
    print('30/360E: %s to %s: %6.6f, should be %6.6f.' \
          % (startdate, enddate, ai, 79.0 / 360.0))
    print('OK')
    print()

    print('Example of US Treasury Bond:')
    freq = 2
    startdate = dates.date('separated',7,7,1997)
    settledate = dates.date('separated',30,8,1997)
    enddate = dates.date('separated',15,1,1998)
    maturitydate = dates.date('separated',15,7,2005)
    ai = AI_Factor('Act/ActISMA',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('Act/ActISMA: %s to %s: %6.6f, should be %6.6f.' \
          % (startdate, settledate, ai, 8.0/362.0 + 46.0/368.0))
    print('OK')
    print()

    print('Examples from the book of R. Steiner "Mastering Financial calculations"')
    freq = 2
    startdate = dates.date('separated',15,1,1999)
    enddate = dates.date('separated',15,7,1999)
    maturitydate = dates.date('separated',15,1,2005)

    settledate = dates.date('separated',30,3,1999)
    ai = AI_Factor('ISMA_99N',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('ISMA_99N: %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 74.0/362.0))
    ai = AI_Factor('ACT/365L',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('ACT/365L: %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 74.0/365.0))
    ai = AI_Factor('ACT/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('ACT/360:  %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 74.0/360.0))
    ai = AI_Factor('30S/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('30S/360:  %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 75.0/360.0))
    ai = AI_Factor('30U/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('30U/360:  %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 75.0/360.0))
    
    settledate = dates.date('separated',31,3,1999)
    ai = AI_Factor('ISMA_99N',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('ISMA_99N: %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 75.0/362.0))
    ai = AI_Factor('ACT/365L',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('ACT/365L: %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 75.0/365.0))
    ai = AI_Factor('ACT/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('ACT/360:  %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 75.0/360.0))
    ai = AI_Factor('30S/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('30S/360:  %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 75.0/360.0))
    ai = AI_Factor('30U/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('30U/360:  %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 76.0/360.0))

    settledate = dates.date('separated',1,4,1999)
    ai = AI_Factor('ISMA_99N',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('ISMA_99N: %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 76.0/362.0))
    ai = AI_Factor('ACT/365L',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('ACT/365L: %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 76.0/365.0))
    ai = AI_Factor('ACT/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('ACT/360:  %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 76.0/360.0))
    ai = AI_Factor('30S/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('30S/360:  %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 76.0/360.0))
    ai = AI_Factor('30U/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('30U/360:  %s to %s: %6.8f, should be %6.8f.' \
          % (startdate, settledate, ai, 76.0/360.0))
    print('OK.')
    print()

    print('SWX ISMA examples:')
    print('Example SWX ISMA-99 A.2 Fig.1')
    freq = 2
    startdate = dates.date('separated',22,10,1996)
    settledate = dates.date('separated',15,1,1997)
    enddate = dates.date('separated',22,4,1997)
    maturitydate = dates.date('separated',22,10,1997)
    ai = AI_Factor('ISMA_99N',str(startdate),str(settledate),str(enddate),freq,str(maturitydate),2.75)
    print('ISMA_99N: %s to %s: %6.6f, should be %6.6f.' \
          % (startdate, settledate, ai, 85.0/182.0/freq*2.75))
    print('Example SWX ISMA-99 A.2 Fig.2')
    freq = 2
    startdate = dates.date('separated',15,8,1995)
    settledate = dates.date('separated',15,3,1996)
    enddate = dates.date('separated',15,7,1996)
    maturitydate = dates.date('separated',15,1,1997)
    ai = AI_Factor('ISMA_99N',str(startdate),str(settledate),str(enddate),freq,str(maturitydate),4.0)
    print('ISMA_99N: %s to %s: %6.6f, should be %6.6f.' \
          % (startdate, settledate, ai, (153.0/184.0+60.0/182.0)/freq*4.0))
    print('Example SWX ISMA-99 A.2 Fig.3')
    freq = 1
    startdate = dates.date('separated',1,2,1999)
    settledate = dates.date('separated',5,5,1999)
    enddate = dates.date('separated',1,7,1999)
    maturitydate = dates.date('separated',1,7,2000)
    ai = AI_Factor('ISMA_99N',str(startdate),str(settledate),str(enddate),freq,str(maturitydate),8.0)
    print('ISMA_99N: %s to %s: %6.6f, should be %6.6f.' \
          % (startdate, settledate, ai, (93.0/365.0)/freq*8.0))
    print('Example SWX ISMA-99 A.2 Fig.4')
    freq = 4
    startdate = dates.date('separated',30,11,1999)
    settledate = dates.date('separated',3,4,2000)
    enddate = dates.date('separated',30,4,2000)
    maturitydate = dates.date('separated',30,4,2000)
    ai = AI_Factor('ISMA_99U',str(startdate),str(settledate),str(enddate),freq,str(maturitydate),5.0)
    print('ISMA_99U: %s to %s: %6.6f, should be %6.6f.' \
          % (startdate, settledate, ai, (91.0/91.0+34.0/92.0)/freq*5.0))
    print('Example SWX ISMA-99 A.2 Fig.5')
    freq = 2
    startdate = dates.date('separated',30,1,2000)
    settledate = dates.date('separated',15,5,2000)
    enddate = dates.date('separated',30,6,2000)
    maturitydate = dates.date('separated',30,6,2000)
    ai = AI_Factor('ISMA_99N',str(startdate),str(settledate),str(enddate),freq,str(maturitydate),6.0)
    print('ISMA_99N: %s to %s: %6.6f, should be %6.6f.' \
          % (startdate, settledate, ai, (106.0/182.0)/freq*6.0))
    print('Example SWX ISMA-99 A.2 Fig.6')
    freq = 0.5
    startdate = dates.date('separated',28,2,2003)
    settledate = dates.date('separated',15,7,2004)
    enddate = dates.date('separated',28,2,2005)
    maturitydate = dates.date('separated',28,2,2005)
    ai = AI_Factor('ISMA_99U',str(startdate),str(settledate),str(enddate),freq,str(maturitydate),6.75)
    print('ISMA_99U: %s to %s: %6.6f, should be %6.6f.' \
          % (startdate, settledate, ai, (1.0+137.0/365.0)*6.75))
    print('OK.')
    print()
    
    print('Example of a Swap (split 365/366 ACT/ACT):')
    freq = 1
    startdate = dates.date('separated',15,10,1999)
    settledate = dates.date('separated',15,10,2000)
    enddate = dates.date('separated',15,10,2000)
    maturitydate = dates.date('separated',15,10,2005)
    ai = AI_Factor('ACT/365L',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    print('ACT/365L: %s to %s: %6.6f, should be %6.6f.' \
          % (startdate, settledate, ai, 78.0/365.0 + 288.0/366.0))
    print('NOT OK this example!')
    print()

    print('Old Swiss Convention (30/360):')
    freq = 1
    startdate = dates.date('separated',11,1,2000)
    enddate = dates.date('separated',31,3,2000)
    ai = AI_Factor('30/360',str(startdate),str(enddate),str(enddate), freq,str(enddate))
    print('30/360: %s to %s: %6.6f, FA: %6.6f.' \
          % (startdate, enddate, ai, 80.0 / 360.0))
    startdate = dates.date('separated',11,1,2001)
    enddate = dates.date('separated',31,3,2001)
    ai = AI_Factor('30/360',str(startdate),str(enddate),str(enddate), freq,str(enddate))
    print('30/360: %s to %s: %6.6f, FA: %6.6f.' \
          % (startdate, enddate, ai, 80.0 / 360.0))
    print('30/360 is NOT the same for SWX and FA!')
    print()

