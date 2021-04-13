""" ******************************************************

    Klasse currency_amount zur Modellierung eines Betrages
    in einer spezifischen Waehrung.

    Beschreibung:   Klasse zur Modellierung
                    eines Waehrungsbetrages.

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    amount          float       Betrag in einer Waehrung
    curr            class instance
                                Instanz der Klasse currency

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   --
*******************************************************"""
import math
from finrecipes.currency import *
from finrecipes import calendars

class currency_amount(currency.currency):
    """ Class for modelling an amount of a specific currency."""
    def __init__(self, amount, ISOCode, name, calendar = calendars.CHF(),
                 minDecimalPositionExponent = 2, minRoundingUnit = 5):
        currency.currency.__init__(self, ISOCode, name, calendar,
                      minDecimalPositionExponent,
                      minRoundingUnit)
        self.__rawAmount = amount
        rounded = amount * math.pow(10.0,minDecimalPositionExponent)
        if minRoundingUnit==1:
            rounded = round(rounded, 0) \
                      / math.pow(10.0,minDecimalPositionExponent)
        elif minRoundingUnit==5:
            rest = round(rounded, 0) % 10
            rounded = round(rounded, 0) - rest
            if rest < 3: rest = 0
            elif rest < 8: rest = 5
            else: rest = 10
            rounded = (rounded + rest) \
                      / math.pow(10.0,minDecimalPositionExponent)
        else:
            raise 'Minimum rounding unit %d not supported!' % minDecimalPositionExponent
        self.__amount = rounded
        pass

    def amount(self): return self.__amount

    def rawAmount(self): return self.__rawAmount
    
    def __add__(self, other):
        if self.ISOCode()!=other.ISOCode():
            raise ValueError('Amounts of different currencies cannot be added!')
        result = self.amount() + other.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __sub__(self, other):
        if self.ISOCode()!=other.ISOCode():
            raise ValueError('Amounts of different currencies cannot be subtracted!')
        result = self.amount() - other.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __mul__(self, other):
        if self.ISOCode()!=other.ISOCode():
            raise ValueError('Amounts of different currencies cannot be multiplied!')
        result = self.amount() * other.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __div__(self, other):
        if self.ISOCode()!=other.ISOCode():
            raise ValueError('Amounts of different currencies cannot be divided!')
        result = self.amount() / other.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __floordiv__(self, other):
        if self.ISOCode()!=other.ISOCode():
            raise ValueError('Amounts of different currencies cannot be divided!')
        result = self.amount() // other.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __mod__(self, other):
        if self.ISOCode()!=other.ISOCode():
            raise ValueError('Amounts of different currencies cannot be divided!')
        result = self.amount() % other.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __pow__(self, other):
        if self.ISOCode()!=other.ISOCode():
            raise ValueError('Amounts of different currencies cannot be divided!')
        result = self.amount() ** other.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __neg__(self):
        result = -self.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __pos__(self):
        result = self.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __abs__(self):
        result = abs(self.amount())
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __invert__(self):
        result = -self.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __int__(self):
        return int(self.amount())

    # 13/04/2021 Python 3 conversion: __long__/long as a datatype 
    # does not exist anymore, use int with full precision
    #def __long__(self):
    #    return long(self.amount())

    def __float__(self):
        return float(self.amount())

    def __cmp__(self, other):
        if isinstance(other,currency_amount):
            if self.__amount > other.amount(): return 1
            elif self.__amount == other.amount(): return 0
            else: return -1
        elif type(other)==float or type(other)==int:
            if self.__amount > other: return 1
            elif self.__amount == other: return 0
            else: return -1
        else:
            raise SyntaxError('comparison for the operand type not supported')

    ## Right hand arithmetic operations

    def __radd__(self, other):
        result = other + self.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __rsub__(self, other):
        result = other - self.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __rmul__(self, other):
        result = other * self.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __rdiv__(self, other):
        result = other / self.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __rfloordiv__(self, other):
        result = other // self.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __rmod__(self, other):
        result = other % self.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __rpow__(self, other):
        result = other ** self.amount()
        return currency_amount(result, self.ISOCode(), self.name(), \
                               self.calendar(), \
                               self.minDecimalPositionExponent(), \
                               self.minRoundingUnit())

    def __str__(self): return 'Currency amount %f in currency %s.' % (self.__amount, self.ISOCode())

    def __repr__(self): return 'Currency amount %f in currency %s.' % (self.__amount, self.ISOCode())


if __name__=="__main__":
    print('Test for class currency_amount')
    print('------------------------------')
    amounts = [1.265, 0.023, 24.99, 25.1, 99.1, 997.75]
    print()
    print('Rounding test')
    print()
    for amount in amounts:
        print('Testing amount of %f' % amount)
        CHF = currency_amount(amount, 'CHF', 'Swiss Franc', calendars.CHF(), 2, 5)
        EUR = currency_amount(amount, 'EUR', 'Euro', calendars.TARGET(), 2, 1)
        USD = currency_amount(amount, 'USD', 'US Dollar', calendars.USD(), 2, 1)
        ITL = currency_amount(amount, 'ITL', 'Lire Italiane', calendars.TARGET(), -1, 5)
        if CHF!=0.0:
            print(float(CHF), CHF+CHF, CHF-CHF, CHF*CHF, CHF/CHF, CHF//CHF, CHF%CHF)
        if EUR!=0.0:
            print(float(EUR), EUR+EUR, EUR-EUR, EUR*EUR, EUR/EUR, EUR//EUR, EUR%EUR)
        if USD!=0.0:
            print(float(USD), USD+USD, USD-USD, USD*USD, USD/USD, USD//USD, USD%USD)
        if ITL!=0.0:
            print(float(ITL), ITL+ITL, ITL-ITL, ITL*ITL, ITL/ITL, ITL//ITL, ITL%ITL)
        print()
    print('OK')

