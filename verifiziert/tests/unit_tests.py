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
import fin_recipes

# manual identification
tested_modules = [
    r'verifiziert\tests\test_termstru_discfact_cubic_spline.py',
    r'verifiziert\tests\test_random_normal.py']

# automatic test discovery
pytest.main()