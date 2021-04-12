""" ******************************************************

    Unittest for day_count
    
    description:    unit test suite based on
                    module pytest

    arguments       Python-type description
    -----------------------------------------------------
        
    status
    -----------------------------------------------------
    syntax          OK
    numeric         OK
    pytest          OK
    literature-ref  --
*******************************************************"""
import pytest, fin_recipes
from day_count import *
from numpy import *

def test_day_count():
    # Unit test suite, tested with SWX-VB-Code and Book from R. Steiner
    
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
    # Unit test Day count rules
    # Examples FA for testing:
    # Old Eurobonds convention (30/360E)
    startdate = dates.date('separated',11,1,2000)
    enddate = dates.date('separated',31,3,2000)
    ai = AI_Factor('30/360E',str(startdate),str(enddate),str(enddate), freq,str(enddate))
    # 30/360E: %s to %s: %6.6f, should be %6.6f.' \
    #      % (startdate, enddate, ai, 79.0 / 360.0))
    assert round(ai,6) == round(79.0 / 360.0, 6)
    startdate = dates.date('separated',11,1,2001)
    enddate = dates.date('separated',31,3,2001)
    ai = AI_Factor('30/360E',str(startdate),str(enddate),str(enddate), freq,str(enddate))
    # 30/360E: %s to %s: %6.6f, should be %6.6f.' \
    #      % (startdate, enddate, ai, 79.0 / 360.0))
    assert round(ai,6) == round(79.0 / 360.0, 6)

    # Example of US Treasury Bond:')
    freq = 2
    startdate = dates.date('separated',7,7,1997)
    settledate = dates.date('separated',30,8,1997)
    enddate = dates.date('separated',15,1,1998)
    maturitydate = dates.date('separated',15,7,2005)
    ai = AI_Factor('Act/ActISMA',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # Act/ActISMA: %s to %s: %6.6f, should be %6.6f.' \
    #     % (startdate, settledate, ai, 8.0/362.0 + 46.0/368.0))
    assert round(ai,6) == round(8.0/362.0 + 46.0/368.0, 6)

    # Examples from the book of R. Steiner "Mastering Financial calculations"')
    freq = 2
    startdate = dates.date('separated',15,1,1999)
    enddate = dates.date('separated',15,7,1999)
    maturitydate = dates.date('separated',15,1,2005)

    settledate = dates.date('separated',30,3,1999)
    ai = AI_Factor('ISMA_99N',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # ISMA_99N: %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 74.0/362.0))
    assert round(ai,6) == round(74.0/362.0, 6)

    ai = AI_Factor('ACT/365L',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # ACT/365L: %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 74.0/365.0))
    assert round(ai,6) == round(74.0/365.0, 6)

    ai = AI_Factor('ACT/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # ACT/360:  %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 74.0/360.0))
    assert round(ai,6) == round(74.0/360.0, 6)

    ai = AI_Factor('30S/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # 30S/360:  %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 75.0/360.0))
    assert round(ai,6) == round(75.0/360.0, 6)

    ai = AI_Factor('30U/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # 30U/360:  %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 75.0/360.0))
    assert round(ai,6) == round(75.0/360.0, 6)
    
    settledate = dates.date('separated',31,3,1999)
    ai = AI_Factor('ISMA_99N',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # ISMA_99N: %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 75.0/362.0))
    assert round(ai,6) == round(75.0/362.0, 6)

    ai = AI_Factor('ACT/365L',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # ACT/365L: %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 75.0/365.0))
    assert round(ai,6) == round(75.0/365.0, 6)

    ai = AI_Factor('ACT/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # ACT/360:  %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 75.0/360.0))
    assert round(ai,6) == round(75.0/360.0, 6)

    ai = AI_Factor('30S/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # 30S/360:  %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 75.0/360.0))
    assert round(ai,6) == round(75.0/360.0, 6)

    ai = AI_Factor('30U/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # 30U/360:  %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 76.0/360.0))
    assert round(ai,6) == round(76.0/360.0, 6)

    settledate = dates.date('separated',1,4,1999)
    ai = AI_Factor('ISMA_99N',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # ISMA_99N: %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 76.0/362.0))
    assert round(ai,6) == round(76.0/362.0, 6)

    ai = AI_Factor('ACT/365L',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # ACT/365L: %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 76.0/365.0))
    assert round(ai,6) == round(76.0/365.0, 6)

    ai = AI_Factor('ACT/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # ACT/360:  %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 76.0/360.0))
    assert round(ai,6) == round(76.0/360.0, 6)

    ai = AI_Factor('30S/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # 30S/360:  %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 76.0/360.0))
    assert round(ai,6) == round(76.0/360.0, 6)


    ai = AI_Factor('30U/360',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # 30U/360:  %s to %s: %6.8f, should be %6.8f.' \
    #      % (startdate, settledate, ai, 76.0/360.0))
    assert round(ai,6) == round(76.0/360.0, 6)

    # SWX ISMA examples:')
    # Example SWX ISMA-99 A.2 Fig.1')
    freq = 2
    startdate = dates.date('separated',22,10,1996)
    settledate = dates.date('separated',15,1,1997)
    enddate = dates.date('separated',22,4,1997)
    maturitydate = dates.date('separated',22,10,1997)
    ai = AI_Factor('ISMA_99N',str(startdate),str(settledate),str(enddate),freq,str(maturitydate),2.75)
    # ISMA_99N: %s to %s: %6.6f, should be %6.6f.' \
    #      % (startdate, settledate, ai, 85.0/182.0/freq*2.75))
    expected_result = 85.0/182.0/freq*2.75
    assert round(ai,6) == round(expected_result, 6)

    # Example SWX ISMA-99 A.2 Fig.2')
    freq = 2
    startdate = dates.date('separated',15,8,1995)
    settledate = dates.date('separated',15,3,1996)
    enddate = dates.date('separated',15,7,1996)
    maturitydate = dates.date('separated',15,1,1997)
    ai = AI_Factor('ISMA_99N',str(startdate),str(settledate),str(enddate),freq,str(maturitydate),4.0)
    # ISMA_99N: %s to %s: %6.6f, should be %6.6f.' \
    #      % (startdate, settledate, ai, (153.0/184.0+60.0/182.0)/freq*4.0))
    expected_result = (153.0/184.0+60.0/182.0)/freq*4.0
    assert round(ai,6) == round(expected_result, 6)

    # Example SWX ISMA-99 A.2 Fig.3')
    freq = 1
    startdate = dates.date('separated',1,2,1999)
    settledate = dates.date('separated',5,5,1999)
    enddate = dates.date('separated',1,7,1999)
    maturitydate = dates.date('separated',1,7,2000)
    ai = AI_Factor('ISMA_99N',str(startdate),str(settledate),str(enddate),freq,str(maturitydate),8.0)
    # ISMA_99N: %s to %s: %6.6f, should be %6.6f.' \
    #      % (startdate, settledate, ai, (93.0/365.0)/freq*8.0))
    expected_result = (93.0/365.0)/freq*8.0
    assert round(ai,6) == round(expected_result, 6)

    # Example SWX ISMA-99 A.2 Fig.4')
    freq = 4
    startdate = dates.date('separated',30,11,1999)
    settledate = dates.date('separated',3,4,2000)
    enddate = dates.date('separated',30,4,2000)
    maturitydate = dates.date('separated',30,4,2000)
    ai = AI_Factor('ISMA_99U',str(startdate),str(settledate),str(enddate),freq,str(maturitydate),5.0)
    # ISMA_99U: %s to %s: %6.6f, should be %6.6f.' \
    #      % (startdate, settledate, ai, (91.0/91.0+34.0/92.0)/freq*5.0))
    expected_result = (91.0/91.0+34.0/92.0)/freq*5.0
    assert round(ai,6) == round(expected_result, 6)
    
    # Example SWX ISMA-99 A.2 Fig.5')
    freq = 2
    startdate = dates.date('separated',30,1,2000)
    settledate = dates.date('separated',15,5,2000)
    enddate = dates.date('separated',30,6,2000)
    maturitydate = dates.date('separated',30,6,2000)
    ai = AI_Factor('ISMA_99N',str(startdate),str(settledate),str(enddate),freq,str(maturitydate),6.0)
    # ISMA_99N: %s to %s: %6.6f, should be %6.6f.' \
    #      % (startdate, settledate, ai, (106.0/182.0)/freq*6.0))
    expected_result = (106.0/182.0)/freq*6.0
    assert round(ai,6) == round(expected_result, 6)

    # Example SWX ISMA-99 A.2 Fig.6')
    freq = 0.5
    startdate = dates.date('separated',28,2,2003)
    settledate = dates.date('separated',15,7,2004)
    enddate = dates.date('separated',28,2,2005)
    maturitydate = dates.date('separated',28,2,2005)
    ai = AI_Factor('ISMA_99U',str(startdate),str(settledate),str(enddate),freq,str(maturitydate),6.75)
    # ISMA_99U: %s to %s: %6.6f, should be %6.6f.' \
    #      % (startdate, settledate, ai, (1.0+137.0/365.0)*6.75))
    expected_result = (1.0+137.0/365.0)*6.75
    assert round(ai,6) == round(expected_result, 6)
    
    # Example of a Swap (split 365/366 ACT/ACT):')
    freq = 1
    startdate = dates.date('separated',15,10,1999)
    settledate = dates.date('separated',15,10,2000)
    enddate = dates.date('separated',15,10,2000)
    maturitydate = dates.date('separated',15,10,2005)
    ai = AI_Factor('ACT/365L',str(startdate),str(settledate),str(enddate),freq,str(maturitydate))
    # ACT/365L: %s to %s: %6.6f, should be %6.6f.' \
    #      % (startdate, settledate, ai, 78.0/365.0 + 288.0/366.0))
    expected_result = 78.0/365.0 + 288.0/366.0
    with pytest.raises(ValueError):
        assert round(ai,6) == round(expected_result, 6)
    # NOT OK this example!')

    # Old Swiss Convention (30/360):')
    freq = 1
    startdate = dates.date('separated',11,1,2000)
    enddate = dates.date('separated',31,3,2000)
    ai = AI_Factor('30/360',str(startdate),str(enddate),str(enddate), freq,str(enddate))
    # 30/360: %s to %s: %6.6f, FA: %6.6f.' \
    #      % (startdate, enddate, ai, 80.0 / 360.0))
    expected_result = 80.0 / 360.0
    assert round(ai,6) == round(expected_result, 6)

    startdate = dates.date('separated',11,1,2001)
    enddate = dates.date('separated',31,3,2001)
    ai = AI_Factor('30/360',str(startdate),str(enddate),str(enddate), freq,str(enddate))
    # 30/360: %s to %s: %6.6f, FA: %6.6f.' \
    #      % (startdate, enddate, ai, 80.0 / 360.0))
    # 30/360 is NOT the same for SWX and FA!')
    expected_result = 80.0 / 360.0
    assert round(ai,6) == round(expected_result, 6)
