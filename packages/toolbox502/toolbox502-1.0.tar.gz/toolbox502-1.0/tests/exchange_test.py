import os
import toolbox502
import pandas as pd

# Import from our exchange file
from toolbox502.exchange import (
    get_code,
    check_country,
    get_exchange_rate,
    get_exchange_rate_code,
)
import pytest


def test_get_code():
    assert get_code("France") == "EUR"
    assert get_code("Germany") == "EUR"


def test_check_country():
    assert check_country("France") == True
    assert check_country("mvifornitv") == False


def test_get_exchange_rate_code():
    assert get_exchange_rate_code("EUR", "EUR") == 1


def test_get_exchange_rate():
    assert get_exchange_rate("France", "Germany") == 1
