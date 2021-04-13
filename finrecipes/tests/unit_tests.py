""" ******************************************************

    Unit test for FinancialRecipes
    
    description:    global unit test suite based on
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
import finrecipes

test_single_module = True
max_errors = 10     # number errors before stopping

# manual identification of single modules
if test_single_module:
    argument_list = [r'test_day_count.py']
else:
    argument_list = ['maxfail', max_errors]

# automatic test discovery
pytest.main(argument_list)