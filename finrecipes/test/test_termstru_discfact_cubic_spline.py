""" ******************************************************

    Unittest term_structure_discount_factor_cubic_spline
    
    description:    unit test suite based on
                    module pytest

    arguments       Python-type description
    -----------------------------------------------------
        
    status
    -----------------------------------------------------
    syntax          OK
    numeric         OK
    pytest          
    literature-ref  --
*******************************************************"""
import pytest
import pandas as pd
from finrecipes.termstru_discfact_cubic_spline import *

@pytest.fixture(autouse=True)
def load_sample_data():
    df = pd.read_excel(
        "test_termstru_discfact_cubic_spline.xlsx",
        usecols=["x","y"],
        )
    return df


def test_termstru_discfact_cubic_spline():
    
    # Unittest of the calculations
    # See p. 299 of manual course Cox GE
    # Test of well-known serpentine-curve: f(x/(0.25 + x*x))
    # unittest accuracy requirement: deviation numeric approximation to analytical solution <= 1%

    def serpentine_curve(x):
        return x/(0.25 + x*x)
    t = [-1.25,-1.15,-1.05,-0.95,-0.85,-0.75,-0.65,-0.55,-0.45,-0.35,-0.25,
         -0.15,-0.05,0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95,1.05,1.15,1.25]
    
    y = [-0.689655172414,-0.731319554849,-0.776340110906,-0.824295010846,-0.874035989717, \
         -0.923076923077,-0.966542750929,-0.995475113122,-0.994475138122,-0.939597315436, \
         -0.8,-0.550458715596,-0.19801980198,0.19801980198,0.550458715596,0.8, \
         0.939597315436,0.994475138122,0.995475113122,0.966542750929,0.923076923077, \
         0.874035989717,0.824295010846,0.776340110906,0.731319554849,0.689655172414]
    n = len(t) - 1
    
    z = spline3_coef(t, y)
    
    for i in numpy.arange(-1.25,1.3,0.05):
        num = spline3_eval(t,y,z,i)
        analyt = serpentine_curve(i)
        deviationPercent = (analyt - num) / analyt * 100.0
        assert round(deviationPercent, 0) == 0.0
        #print('x = %1.2f,\twith cubic splines: %1.6f,\tanalytic: %1.6f' \
        #      % (i, spline3_eval(t,y,z,i), serpentine_curve(i)))
