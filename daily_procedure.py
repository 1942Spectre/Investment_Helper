import pandas as pd
import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from os import path
import datetime

##################################################
API_KEY = "YOU NEED TO DEFINE YOUR API KEY HERE"
##################################################


def get_converted_value(symbol, convert):
    url = "https://pro-api.coinmarketcap.com/v2/tools/price-conversion"
    parameters = {
        'amount': 1,
        'symbol': symbol,
        'convert': convert
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


# USD 
def get_dollar_assets(assets):
    asset_dict = dict()
    usd_dict = dict()
    for row_num in range(assets.shape[0]):
        row = assets.iloc[row_num]
        asset_dict[row["Currency"]] = row["Amount"]
    for currency in asset_dict.keys():
        if currency != "GAU":
            price = float(get_converted_value(currency, "USD")
                          ["data"][0]["quote"]["USD"]["price"])
            usd_dict[currency] = asset_dict[currency] * price
        if currency == "GAU":
            price = float(get_converted_value("XAU", "USD")[
                          "data"][1]["quote"]["USD"]["price"]) * 0.035274
            usd_dict[currency] = asset_dict[currency] * price
    return usd_dict


# The currency in Turkey is TRY, Turkish Liras.
def get_try_assets(assets):
    asset_dict = dict()
    try_dict = dict()
    for row_num in range(assets.shape[0]):
        row = assets.iloc[row_num]
        asset_dict[row["Currency"]] = row["Amount"]

    for currency in asset_dict.keys():

        if currency != "GAU":
            price = float(get_converted_value(currency, "TRY")
                          ["data"][0]["quote"]["TRY"]["price"])
            try_dict[currency] = asset_dict[currency] * price
        # Since we use GAU instead of XAU in my country
        # Gold in grams instead of ounces, and the API does not support GAU,
        # There is a conversion
        if currency == "GAU":
            price = float(get_converted_value("XAU", "TRY")[
                          "data"][1]["quote"]["TRY"]["price"]) * 0.035274
            try_dict[currency] = asset_dict[currency] * price
    return try_dict


# This function creates a daily table if its not already there,
# The excel table which is the output of that function contains the information
# of all the currencies in the assets table, how much they were worth in different
# currencies

def create_daily_table(usd_assets, try_assets):
    daily_table = pd.DataFrame(assets)
    daily_table["USD"] = usd_assets.values()
    daily_table["TRY"] = try_assets.values()

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    file_name = f"asset_outputs/assets-{day}-{month}-{year}.xlsx"

    if path.exists(file_name):
        print("Create daily table procedure already ran today.")
    else:
        daily_table.to_excel(
            f"asset_outputs/assets-{day}-{month}-{year}.xlsx", index=False)
    return()


# This function adds a row at the bottom of the history.xlsx file,
# recording the wealth information on that particular date.
def update_total_assets_table(total_usd_assets, total_try_assets):
    total_assets_table = pd.read_excel("history.xlsx",)
    total_assets_table["DATE"] = pd.to_datetime(total_assets_table["DATE"])
    date = total_assets_table.iloc[-1]["DATE"]
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    try:
        total_assets_table = total_assets_table.drop(["Unnamed: 0"], axis=1)
    except:
        pass

    print(total_assets_table)
    if (date.year != year or date.month != month or date.day != day):
        df1 = pd.DataFrame()
        df1["DATE"] = [datetime.datetime.now().date()]
        df1["DATE"] = pd.to_datetime(df1["DATE"])
        df1["TRY"] = [total_try_assets]
        df1["USD"] = [total_usd_assets]
        total_assets_table = total_assets_table.append(df1, ignore_index=True)
        total_assets_table.to_excel("history.xlsx", index=False)
        print(total_assets_table)
    else:
        print("Procedure has already run today.")

############################################################################
############################## MAIN BLOCK ##################################
############################################################################
assets = pd.read_excel("assets.xlsx")
usd_assets = get_dollar_assets(assets)
total_usd_assets = sum(usd_assets.values())

try_assets = get_try_assets(assets)
total_try_assets = sum(try_assets.values())

create_daily_table(usd_assets, try_assets)
update_total_assets_table(total_usd_assets, total_try_assets)
