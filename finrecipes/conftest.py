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


