""" ******************************************************

    Datums-Klasse

    Beschreibung:   Klasse fuer die mathematische
                    Beschreibung eines Datums.

                    Es sind die folgenden Operationen
                    definiert:
                    
                    Vergleichs-Operatoren:
                    ==, !=, <, >, <=, >=
                    Assigments:
                    +=, -=
                    Arithmetik:
                    -

                    Achtung: plus hat fuer Datuemer keinen
                    Sinn!

                    Der Konstruktor ist flexibel ausgelegt,
                    es koennen Datuemer in den folgenden
                    Formaten geliefert werden:

                    US          mm/dd/yyyy
                    USserial    yyyymmdd oder yymmdd
                    EU          dd.mm.yyyy - Separator egal!
                    separated   (dd, mm, yyyy), als Tupel
                    PythonDate  Copy Construktor-Emulation
                                mit derselben date-Klasse
                                als Argument
                    autodetect  autodetect!
                    
                    Usage:
                    d1 = date('US','12/22/2004')
                    d2 = date('PythonDate',d1)
                    d3 = date('USserial',041222)
                    d4 = date('USserial',20041222)
                    d5 = date('EU','22.12.2005')
                    d6 = date('EU','22$12$2005') - es kommt
                        hier nicht auf den Separator an!
                    d7 = date('separated',22,12,2004)
                    d8 = date('autodetect','22.12.2005')
                    d9 = date('autodetect','12/22/2005')
                    d10 = date('autodetect','2005-12-22')

                    Es kann zusaetzlich ein drittes Argument
                    mitgegeben werden, das bei Ultimo-Daten
                    bei Addition/Subtraktion von Monaten immer
                    das Monatsende belaesst (Achtung: NUR bei
                    Monats-Arithmetik!)

                    Also fuer Ultimo-Daten:
                    d10 = date('autodetect','2005-12-31', True)

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    siehe Sektion Usage

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur       OK
*******************************************************"""
import datetime, math
import fin_recipes
import calendar # native module
import calendars # my module
DEBUG = 0

