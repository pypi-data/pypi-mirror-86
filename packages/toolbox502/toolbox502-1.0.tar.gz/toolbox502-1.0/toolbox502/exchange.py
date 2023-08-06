import requests
import pandas as pd

URL = "https://gist.githubusercontent.com/girvan/ba84c30ec97cb452b98a5bcab153638e/raw/4e7806001686573d4a0dcb947cf1f8c6343c0bf7/country-code-to-currency-code-mapping.csv"
DF = pd.read_csv(URL)


def get_code(name):
    """
    Will return code of currency of the given country.
    """
    if name in DF["Country"].get_values():
        return DF[DF["Country"] == name]["Code"].values[0]
    return "Doesn't exist"


def check_country(name):
    if name in DF["Country"].get_values():
        return True
    return False


def get_exchange_rate_code(ref_code, comp_code):
    """
    Will return the exchange rate 1 ref_code: X comp_code
    """
    url = "https://api.exchangerate-api.com/v4/latest/"
    response = requests.get(url + ref_code)
    return response.json()["rates"][comp_code]


def get_exchange_rate(country_ref, country_comp):
    """
    Will return the exchange 1 country_a : X country_b
    """
    first_code = get_code(country_ref)
    second_code = get_code(country_comp)
    return get_exchange_rate_code(first_code, second_code)


def get_countries():
    return DF[["Countries"]]


if __name__ == "__main__":
    print(get_exchange_rate("France", "Germany"))
    print(get_code("France"))
