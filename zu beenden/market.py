""" ******************************************************

    market Klasse
    
    Beschreibung:   market-Klasse

                                Klasse zur Beschreibung eines
                                Boersenplatzes.

                                ACHTUNG:********************
                                Der Boersenplatz GLOBEX muss
                                noch implementiert werden!
                                ****************************

                                Die verfuegbaren Typen sind:
                                normal: Normaler Boersenplatz
                                        (Oeffnungszeiten normale
                                         Business hours)
                                Forex: Ab Freitag Abend geschlossen
                                        bis Sonntag Abend
                                Forex w/o weekends: Immer geoeffnet
                                GLOBEX: tbd.

                                Die Argumente openingHour und
                                closingHour sind fuer den
                                Boersenplatz 'Forex w/o weekends'
                                nicht relevant, da immer
                                geoeffnet.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    name            string      Name des markets
    cals            List of Python Object of type calendars.calendar
                                Business day Kalender der
                                Boerse (mehrere moeglich)
    Type            string      in ['normal','Forex',
                                'Forex w/o weekends','GLOBEX']
    openingHour     float       8.25 fuer 8 Uhr 15 Minuten
    SundayOpeningHour float     8.25 fuer 8 Uhr 15 Minuten,
                                relevant NUR fuer die GLOBEX
    closingHour     float       16.75 fuer 16 Uhr 45 Minuten
    timezone        string      Zeitzone des Boersenplatzes
    timestamp       datetime.datetime oder
                    dates.date  

    Status
    -----------------------------------------------------
    Syntax          --
    Numerisch       --
    Testprogramm    --
    Literatur-Ref   --
*******************************************************"""
import fin_recipes
import datetime, dates, calendars, math

class market:
    """ Klasse zur Beschreibung eines market. """
    def __init__(self, name, cals, Type, openingHour, closingHour, timezone = 'Europe/Zurich', SundayOpeningHour = 0.0):
        if type(name) != type(''):
            raise TypeError, 'Wrong argument type used in name argument (must be a string)!'
        self.name = name
        
        if type(timezone) != type(''):
            raise TypeError, 'Wrong argument type used in timezone argument (must be a string)!'
        self.timezone = timezone

        if cals == None:
            cals = [calendars.CHF()]
        for calendar in cals:
            if not isinstance(calendar,calendars.calendar):
                raise TypeError, 'Wrong argument type used in calendar argument (object of type calendars.calendar)!'
        self.calendar = cals

        if Type not in ['normal','Forex', 'Forex w/o weekends','GLOBEX']:
            raise TypeError, 'Wrong argument used in Type argument (must be one of [normal, Forex, Forex w/o weekends,GLOBEX])!'
        self.Type = Type

        try:
            self.openingHour = float(openingHour)
        except:
            raise TypeError, 'Wrong argument type used in openingHour argument (must be numeric)!'

        try:
            self.closingHour = float(closingHour)
        except:
            raise TypeError, 'Wrong argument type used in closingHour argument (must be numeric)!'

        try:
            self.SundayOpeningHour = float(SundayOpeningHour)
        except:
            raise TypeError, 'Wrong argument type used in SundayOpeningHour argument (must be numeric)!'
        pass

    def __str__(self):
        return 'market %s with type %s' % (self.name, self.Type)

    def is_businesshour(self, timestamp):
        """ gibt True zurueck, falls das Argument timestamp waehrend den
            Geschaeftzeiten liegt. """
        if not isinstance(timestamp, datetime.date):
            raise Exception, 'Invalid date furnished in is_businessday(%s)!' % str(timestamp)
        datum = dates.date('PythonDate', timestamp)
        openingtime = datetime.datetime(timestamp.year,timestamp.month,timestamp.day, \
                int(self.openingHour),int((self.openingHour - float(int(self.openingHour)))/100.0*60.0),0)
        closingtime = datetime.datetime(timestamp.year,timestamp.month,timestamp.day, \
                int(self.closingHour),int((self.closingHour - float(int(self.closingHour)))/100.0*60.0),0)
        Sundayopeningtime = datetime.datetime(timestamp.year,timestamp.month,timestamp.day, \
                int(self.SundayOpeningHour),int((self.SundayOpeningHour - float(int(self.SundayOpeningHour)))/100.0*60.0),0)
        if self.Type=='Forex w/o weekends':
            return True
        elif self.Type=='GLOBEX':
            if datum.weekday()==6: # Saturday -> closed
                return False
            elif (datum.weekday()==7 or self.calendar.is_businessday(datum)==False) and timestamp > Sundayopeningtime:
                return True
            elif (datum.weekday()==7 or self.calendar.is_businessday(datum)==False) and timestamp <= Sundayopeningtime:
                return False
            elif (datum.weekday()==5 and self.calendar.is_businessday(datum)==False):
                return False
            elif datum.weekday()==5 and timestamp <= closingtime:
                return True
            elif datum.weekday()==5 and timestamp > closingtime:
                return False
            elif timestamp > closingtime or timestamp < openingtime:
                return False
            else:
                return True
        elif self.Type=='normal':
            if datum.is_weekend():
                return False
            for cal in self.calendar:
                if not cal.is_businessday(datum):
                    return False
            else:
                if timestamp <= openingtime:
                    return False
                elif timestamp > closingtime:
                    return False
                return True
        elif self.Type=='Forex':
            if datum.weekday()==5 and timestamp > closingtime:
                return False
            elif datum.weekday()==5 and timestamp <= closingtime:
                return True
            elif datum.weekday()==7 and timestamp > openingtime:
                return True
            elif datum.weekday()==7 and timestamp <= openingtime:
                return False
            elif datum.weekday()==6:    # Saturday
                return False
            else:
                return True

    def is_businessday(self, datum):
        """ gibt True zurueck, falls das Argument datum ein Business day
            nach Kalender self.calendar ist. """
        result = True
        if datum.is_weekend():
            return False
        for cal in self.calendar:
            if not cal.is_businessday(datum): result = False
        return result
        
       
        
