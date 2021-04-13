""" ******************************************************

    Unittest for dates
    
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
import pytest
from finrecipes.dates import *


def test_dates():
    # Unittesting (module unittest), called from pytest
    # Unittesting - strong test over 30 years

    import unittest
    import sys

    calendarlist = []
    calendarlist.append(calendars.TARGET())
    calendarlist.append(calendars.USD())
    
    class DateTestCompareDates(unittest.TestCase):
        def testCompareDates(self):
            """testCompareDates tests 2 dates against each other (<,==,>)."""
            d1 = date('USserial',930725)
            d2 = date('USserial',930810)
            # NOT EQUAL
            self.assertEqual(d1!=d2, True, 'failed comparison of NOT EQUAL of two dates (%s, %s).' % (str(d1),str(d2)))
            self.assertEqual(d2!=d1, True, 'failed comparison of NOT EQUAL of two dates (%s, %s).' % (str(d2),str(d1)))
            # EQUAL
            self.assertEqual(d1==d1, True, 'failed comparison of EQUAL of two dates (%s, %s).' % (str(d1),str(d1)))
            self.assertEqual(d2==d2, True, 'failed comparison of EQUAL of two dates (%s, %s).' % (str(d2),str(d2)))
            # LESS
            self.assertEqual(d1<d2, True,  'failed comparison of LESS of two dates (%s, %s).' % (str(d1),str(d2)))
            self.assertEqual(d2<d1, False, 'failed comparison of LESS of two dates (%s, %s).' % (str(d2),str(d1)))
            self.assertEqual(d2<d2, False, 'failed comparison of LESS of two dates (%s, %s).' % (str(d2),str(d2)))
            self.assertEqual(d1<d1, False, 'failed comparison of LESS of two dates (%s, %s).' % (str(d1),str(d1)))
            # GREATER
            self.assertEqual(d2>d1, True,  'failed comparison of GREATER of two dates (%s, %s).' % (str(d2),str(d1)))
            self.assertEqual(d1>d2, False, 'failed comparison of GREATER of two dates (%s, %s).' % (str(d1),str(d2)))
            self.assertEqual(d2>d2, False, 'failed comparison of GREATER of two dates (%s, %s).' % (str(d2),str(d2)))
            self.assertEqual(d1>d1, False, 'failed comparison of GREATER of two dates (%s, %s).' % (str(d1),str(d1)))
            # GREATER EQUAL
            self.assertEqual(d2>=d1, True, 'failed comparison of GREATER EQUAL of two dates (%s, %s).' % (str(d2),str(d1)))
            self.assertEqual(d1>=d2, False,'failed comparison of GREATER EQUAL of two dates (%s, %s).' % (str(d1),str(d2)))
            self.assertEqual(d2>=d2, True,  'failed comparison of GREATER EQUAL of two dates (%s, %s).' % (str(d2),str(d2)))
            self.assertEqual(d1>=d1, True,  'failed comparison of GREATER EQUAL of two dates (%s, %s).' % (str(d1),str(d1)))
            # LESS EQUAL
            self.assertEqual(d1<=d2, True, 'failed comparison of LESS EQUAL of two dates (%s, %s).' % (str(d1),str(d2)))
            self.assertEqual(d2<=d1, False,'failed comparison of LESS EQUAL of two dates (%s, %s).' % (str(d2),str(d1)))
            self.assertEqual(d2<=d2, True,  'failed comparison of LESS EQUAL of two dates (%s, %s).' % (str(d2),str(d2)))
            self.assertEqual(d1<=d1, True,  'failed comparison of LESS EQUAL of two dates (%s, %s).' % (str(d1),str(d1)))
            pass
        def id(self): return "testCompareDates"
        def shortDescription(self): return "TESTING DATE COMPARISONS"


    class DateTestWellFormedConstructor(unittest.TestCase):
        def testWellFormedConstructor(self):
            """testWellFormedConstructor tests wether the different formats are constructed correctly."""
            d1 = date('separated',22,12,2005)
            date_list = []
            date_list.append((date('separated',22,12,2005),"date('separated',22,12,2005)"))
            date_list.append((date('USserial',20051222),"date('USserial',20051222)"))
            date_list.append((date('autodetect','22.12.2005'),"date('autodetect','22.12.2005')"))
            date_list.append((date('autodetect','12/22/2005'),"date('autodetect','12/22/2005')"))
            date_list.append((date('autodetect','2005-12-22'),"date('autodetect','2005-12-22')"))
            date_list.append((date('EU','22.12.2005'),"date('EU','22.12.2005')"))
            date_list.append((date('EU','22#12#2005'),"date('EU','22#12#2005')"))
            date_list.append((date('US','12/22/2005'),"date('US','12/22/2005')"))
            for datum, description in date_list:
                self.assertEqual(d1==datum, True, 'failed construction of date %s. Is read as %s. Construction string %s.' % (str(datum),str(d1),description))
            pass
        def id(self): return "testWellFormedConstructor"
        def shortDescription(self): return "TESTING DATE CONSTRUCTION WELL FORMED DATES"


    class DateTestMalformedConstructor(unittest.TestCase):
        def testMalformedConstructor(self):
            """testMalformedConstructor tests wether the different formats are correctly signalled during construction."""
            date_list = []
            date_list.append((('separated',[29,2,2005]),"date('separated',29,2,2005)"))
            date_list.append((('USserial',[20051299]),"date('USserial',20051299)"))
            date_list.append((('autodetect',['29.02.2005']),"date('autodetect','29.02.2005')"))
            date_list.append((('autodetect',['13/22/2005']),"date('autodetect','13/22/2005')"))
            date_list.append((('autodetect',['205-12-22']),"date('autodetect','205-12-22')"))
            date_list.append((('EU',['32.12.2005']),"date('EU','32.12.2005')"))
            date_list.append((('EU',['00#12#2005']),"date('EU','00#12#2005')"))
            date_list.append((('US',['01/00/2005']),"date('US','01/00/2005')"))
            for datum, description in date_list:
                self.assertRaises(Exception, date, datum[0], datum[1])
            pass
        def id(self): return "testMalformedConstructor"
        def shortDescription(self): return "TESTING DATE CONSTRUCTION MALFORMED DATES"


    class DateTestAddSubtract(unittest.TestCase):
        def addMonths(self, datum, months, ultimo_date):
            """ Helper Function for testing purposes only - cross check on algorithm. """
            #print 'called addMonths for date %s with months %d.' % (str(date('PythonDate',datum)),months)
            y = datum.year
            m = datum.month
            d = datum.day
            if months>=0:
                years = months // 12
            else:
                years = -(abs(months) // 12)
            y += years
            if months>=0:
                # Monate hinzuzaehlen
                m = m+(months-12*years)
                if m>12:
                    y += 1
                    m -= 12
            else:
                # Monate subtrahieren
                #print m, y, (months-12*years), years, months
                m = m+(months-12*years)
                if m<1:
                    y -= 1
                    m += 12
            if m==2:
                if d>=29:
                    if y%4==0:
                        # leap year
                        d = 29
                    else:
                        d = 28
            elif m not in [1,3,5,7,8,10,12]:
                if d==31:
                    # adjust backward for months with 30 days in case of 31st at start day.
                    d = 30
            #print d, m, y, ultimo_date
            if ultimo_date:
                tempM = m+1
                tempY = y
                if tempM>12:
                    tempM -= 12
                    tempY += 1
                return datetime.date(tempY,tempM,1)+datetime.timedelta(days=-1)
            else:
                return datetime.date(y, m, d)
            

        def testAddSubtract(self):
            nativedate = datetime.date(1980,1,1)
            enddate = datetime.date(2010,1,1)
            oneday = datetime.timedelta(days=1)
            d = date('separated',1,1,1990)
            d1 = date('separated',21,3,2005)
            d2 = date('separated',29,2,2000)
            d3 = date('separated',28,2,2000)
            d4 = date('separated',28,2,2001)
            d5 = date('separated',31,12,1990)
            run = nativedate
            #run = date('autodetect',run)
            while run<=enddate:
                start = date('PythonDate',run)
                # next date
                end = date('PythonDate', run+oneday)
                self.assertEqual(start.next_day()==end, True, 'failed next date in date %s.' % str(start))
                # add 25 days
                end = date('PythonDate', run+oneday*25)
                self.assertEqual(start+25==end, True, 'failed add 25 days in date %s.' % str(start))
                # add 125 days
                end = date('PythonDate', run+oneday*125)
                self.assertEqual(start+125==end, True, 'failed add 125 days in date %s.' % str(start))
                # previous date
                end = date('PythonDate', run-oneday)
                self.assertEqual(start.previous_day()==end, True, 'failed previous date in date %s.' % str(start))
                # subtract 25 days
                end = date('PythonDate', run-oneday*25)
                self.assertEqual(start-25==end, True, 'failed subtract 25 days in date %s.' % str(start))
                # subtract 125 days
                end = date('PythonDate', run-oneday*125)
                self.assertEqual(start-125==end, True, 'failed subtract 125 days in date %s.' % str(start))
                # add 1 month
                end = date('PythonDate', self.addMonths(run,1,False))
                self.assertEqual(start.next_month()==end, True, 'failed add 1 month in date %s (%s - %s)' % ( str(start), str(start.next_month()), str(end) ))
                # ultimo relative to
                end = date('PythonDate', self.addMonths(run,0,True))
                self.assertEqual(start.ultimo()==end, True, 'failed ultimo relative to %s (%s vs %s).' % ( str(start), str(start.ultimo()), str(end) ))
                # is February ultimo
                result = date('PythonDate', self.addMonths(run,0,True)) == date('PythonDate', run)
                if run.month==2 and result==True:
                    result = True
                else:
                    result = False
                self.assertEqual(start.is_feb_ultimo()==result, True, 'failed February Ultimo for %s.' % str(start))
                # add 3 months
                end = date('PythonDate', self.addMonths(run,3,False))
                self.assertEqual(start.add_months(3)==end, True, 'failed add 3 months in date %s (%s vs %s).' % (str(start), str(start.add_months(3)), str(end)))
                # add 6 months
                end = date('PythonDate', self.addMonths(run,6,False))
                self.assertEqual(start.add_months(6)==end, True, 'failed add 6 months in date %s (%s vs %s).' % (str(start),str(start.add_months(6)),str(end)))
                # add 11 months
                end = date('PythonDate', self.addMonths(run,11,False))
                self.assertEqual(start.add_months(11)==end, True, 'failed add 11 months in date %s (%s vs %s).' % (str(start),str(start.add_months(11)),str(end)))
                # add 12 months
                end = date('PythonDate', self.addMonths(run,12,False))
                self.assertEqual(start.add_months(12)==end, True, 'failed add 12 months in date %s (%s vs %s).' % (str(start),str(start.add_months(12)),str(end)))
                # add 13 months
                end = date('PythonDate', self.addMonths(run,13,False))
                self.assertEqual(start.add_months(13)==end, True, 'failed add 13 months in date %s (%s vs %s).' % (str(start),str(start.add_months(13)),str(end)))
                # add 25 months
                end = date('PythonDate', self.addMonths(run,25,False))
                self.assertEqual(start.add_months(25)==end, True, 'failed add 25 months in date %s (%s vs %s).' % (str(start),str(start.add_months(25)),str(end)))
                # add -3 months
                end = date('PythonDate', self.addMonths(run,-3,False))
                self.assertEqual(start.add_months(-3)==end, True, 'failed add -3 months in date %s (%s vs %s).' % (str(start),str(start.add_months(-3)),str(end)))
                # add -6 months
                end = date('PythonDate', self.addMonths(run,-6,False))
                self.assertEqual(start.add_months(-6)==end, True, 'failed add -6 months in date %s (%s vs %s).' % (str(start),str(start.add_months(-6)),str(end)))
                # add -11 months
                end = date('PythonDate', self.addMonths(run,-11,False))
                self.assertEqual(start.add_months(-11)==end, True, 'failed add -11 months in date %s (%s vs %s).' % (str(start),str(start.add_months(-11)),str(end)))
                # add -12 months
                end = date('PythonDate', self.addMonths(run,-12,False))
                self.assertEqual(start.add_months(-12)==end, True, 'failed add -12 months in date %s (%s vs %s).' % (str(start),str(start.add_months(-12)),str(end)))
                # add -13 months
                end = date('PythonDate', self.addMonths(run,-13,False))
                self.assertEqual(start.add_months(-13)==end, True, 'failed add -13 months in date %s (%s vs %s).' % (str(start),str(start.add_months(-13)),str(end)))
                # add -25 months
                end = date('PythonDate', self.addMonths(run,-25,False))
                self.assertEqual(start.add_months(-25)==end, True, 'failed add -25 months in date %s (%s vs %s).' % (str(start),str(start.add_months(-25)),str(end)))
                # is Working day
                result = run.isoweekday()<=5
                self.assertEqual((start.weekday()<=5)==result, True, 'failed Working day in date %s.' % str(start))
                # Weekday
                result = run.isoweekday()
                self.assertEqual(start.weekday()==result, True, 'failed Weekday in date %s.' % str(start))
                # Add 2 banking days
                counter = 0
                number = 1
                busday = True
                while counter<2:
                    end = date('PythonDate', run+oneday*number)
                    for calen in calendarlist:
                        if not calen.is_businessday(str(end)): busday = False
                    if busday==True:
                        counter += 1
                    else:
                        busday = True
                    number += 1
                self.assertEqual(start.add_banking_days(2,calendarlist)==end, True, 'failed Add 2 banking days in date %s.' % str(start))
                run += oneday
            pass
        def id(self): return "testAddSubtract"
        def shortDescription(self): return "TESTING DATE ADDDITION/SUBTRACTION"

    class DateTestString(unittest.TestCase):
        def testString(self):
            """testString tests wether a date is correctly printed by means of the functions str() and repr()."""
            d = date('separated',28,2,2001)
            self.assertEqual(str(d)=='28.02.2001', True, 'failed string representation for date %s.' % str(d))
            pass
        def id(self): return "testString"
        def shortDescription(self): return "TESTING DATE STRING REPRESENTATION"


    result = unittest.TestResult()
    suite = unittest.TestSuite()
    suite.addTest(DateTestCompareDates("testCompareDates"))
    suite.addTest(DateTestWellFormedConstructor("testWellFormedConstructor"))
    suite.addTest(DateTestMalformedConstructor("testMalformedConstructor"))
    suite.addTest(DateTestAddSubtract("testAddSubtract"))
    suite.addTest(DateTestString("testString"))

    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)

