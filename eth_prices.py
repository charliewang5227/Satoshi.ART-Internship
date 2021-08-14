# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 13:47:02 2021

@author: Charlie
"""
from pycoingecko import CoinGeckoAPI
# import datetime
cg = CoinGeckoAPI()

def get_today_price():
    curr_price = cg.get_price(ids='ethereum', vs_currencies='usd')
    curr_price = curr_price["ethereum"]["usd"]
    return curr_price
    
    
def get_historical_price(sale_date):
    date_sold = sale_date.strftime("%d-%m-%Y")
    historical_price = cg.get_coin_history_by_id(id = "ethereum", date = date_sold, localization = "false")
    historical_price = historical_price["market_data"]["current_price"]["usd"]
    
    return historical_price

def get_price_change(start_date, end_date, scaler = 0.50):
    # start = start_date.strftime("%d-%m-%Y")
    # end = end_date.strftime("%d-%m-%Y")
    
    start_price = get_historical_price(start_date)
    end_price = get_historical_price(end_date)
    
    percent_change = ((end_price - start_price) / start_price)
    scaled_change = percent_change * scaler
    
    return scaled_change