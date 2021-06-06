""" ******************************************************

    Unittest for random_normal
    
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
from finrecipes.anal_price_am_call_div import *

@pytest.mark.parametrize(
    "S,K,r,sigma,tau,D1,tau1,expected",
    [
        (100.0,100.0,0.1,0.25,1.0,10.0,0.5,10.0166)
    ]
)

def test_option_price_american_call_one_dividend(S,K,r,sigma,tau,D1,tau1, expected):
    # The Roll-Geske-Whaley-Formula result for an example option should be 10.0166
    # Derivagem calculates 10.0088
    assert option_price_american_call_one_dividend(S,K,r,sigma,tau,D1,tau1) == expected

