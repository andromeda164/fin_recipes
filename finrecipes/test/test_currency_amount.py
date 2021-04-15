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
        if amount == 1.265:
            assert 2.50 == (CHF+CHF).amount()
            assert 2.52 == (EUR+EUR).amount()
            assert 2.52 == (USD+USD).amount()
            assert 0.00 == (ITL+ITL).amount()
        elif amount == 0.023:
            assert 0.00 == (CHF+CHF).amount()
            assert 0.04 == (EUR+EUR).amount()
            assert 0.04 == (USD+USD).amount()
            assert 0.0  == (ITL+ITL).amount()
        elif amount == 24.99:
            assert 50.0 == (CHF+CHF).amount()
            assert 49.98 == (EUR+EUR).amount()
            assert 49.98 == (USD+USD).amount()
            assert 0.0 == (ITL+ITL).amount()
        elif amount == 25.1:
            assert 50.20 == (CHF+CHF).amount()
            assert 50.20 == (EUR+EUR).amount()
            assert 50.20 == (USD+USD).amount()
            assert 100.00 == (ITL+ITL).amount()
        elif amount == 997.75:
            assert 1995.5 == (CHF+CHF).amount()
            assert 1995.5 == (EUR+EUR).amount()
            assert 1995.5 == (USD+USD).amount()
            assert 2000.0 == (ITL+ITL).amount()
        elif amount == 0.0:
            assert 0.0 == (CHF+CHF).amount()
            assert 0.0 == (EUR+EUR).amount()
            assert 0.0 == (USD+USD).amount()
            assert 0.0 == (ITL+ITL).amount()
            
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

        # test / // amount
        if CHF.amount() != 0.0:
            assert 1.0 == (CHF/CHF).amount()
        else:
             # division by zero raises ZeroDivisionError
            with pytest.raises(ZeroDivisionError):
                CHF/CHF
            with pytest.raises(ZeroDivisionError):
                CHF//CHF

        if EUR.amount() != 0.0:
            assert 1.0 == (EUR/EUR).amount()
        else:
            # division by zero raises ZeroDivisionError
            with pytest.raises(ZeroDivisionError):
                EUR/EUR
            with pytest.raises(ZeroDivisionError):
                EUR//EUR

        if USD.amount() != 0.0:
            assert 1.0 == (USD/USD).amount()
        else:
            # division by zero raises ZeroDivisionError
            with pytest.raises(ZeroDivisionError):
                USD/USD
            with pytest.raises(ZeroDivisionError):
                USD//USD

        if ITL.amount() != 0.0:
            # result raw is 1.0 --> 0 Lire
            assert 0.0 == (ITL/ITL).amount()
        else:
            # division by zero raises ZeroDivisionError
            with pytest.raises(ZeroDivisionError):
                ITL/ITL
            with pytest.raises(ZeroDivisionError):
                ITL//ITL

        # test // amount
        #assert 1.0 == (CHF//CHF).amount()
        #assert 1.0 == (EUR//EUR).amount()
        #assert 1.0 == (USD//USD).amount()
#        assert 1.0 == (ITL//ITL).amount()

         # test % rawAmount
##        if amount == 1.265:
##            assert 1.0 == ((1.0+CHF)//CHF).amount()
##            assert 1.0 == ((1.0+EUR)//EUR).amount()

        # print(float(CHF), CHF+CHF, CHF-CHF, CHF*CHF, CHF/CHF, CHF//CHF, CHF%CHF)

