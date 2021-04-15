""" ******************************************************

    Klasse fx_spot_deal zur Modellierung eines
    FX Spot Deals.

    Beschreibung:   Klasse zur Modellierung
                    eines FX Spot Deals.

                    Es muessen zwei der drei Variablen
                    base_amount, counter_amount und fx_rate
                    mitgeliefert werden.

                    Buy/Sell wird ueber positiv/negativ-
                    Betraege gesteuert (positiver Betrag
                    wird gekauft)

    Argumente       Python-Typ  Beschreibung
    -----------------------------------------------------
    transaction_date
                    class instance
                                Instanz der Klasse
                                dates.date, datetime.date
                                oder string
    base_amount     float       Betrag Base Currency
    counter_amount  float       Betrag Counter Currency
    fx_rate         float       FX Rate des Deals
    fx_pair         class instance
                                Instanz der Klasse fx_pair

    Status
    -----------------------------------------------------
    Syntax          OK
    Numerisch       OK
    Testprogramm    OK
    Literatur-Ref   OK
*******************************************************"""
import math
from finrecipes import fx_pair, calendars, dates, datetime, currency

class fx_spot(fx_pair.fx_pair):
    """ Class for modelling an FX Spot transaction."""
    def __init__(self, pair, transaction_date, base_amount = 0.0, counter_amount = 0.0, fx_rate = 0.0):
        if not isinstance(pair, fx_pair.fx_pair):
            raise TypeError('fx pair furnished is not a fx_pair instance!')
        fx_pair.fx_pair.__init__(self, pair.baseCurr(), pair.counterCurr(), pair.basis())
        if fx_rate:
            if base_amount:
                counter_amount = - base_amount * fx_rate / pair.basis()
            elif counter_amount:
                base_amount = - counter_amount / fx_rate * pair.basis()
            else:
                raise ValueError('Either base or counter currency amount must be not equal 0.')
        elif base_amount and counter_amount:
            fx_rate = -counter_amount / base_amount * pair.basis()
        else:
            raise ValueError('Two of fx_rate,  base or counter currency amount must be not equal 0.')
        self.__fx_rate = fx_rate
        self.__base_amount = base_amount
        self.__counter_amount = counter_amount
        self.__transaction_date = dates.date('autodetect',transaction_date)
        if self.__base_amount > 0.0: self.__buy_sell = 'BUY'
        else: self.__buy_sell = 'SELL'
        self.__value_date = self.__transaction_date.add_banking_days(2, pair.calendarList())
        pass

    def baseAmount(self): return self.__base_amount
    def counterAmount(self): return self.__counter_amount
    def fxRate(self): return self.__fx_rate
    def transactionDate(self): return self.__transaction_date
    def valueDate(self): return self.__value_date
    def buySell(self): return self.__buy_sell
    def __str__(self): return 'FX Spot deal (%s %f %s against %f %s @ %f)' % (self.__buy_sell, self.__base_amount, self.baseCurr().ISOCode(), self.__counter_amount, self.counterCurr().ISOCode(), self.__fx_rate)
    def __repr__(self): return 'FX Spot deal (%s %f %s against %f %s @ %f)' % (self.__buy_sell, self.__base_amount, self.baseCurr().ISOCode(), self.__counter_amount, self.counterCurr().ISOCode(), self.__fx_rate)


if __name__=="__main__":
    print('Test for class fx_spot')
    print('----------------------')
    CHF = currency.currency('CHF', 'Swiss Franc', calendars.CHF(), 2, 5)
    EUR = currency.currency('EUR', 'Euro', calendars.TARGET(), 2, 1)
    USD = currency.currency('USD', 'US Dollar', calendars.USD(), 2, 1)
    JPY = currency.currency('JPY', 'Japanese Yen', calendars.USD(), 0, 1)
    ITL = currency.currency('ITL', 'Lire Italiane', calendars.TARGET(), -1, 5)
    pairs = [(fx_pair.fx_pair(EUR, CHF, 1.0), 1.6200), \
             (fx_pair.fx_pair(JPY, CHF, 100.0), 1.0250),
             (fx_pair.fx_pair(EUR, USD, 1), 1.2750)]
    transaction_date = '2007-01-22'
    amounts = [1.0, 100.0, 1000.0, 1000000.0]
    for pair, rate in pairs:
        for amount in amounts:
            bybase =    fx_spot(pair, transaction_date, base_amount=amount, fx_rate = rate)
            bycounter = fx_spot(pair, transaction_date, counter_amount=-amount*rate/pair.basis(), fx_rate = rate)
            byamount =  fx_spot(pair, transaction_date, base_amount=bybase.baseAmount(), counter_amount=bycounter.counterAmount())
            print('Should be all equal:')
            print(bybase)
            print(bycounter)
            print(byamount)
            print()
    print('OK')