class date:
    """ Datums-Klasse """
    def __init__(self, mode, *rest):
        # fuer mode und *rest siehe Modul-Docstring!
        self.separator = '.'
        if mode=='US':
            # Format: mm/dd/yyyy
            # Separator: Laenge: 1 Buchstabe, egal welcher
            self.year_  = int(rest[0][6:10])
            self.month_ = int(rest[0][0:2])
            self.day_   = int(rest[0][3:5])
            try:
                self.datum = datetime.date(self.year_, self.month_, self.day_)
            except Exception as detail:
                raise Exception('Exception happened in dates.date (US): %s\nValues: day %d, month %d, year %d' \
                      % (detail, self.day_, self.month_, self.year_))
            if len(rest)>1:
                self.ultimo_ = rest[1]
            else:
                self.ultimo_ = False
        elif mode=='USserial':
            # Format: yyyymmdd oder yymmdd
            # Unterscheidung nach Laenge
            if len(str(rest[0]))==6:
                y = int(str(rest[0])[0:2])
                if y<30:
                    # the simplest possible fix for Y2K,
                    # choose 2K if year < 30 (unusual that
                    # dates before 1930 is referred to
                    # year_ = 2000+y
                    self.year_ = 2000+y
                else:
                    self.year_ = 1900+y
                self.month_ = int(str(rest[0])[2:4])
                self.day_   = int(str(rest[0])[4:6])
            else:
                self.year_  = int(str(rest[0])[0:4])
                self.month_ = int(str(rest[0])[4:6])
                self.day_   = int(str(rest[0])[6:8])
            try:
                self.datum = datetime.date(self.year_, self.month_, self.day_)
            except Exception as detail:
                raise Exception('Exception happened in dates.date (USserial): %s\nValues: day %d, month %d, year %d' \
                      % (detail, self.day_, self.month_, self.year_))
            if len(rest)>1:
                self.ultimo_ = rest[1]
            else:
                self.ultimo_ = False
            if DEBUG:
                print('USserial date: ', str(rest[0]), str(self.datum))
        elif mode=='EU':
            # Format: dd.mm.yyyy
            # Separator: Laenge: 1 Buchstabe,
            # egal was
            self.year_  = int(rest[0][6:10])
            self.month_ = int(rest[0][3:5])
            self.day_   = int(rest[0][0:2])
            try:
                self.datum = datetime.date(self.year_, self.month_, self.day_)
            except Exception as detail:
                raise Exception('Exception happened in dates.date (EU): %s\nValues: day %d, month %d, year %d' \
                      % (detail, self.day_, self.month_, self.year_))
            if len(rest)>1:
                self.ultimo_ = rest[1]
            else:
                self.ultimo_ = False
        elif mode=='separated':
            # Format: (dd, mm, yyyy)
            self.month_ = int(rest[1])
            self.day_ = int(rest[0])
            y = int(rest[2])
            if y<100:
                if y<25:
                    # the simplest possible fix for Y2K,
                    # choose 2K if year < 20 (unusual that
                    # dates before 1930 is referred to
                    # year_ = 2000+y
                    self.year_ = 2000+y
                else:
                    self.year_ = 1900+y
            else:
                self.year_ = y
            try:
                self.datum = datetime.date(self.year_, self.month_, self.day_)
            except Exception as detail:
                raise Exception('Exception happened in dates.date (separated): %s\nValues: day %d, month %d, year %d' \
                      % (detail, self.day_, self.month_, self.year_))
            if len(rest)>4:
                self.ultimo_ = rest[1]
            else:
                self.ultimo_ = False
            if DEBUG:
                print('separated date: ', str(rest), str(self.datum))
        elif mode=='PythonDate':
            data = rest[0]
            if not isinstance(data,datetime.date):
                raise Exception('Invalid date furnished in section PythonDate (%s)!' % str(data))
            self.datum = data
            self.year_ = data.year
            self.month_ = data.month
            self.day_ = data.day
            if len(rest)>1:
                self.ultimo_ = rest[1]
            else:
                self.ultimo_ = False
            if DEBUG:
                print('Python date: ', str(rest), str(self.datum))
        elif mode=='autodetect':
            data = rest[0]
            if type(data)!=type(''):
                if not isinstance(data, date):
                    if not isinstance(data,datetime.date):
                        raise Exception('Only strings/python dates allowed for option autodetect!')
            if isinstance(data, date):
                self.datum = data.datum
                self.year_ = data.year()
                self.month_ = data.month()
                self.day_ = data.day()
                if DEBUG:
                    print('autodetect date: ', str(rest), str(self.datum))
            elif type(data)==type(datetime.date):
                self.datum = data
                self.year_ = data.year
                self.month_ = data.month
                self.day_ = data.day
            elif type(data)==type(''):
                date_separator = ''
                separator_position = []
                for c in range(len(data)):
                    try:
                        temp = int(data[c])
                    except:
                        date_separator = data[c]
                        separator_position.append(c)
                if DEBUG:
                    print('Separator %s positions: %s' \
                          % (date_separator, str(separator_position)))
                if len(separator_position)!=2:
                    raise Exception('Unknown autodetect date format %s!' % data)
                if separator_position[0]==4 and separator_position[1]==7 and \
                   date_separator=='-':
                    # US date format '2004-01-12'
                    self.year_ = int(data[0:4])
                    self.month_ = int(data[5:7])
                    self.day_ = int(data[8:10])
                elif separator_position[0]==2 and separator_position[1]==5 and \
                   date_separator=='.':
                    # EU date format '12.01.2004'
                    self.year_ = int(data[6:10])
                    self.month_ = int(data[3:5])
                    self.day_ = int(data[0:2])
                elif separator_position[0]==2 and separator_position[1]==5 and \
                   date_separator=='/':
                    # US date format '01/12/2004'
                    self.year_ = int(data[6:10])
                    self.month_ = int(data[0:2])
                    self.day_ = int(data[3:5])
                else:
                    raise Exception('Unknown autodetect date format %s!' % data)
                try:
                    self.datum = datetime.date(self.year_, self.month_, self.day_)
                except Exception as detail:
                    raise Exception('Exception happened in dates.date (EU): %s\nValues: day %d, month %d, year %d' \
                          % (detail, self.day_, self.month_, self.year_))
            if len(rest)>1:
                self.ultimo_ = rest[1]
            else:
                self.ultimo_ = False
            if DEBUG:
                print('autodetect date: ', str(rest), str(self.datum))
        else:
            raise Exception('Unknown date construction format %s!' \
                  % (mode))
        if not self.valid():
            raise Exception('Invalid date furnished (%s)!' % (str(rest)))
        pass

    def valid(self):
        """ eigentlich nicht notwendig, da die Funktion durch das interne datetime-Objekt
            automatisch bei der Konstruktion geprueft wird! """
        # This function will check the given date is valid or not.
        # If the date is not valid then it will return the value False.
        # Need some more checks on the year, though - for leap years only primitive
        # check implemented - every four years
        if self.year_<0: return False
        if self.month_>12 or self.month_<1: return False
        if self.day_>31 or self.day_<1: return False
        if self.day_==31 and \
                ( self.month_==2 or self.month_==4 or self.month_==6 or \
                  self.month_==9 or self.month_==11): return False
        if self.day_==30 and self.month_==2: return False
        if self.day_==29 and self.month_==2 and (self.year_%4!=0.0): return False
        #if self.ultimo_==True and self.is_ultimo()==False: return False
        return True

    def day(self): return self.day_
    def month(self): return self.month_
    def year(self): return self.year_

    def set_day(self, day):
        self.day_ = day
        self.datum = datetime.date(self.year_, self.month_, self.day_, self.ultimo_)
        
    def set_month(self, month):
        self.month_ = month
        self.datum = datetime.date(self.year_, self.month_, self.day_, self.ultimo_)
        
    def set_year(self, year):
        self.year_ = year
        self.datum = datetime.date(self.year_, self.month_, self.day_, self.ultimo_)

    def __eq__(self, other):
        # check for equality
        if not self.valid(): return False
        if not other.valid(): return False
        if (self.day()==other.day()) and (self.month()==other.month()) \
            and (self.year()==other.year()): return True
        return False

    def __ne__(self, other):
        return not (self==other)

    def __lt__(self, other):
        if not self.valid(): return False  # not  meaningful, return anything
        if not other.valid(): return False    # should really be an exception, but ?
        if self.year() < other.year(): return True
        else:
            if self.year()>other.year(): return False
            else:
                # same year
                if self.month()<other.month(): return True
                else:
                    if self.month()>other.month(): return False
                    else: # same  month
                        if self.day()<other.day(): return True
                        else: return False
        return False

    def __gt__(self, other):
        if self==other: return False  # this is strict inequality 
        if self<other: return False
        return True

    def __le__(self, other):
        if self==other: return True
        return self<other

    def __ge__(self, other):
        if self==other: return True
        return self>other

    def next_day(self):
        diff = datetime.timedelta(days=1)
        data = self.datum + diff
        newDate = date('PythonDate',data)
        return newDate

    def previous_day(self):
        diff = datetime.timedelta(days=-1)
        data = self.datum + diff
        newDate = date('PythonDate',data)
        return newDate

    def next_month(self):
        return self.add_months(1)

    def previous_month(self):
        return self.add_months(-1)

    def ultimo_date(self):
        """ For addition/subtraction, should the date be considered always an ultimo date? """
        return self.ultimo_

    def ultimo(self):
        """ Returns the last calendar day in the month of the date considered. """
        next_month = self.add_months(1)
        first_day_next_month = date('separated', 1, next_month.month(), next_month.year())
        return first_day_next_month.previous_day()

    def is_ultimo(self):
        """ Returns true, if the date is effectively the last calendar day in the month. """
        if self==self.ultimo(): return True
        return False

    def is_feb_ultimo(self):
        if self==self.ultimo():
            if self.month()==2:
                return True
        return False

    def weekday(self):
        """ 1 fuer Montag, 7 fuer Sonntag """
        return self.datum.isoweekday()

    def is_leap_year(self):
        return calendar.isleap(self.year_)

    def is_weekend(self):
        return self.weekday()>5

    def is_businessday(self, calendarlist):
        result = True
        for cal in calendarlist:
            if not cal.is_businessday(self): result = False
        return result

    def add_banking_days(self, days, calendarlist):
        data = date('autodetect',self)
        if days>=0: direction = 1
        else: direction = -1
        counter = 0
        while counter<abs(days):
            data += direction
            if data.is_businessday(calendarlist):
                counter += 1
        return data

    def first_of_month(self):
        next_month = self.add_months(1)
        return date('separated', 1, next_month.month(), next_month.year())

    def int_date(self):
        if self.valid():
            return self.year() * 10000 + self.month() * 100 + self.day()
        return -1

    def __str__(self):
        if self.valid():
            if self.day_<10: day = '0' + str(self.day_)
            else: day = str(self.day_)
            if self.month_<10: month = '0'+str(self.month_)
            else: month = str(self.month_)
            return day + self.separator + month \
                   + self.separator + str(self.year_)
        else:
            raise Exception('Invalid date (%s)!' % (str(self.int_date())))

    def __repr__(self):
        if self.valid():
            return str(self.day_) + self.separator + str(self.month_) \
                   + self.separator + str(self.year_)
        else:
            raise Exception('Invalid date (%s)!' % (str(self.int_date())))

    def __add__(self, other):
        if type(other)==int:
            diff = datetime.timedelta(days=other)
            data = self.datum + diff
            newDate = date('PythonDate',data)
            return newDate
        else:
            raise Exception('Error in numeric date operation (add)!')
        pass
            
    def __iadd__(self, other):
        if type(other)==int:
            diff = datetime.timedelta(days=other)
            self.datum = self.datum + diff
            self.year_ = self.datum.year
            self.month_ = self.datum.month
            self.day_ = self.datum.day
            return self
        else:
            raise Exception('Error in numeric date operation (iadd)!')
        pass
            
    def __sub__(self, other):
        if type(other)==int:
            if DEBUG:
                print('I am subtracting from date %s %d days' % (str(self), other))
            diff = datetime.timedelta(days=-other)
            data = self.datum + diff
            newDate = date('PythonDate',data)
            return newDate
        else:
            try:
                if DEBUG:
                    print('I am subtracting from date %s the date %s' % (str(self), str(other)))
                diff = self.datum - other.datum
                return diff.days
            except Exception as detail:
                raise Exception('Error in numeric date operation (sub): %s!' % detail)
        pass

    def __isub__(self, other):
        if type(other)==int:
            diff = datetime.timedelta(days=-other)
            self.datum = self.datum + diff
            self.year_ = self.datum.year
            self.month_ = self.datum.month
            self.day_ = self.datum.day
            return self
        else:
            raise Exception('Error in numeric date operation (isub)!')
        pass

    def add_months(self, months):
        if type(months)==int:
            m = self.month_
            # bugfix bf2103-001 module dates (test failure)
            # added math.floor to year calculation
            y = self.year_ + math.floor((m+months-1)/12)
            if months>=0:
                m_ = m + months % 12
                if m_>12:
                    m = m_-12
                else:
                    m = m_
            else:
                m_ = m - abs(months)%12
                if m_<1:
                    m = m_ + 12
                else:
                    m = m_
            if self.day_>28 and m==2:
                if calendar.isleap(y):
                    d = 29
                else:
                    d = 28
            else:
                if self.day_==31 and m in [4,6,9,11]:
                    d = 30
                else:
                    d = self.day_
            newDate = date('separated', d, m, y)
            if self.ultimo_date():
                # Falls das Ausgangsdatum immer als Ultimo-Datum betrachtet werden soll,
                # dann muss das neue Datum ebenfalls ein Ultimo-Datum sein.
                #print 'Ist ultimo-date'
                m += 1
                if m>12:
                    y += 1
                    m -= 12
                newDate = date('separated', 1, m, y) - 1
            return newDate
        else:
            raise Exception('Error in numeric date operation (add_months)!')
        pass


# Allgemeine Hilfsfunktion
def invalid_date(dd, mm, yyyy):
    """ Gibt True fuer ein ungueltiges Datum zurueck. """
    try:
        if DEBUG:
            print('Verification of date %d.%d.%d.' % (dd,mm,yyyy))
        d = date('separated',dd,mm,yyyy)
        if DEBUG:
            print('Verification successful. Valid date!')
        return False
    except:
        if DEBUG:
            print('Verification failed. Invalid date!')
        return True


