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
import sys
sys.path.append(r'F:\IT\TS\FinancialRecipes\Python\verifiziert')

tested_modules = [r'..\random_normal.py']

pytest.main(tested_modules)