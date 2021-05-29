import pytest
#import requests
import pandas as pd

# disable any network call during test (even by error)
#  @pytest.fixture(autouse=True)
#  def disable_network_calls(monkeypatch):
#      def stunted_get():
#          raise RuntimeError("Network access not allowed during testing!")
#      monkeypatch.setattr(requests, "get", lambda *args, **kwargs: stunted_get())

# this is not supported at the root level, only below
#pytest_plugins = [
    # add here any fixture plugin
    #  "tests.unit.fixtures.some_stuff",
#]



@pytest.fixture(autouse=True, scope="session")
def load_sample_cubic_spline_data():
    df_cubic_spline = pd.read_excel(
        r"/finrecipes/test/test_termstru_discfact_cubic_spline.xlsx",
        usecols=["x","y"],
        )
    return df_cubic_spline

