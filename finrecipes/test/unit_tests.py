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
import sys 
sys.path.append(r'..\..')
import pytest
import finrecipes

test_single_module = False
max_errors = 10     # number errors before stopping

# manual identification of single modules
if test_single_module:
    argument_list = [r'test_termstru_discfact_cubic_spline.py']
else:
    argument_list = []

# automatic test discovery
pytest.main(argument_list)
