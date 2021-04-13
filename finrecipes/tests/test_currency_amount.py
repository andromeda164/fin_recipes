""" ******************************************************

    Unittest for currency_amount
    
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
from finrecipes.currency_amount import *


def test_currency_amount():
    # Test for class currency_amount
    # ------------------------------
    amounts = [1.265, 0.023, 24.99, 25.1, 99.1, 997.75, 0.0]

    # Rounding test
    for amount in amounts:
        CHF = currency_amount(amount, 'CHF', 'Swiss Franc', calendars.CHF(), 2, 5)
        EUR = currency_amount(amount, 'EUR', 'Euro', calendars.TARGET(), 2, 1)
        USD = currency_amount(amount, 'USD', 'US Dollar', calendars.USD(), 2, 1)
        ITL = currency_amount(amount, 'ITL', 'Lire Italiane', calendars.TARGET(), -1, 5)
        if amount == 0.0:
            # division by zero raises ValueError
            with pytest.raises(ValueError):
                CHF/CHF
            with pytest.raises(ValueError):
                EUR/EUR
            with pytest.raises(ValueError):
                USD/USD
            with pytest.raises(ValueError):
                ITL/ITL
            with pytest.raises(ValueError):
                CHF//CHF
            with pytest.raises(ValueError):
                EUR//EUR
            with pytest.raises(ValueError):
                USD//USD
            with pytest.raises(ValueError):
                ITL//ITL
        else:
            assert amount*2 == (CHF+CHF).rawAmount()
            assert CHF+CHF == 2.55
            print(float(CHF), CHF+CHF, CHF-CHF, CHF*CHF, CHF/CHF, CHF//CHF, CHF%CHF)
        if EUR!=0.0:
            print(float(EUR), EUR+EUR, EUR-EUR, EUR*EUR, EUR/EUR, EUR//EUR, EUR%EUR)
        if USD!=0.0:
            print(float(USD), USD+USD, USD-USD, USD*USD, USD/USD, USD//USD, USD%USD)
        if ITL!=0.0:
            print(float(ITL), ITL+ITL, ITL-ITL, ITL*ITL, ITL/ITL, ITL//ITL, ITL%ITL)