if __name__ == "__main__":
    import unittest
    import sys

    print 'Unittesting of class market'
    class CalendarTestUSD(unittest.TestCase):
        def setUp(self):
            self.knownValues = [ \
                '01.01.2000', '01.05.2000', '25.12.2000', '26.12.2000',
                '01.01.2001', '01.05.2001', '25.12.2001', '26.12.2001',
                '01.01.2002', '01.05.2002', '25.12.2002', '26.12.2002',
                '01.01.2003', '01.05.2003', '25.12.2003', '26.12.2003',
                '01.01.2004', '01.05.2004', '25.12.2004', '26.12.2004',
                '01.01.2005', '01.05.2005', '25.12.2005', '26.12.2005',
                '01.01.2006', '01.05.2006', '25.12.2006', '26.12.2006',
                '01.01.2007', '01.05.2007', '25.12.2007', '26.12.2007',
                '01.01.2008', '01.05.2008', '25.12.2008', '26.12.2008',
                '01.01.2009', '01.05.2009', '25.12.2009', '26.12.2009',
                '01.01.2010', '01.05.2010', '25.12.2010', '26.12.2010']
            pass
        

    class marketTestAllValuesUSD(CalendarTestUSD):
        def testAllValues(self):
            """testAllValues tests a market of type Forex tests against 10 years of known USD holidays and weekends."""
            testCal = calendars.calendar(self.knownValues)
            name = 'test calendar'
            Type = 'Forex'
            openingHour = 22.50
            closingHour = 20.00
            timezone = 'Europe/London'
            boerse = market(name, [testCal], Type, openingHour, closingHour, timezone)
            start = dates.date('EU','31.12.1999')
            end = dates.date('EU','31.12.2010')
            run = start
            testHolidays = [holi for holi in testCal.holidays()]
            while run < end:
                isHoliday = False
                if run in testHolidays: isHoliday = True
                if run.is_weekend(): isHoliday = True
                self.assertEqual(not isHoliday, boerse.is_businessday(run),'failed comparison of all values of day %s' % str(run))
                run += 1
            pass
        def id(self): return "testAllValues"
        def shortDescription(self): return "Tests a market of type 'Forex' against 10 years of known USD holidays and weekends."

    class marketTestNormalMarket(unittest.TestCase):
        def testNormalMarket(self):
            """testNormalMarket tests a market of type 'normal' for 3 years
               against known CHF holidays and weekends with a time step of 5 minutes."""
            name = 'Normal Market'
            cal1 = calendars.CHF()
            cal2 = calendars.USD()
            print len(cal1.holidays())
            cals = [cal1, cal2]
            Type = 'normal'
            openingHour = 8.25
            closingHour = 17.0 + 10.0/60.0  # --> 17.10
            timezone = 'Europe/Zurich'
            boerse = market(name, cals, Type, openingHour, closingHour, timezone)
            start = datetime.datetime(2003,1,1,0,0,0)
            end = datetime.datetime(2006,1,1,0,0,0)
            delta = datetime.timedelta(minutes=5)
            run = start
            testHolidays = []
            print len(cals)
            for cal in cals:
                print len(cal.holidays())
                l = [holi for holi in cal.holidays()]
                testHolidays.extend(l)
            testHolidays = testHolidays.sort()
            print len(testHolidays)
            while run < end:
                isHoliday = False
                isBusinessHour = True
                pythonrun = dates.date('PythonDate', run)
                if pythonrun in testHolidays:
                    isHoliday = True
                    isBusinessHour = False
                if pythonrun.is_weekend():
                    isHoliday = True
                    isBusinessHour = False
                openingtime = datetime.datetime(run.year,run.month,run.day, \
                        math.floor(openingHour),math.floor((openingHour - float(math.floor(openingHour)))/100.0*60.0),0)
                closingtime = datetime.datetime(run.year,run.month,run.day, \
                    math.floor(closingHour),math.floor((closingHour - float(math.floor(closingHour)))/100.0*60.0),0)
                if not isHoliday:
                    if run <= openingtime:
                        isBusinessHour = False
                    if run > closingtime:
                        isBusinessHour = False
                #print isHoliday, isBusinessHour, not boerse.is_businessday(pythonrun), str(pythonrun), str(run)
                self.assertEqual(isHoliday, not boerse.is_businessday(pythonrun),'failed comparison of a market of type \'normal\' of function is_businessday() of day %s' % str(run))
                self.assertEqual(isBusinessHour, boerse.is_businesshour(run),'failed comparison of a market of type \'normal\' of function is_businesshour() of timestamp %s' % str(run))
                run += delta
            pass
        def id(self): return "testNormalMarket"
        def shortDescription(self): return "Tests a market of type 'normal' against 3 years of known CHF holidays and weekends."

    class marketTestForexMarket(unittest.TestCase):
        def testForexMarket(self):
            """testForexMarket tests a market of type 'Forex' for 3 years
               against weekends with a time step of 5 minutes."""
            name = 'Forex market'
            Type = 'Forex'
            openingHour = 23.0
            closingHour = 22.0
            cals = [calendars.CHF()]   # doesn't matter...
            timezone = 'Europe/Zurich'
            boerse = market(name, cals, Type, openingHour, closingHour, timezone)
            start = datetime.datetime(2003,1,1,0,0,0)
            end = datetime.datetime(2006,1,1,0,0,0)
            delta = datetime.timedelta(minutes=5)
            run = start
            #print
            while run < end:
                closed = False
                pythonrun = dates.date('PythonDate', run)
                openingtime = datetime.datetime(pythonrun.year(),pythonrun.month(),pythonrun.day(), \
                        math.floor(openingHour),math.floor((openingHour - float(math.floor(openingHour)))/100.0*60.0),0)
                closingtime = datetime.datetime(pythonrun.year(),pythonrun.month(),pythonrun.day(), \
                        math.floor(closingHour),math.floor((closingHour - float(math.floor(closingHour)))/100.0*60.0),0)
                if pythonrun.weekday()==5 and run > closingtime:
                    closed = True
                elif pythonrun.weekday()==5 and run <= closingtime:
                    closed = False
                elif pythonrun.weekday()==7 and run > openingtime:
                    closed = False
                elif pythonrun.weekday()==7 and run <= openingtime:
                    closed = True
                elif pythonrun.weekday()==6:
                    closed = True
                else:
                    isHoliday = False
                self.assertEqual(not closed, boerse.is_businesshour(run), 'failed comparison for date %s' % str(run))
                run += delta
            pass
        def id(self): return "testForexMarket"
        def shortDescription(self): return "Tests a market of type 'Forex' against 3 years with a 5 minute step."

    class marketTestForexWthWeekendsMarket(unittest.TestCase):
        def testForexWthWeekendsMarket(self):
            """testForexWthWeekendsMarket tests a market of type 'Forex w/o weekends' for 3 years
               against weekends with a time step of 5 minutes."""
            name = 'Forex w/o weekends'
            CHF = calendars.CHF()
            Type = 'Forex w/o weekends'
            openingHour = 8.25
            closingHour = 17.10
            timezone = 'Europe/Zurich'
            boerse = market(name, [CHF], Type, openingHour, closingHour, timezone)
            start = datetime.datetime(2003,1,1,0,0,0)
            end = datetime.datetime(2006,1,1,0,0,0)
            delta = datetime.timedelta(minutes=5)
            run = start
            while run < end:
                self.assertEqual(True, boerse.is_businesshour(run),'failed comparison of all values of day %s' % str(run))
                run += delta
            pass
        def id(self): return "testForexWthWeekendsMarket"
        def shortDescription(self): return "Tests a market of type 'Forex w/o weekends' against 3 years of known CHF holidays and weekends."

    class marketTestBadFormatting(unittest.TestCase):
        def testBadFormattedValues(self):
            """ testBadFormattedValues tests the market constructor against malformed arguments. """
            names = [123, 123.12, calendars.USD(), [] ]
            for name in names:
                self.assertRaises(Exception, market, name, calendars.USD(), 'normal', 22.0, 22.0, '')
            pass
            name = ''
            cals = ['bbb',123, 1234.0,[]]
            for cal in cals:
                self.assertRaises(Exception, market, name, [cal], 'normal', 22.0, 22.0, '')
            cal = calendars.USD()
            Types = ['bbb',123, 1234.0,[], 'Normal', 'FX']
            for Type in Types:
                self.assertRaises(Exception, market, name, [cal], Type, 22.0, 22.0, '')
            Type = 'normal'
            numbers = ['aaa',[], calendars.USD()]
            for number in numbers:
                self.assertRaises(Exception, market, name, [cal], Type, number, 22.0, '')
                self.assertRaises(Exception, market, name, [cal], Type, 22.0, number, '')
            timezones = [123, 1234.2, [], calendars.USD()]
            for timezone in timezones:
                self.assertRaises(Exception, market, name, [cal], Type, 22.0, 22.0, timezone)
        def id(self): return "testBadFormattedValues"
        def shortDescription(self): return """Test against malformatted arguments. """



    result = unittest.TestResult()
    suite = unittest.TestSuite()
    suite.addTest(marketTestBadFormatting("testBadFormattedValues"))
    suite.addTest(marketTestAllValuesUSD("testAllValues"))
    suite.addTest(marketTestForexMarket("testForexMarket"))
    suite.addTest(marketTestForexWthWeekendsMarket("testForexWthWeekendsMarket"))
    suite.addTest(marketTestNormalMarket("testNormalMarket"))
    result = unittest.TextTestRunner(stream=sys.stdout, verbosity=2).run(suite)
    if result.wasSuccessful():
        print 'Unittest properly executed with %d tests, %d failed.' % (result.testsRun, len(result.failures))
    else:
        print 'Unittest failed: %d failures, %d errors!' % (len(result.failures),len(result.errors))
