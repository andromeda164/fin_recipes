import pytest
#import requests
import pandas as pd

# disable any network call during test (even by error)
# @pytest.fixture(autouse=True)
# def disable_network_calls(monkeypatch):
#     def stunted_get():
#         raise RuntimeError("Network access not allowed during testing!")
#     monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_get())

@pytest.fixture(autouse=True)
def load_sample_data():
    df = pd.read_excel(
        r".\datasets\test_termstru_discfact_cubic_spline.xlsx",
        usecols=[
            "x",
            "y"
        ],
    )