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
import sys 
sys.path.append(r'..\..')
import pytest
from finrecipes import currency_amount
from finrecipes import calendars


def test_currency_amount():
    # Test for class currency_amount
    # ------------------------------
    amounts = [1.265, 0.023, 24.99, 25.1, 99.1, 997.75, 0.0]

    # Rounding test
    for amount in amounts:
        CHF = currency_amount.currency_amount(amount, 'CHF', 'Swiss Franc', calendars.CHF(), 2, 5)
        EUR = currency_amount.currency_amount(amount, 'EUR', 'Euro', calendars.TARGET(), 2, 1)
        USD = currency_amount.currency_amount(amount, 'USD', 'US Dollar', calendars.USD(), 2, 1)
        ITL = currency_amount.currency_amount(amount, 'ITL', 'Lire Italiane', calendars.TARGET(), -1, 5)
        if CHF.amount() == 0.0:
            # division by zero raises ZeroDivisionError
            with pytest.raises(ZeroDivisionError):
                CHF/CHF
        if EUR.amount() == 0.0:
            # division by zero raises ZeroDivisionError
            with pytest.raises(ZeroDivisionError):
                EUR/EUR
        if USD.amount() == 0.0:
            # division by zero raises ZeroDivisionError
            with pytest.raises(ZeroDivisionError):
                USD/USD
        if ITL.amount() == 0.0:
            # division by zero raises ZeroDivisionError
            with pytest.raises(ZeroDivisionError):
                ITL/ITL
        # test + rawAmount
        assert amount*2 == (CHF+CHF).rawAmount()
        assert amount*2 == (EUR+EUR).rawAmount()
        assert amount*2 == (USD+USD).rawAmount()
        assert amount*2 == (ITL+ITL).rawAmount()

        # test - rawAmount
        assert 0.0 == (CHF-CHF).rawAmount()
        assert 0.0 == (EUR-EUR).rawAmount()
        assert 0.0 == (USD-USD).rawAmount()
        assert 0.0 == (ITL-ITL).rawAmount()

        # test - amount
        assert 0.0 == (CHF-CHF).amount()
        assert 0.0 == (EUR-EUR).amount()
        assert 0.0 == (USD-USD).amount()
        assert 0.0 == (ITL-ITL).amount()

        # test / amount
        assert 1.0 == (CHF/CHF).amount()
        assert 1.0 == (EUR/EUR).amount()
        assert 1.0 == (USD/USD).amount()
        assert 1.0 == (ITL/ITL).amount()

        # test // amount
        assert 1.0 == (CHF//CHF).amount()
        assert 1.0 == (EUR//EUR).amount()
        assert 1.0 == (USD//USD).amount()
        assert 1.0 == (ITL//ITL).amount()

        # print(float(CHF), CHF+CHF, CHF-CHF, CHF*CHF, CHF/CHF, CHF//CHF, CHF%CHF)

