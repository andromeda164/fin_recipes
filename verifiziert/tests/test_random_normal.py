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
import pytest, fin_recipes
from random_normal import *

def test_random_normal():
    # Unittest of the calculations
    # unittest accuracy requirement: deviation numeric approximation to analytical solution <= 1%
    MAXINDEX = 1000000
    # run a statistical test with MAXINDEX runs
    results = numpy.zeros((MAXINDEX+1))
    for i in range(MAXINDEX):
        results[i] = random_normal()
    # mean of a random normal variable should be 0
    assert round(numpy.average(results), 2) == 0.0
    # variance of a random normal variable should be 1
    assert round(numpy.var(results), 2) == 1.0
    return