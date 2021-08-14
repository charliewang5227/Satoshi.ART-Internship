# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 19:09:53 2021

@author: Charlie
"""
import twitter_api as tw
import google_trends_api as google
import eth_prices as eth
import sales as s

import datetime

def get_projection(start_date = None, end_date = None):
    projected_price = 0
    original_price = 0
    google_search = "Rob Gronkowski"
    twitter_handle = "RobGronkowski"
    collection_name = "rob-gronkowski-championship-series-nfts"
    
    eth_price_percent = eth.get_price_change(start_date, end_date)
    social_score_percent = tw.social_score_change(twitter_handle, start_date, end_date)
    google_trends_percent = google.interest_over_time_change(google_search, start_date, end_date)
    
    percent_change = eth_price_percent + social_score_percent + google_trends_percent
    
        
    # original_price = s.earliest_sale_sum(collection_name)
    
    # if percent_change > 0:
    #     projected_price = original_price * (1 + percent_change)
    # else:
    #     projected_price = original_price * (1 - percent_change)
    
    # return float(projected_price)

    if percent_change > 0:
        projected_pct = (1 + percent_change)
    else:
        projected_pct = (1 - percent_change)
    
    return float(projected_pct)



# main function
def projection_comparison(collection_name = "rob-gronkowski-championship-series-nfts",
                            start_date = datetime.datetime(2021, 3, 14), 
                            end_date = datetime.datetime(2021, 8, 5)):
    
    eth_price = eth.get_historical_price(end_date)
    projected_pct = get_projection(start_date, end_date)
    sales = s.sales_summary(slug = collection_name)
    
    first_price = s.earliest_sale_sum(sales)
    projected_price = projected_pct * first_price    
    projected_usd = projected_price * eth_price
    
    real_price = s.current_sale_sum(sales)
    real_usd = real_price * eth_price

    return projected_price, projected_usd, real_price, real_usd

######
projected_price, projected_usd, real_price, real_usd = projection_comparison(
                            collection_name = "rob-gronkowski-championship-series-nfts",
                            start_date = datetime.datetime(2021, 3, 14), 
                            end_date = datetime.datetime(2021, 8, 5)
                            )
    
print("Projected Price(ETH): ", round(projected_price, 2) , "ETH")
print("Projected Price(USD): ", round(projected_usd, 2), "USD")
print("Real Price(ETH): ", round(real_price, 2), "ETH")
print("Real Price(USD): ",  round(real_usd, 2), "USD")

