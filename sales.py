# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 17:01:02 2021

@author: Charlie
"""
import requests
import pandas as pd
import datetime
import eth_prices
pd.set_option('display.max_rows', None, 
              'display.max_columns', None, 
              'display.width', None)

URL = "https://api.opensea.io/api/v1/assets"
URL2 = "https://api.opensea.io/api/v1/events"
data_dir = "C:\\Users\Charlie\Documents\School\\"


def get_last_sales(collection = "rob-gronkowski-championship-series-nfts"):
    nft = []
    completed = True
    offset = 0
    
    while (completed):
        querystring = {"order_by": "sale_price",
                        "order_direction": "desc",
                        "offset": offset,
                        "limit": "50",
                        "collection": collection}
         
        response = requests.request("GET", URL, params = querystring)
        response_json = response.json()
        
        asset = response_json["assets"]
        
        for i in range(0, len(asset)):
            y = int(asset[i]["last_sale"]["total_price"])/(10**18)
            y = round(y, 2)
            # print(y)
            asset[i]["total_price"] = y
        
        df = pd.DataFrame(asset)[["name", "total_price"]]
        nft.append(df)
        
        offset = offset + 50
        
        if len(asset) < 50:
            completed = False
    
    if(len(nft) == 1):
        nft = nft[0]
    else:
        nft = pd.concat(nft)    
    return nft

        

def get_historical_sales(slug = ""):
    nft = []
    completed = True
    offset = 0
    while (completed):
        querystring = {"collection_slug": slug,
                       "event_type":"successful",
                       "only_opensea":"false",
                       "offset": offset,
                       "limit":"100"}
        
        headers = {"Accept": "application/json"}
        
        response = requests.request("GET", URL2, headers=headers, params=querystring)
        response_json = response.json()
        asset = response_json["asset_events"]
        for i in range(0, len(asset)):
            
            # print (offset, i)
            asset[i]["total_price"] = round((int(asset[i]["total_price"])/10**18), 2)
            try:
                x = asset[i]["asset"]["name"]
            except TypeError:
                x = asset[i]["asset_bundle"]["assets"][0]["name"]
            y = asset[i]["transaction"]["timestamp"]
            z = round(float(asset[i]["payment_token"]["usd_price"]), 2)
            
            asset[i]["name"] = x
            asset[i]["timestamp"] = y
            asset[i]["curr_eth_price"] = z
        
        df = pd.DataFrame(asset)[["name", "timestamp", "total_price", "curr_eth_price"]]
        nft.append(df)
        
        offset = offset + 100
        
        if len(asset) < 100:
            completed = False
    
    nft = pd.concat(nft)
    return nft    

def sales_summary(slug = ""):
    # nft =  get_last_sales()
    # today_price = eth_prices.get_today_price()
    # earliest_price = round(float(eth_prices.get_historical_price("14-3-2021")), 2)
    
    # nft.to_csv(data_dir + "Gronk_{}.csv".format(datetime.date.today()), index = False)
    
    nft_historical = get_historical_sales(slug) 
    
    nft_historical.sort_values(['name', 'timestamp'], inplace =True)  
     
    summary = nft_historical.groupby(["name"]).apply(lambda x: pd.Series(
                        {"price_first" : x['total_price'].iloc[0], 
                          "price_last" : x['total_price'].iloc[-1],
                          "Time_first": x["timestamp"].iloc[0],
                          "Times_last": x["timestamp"].iloc[-1],
                          "Num_of_Sales" : len(x)})).reset_index()


# summary = summary[summary["Num_of_Sales"] > 1]         *gets rid of nfts that have been sold once*
    # summary.loc[:,"ETH_Current_Price"] = today_price
    # summary.loc[:, "ETH_Price_at_First_Sale"] = earliest_price
    
    return summary

def earliest_sale_sum(summary):
    df = summary["price_first"].sum()
    return df

def current_sale_sum(summary ):
    df = summary["price_last"].sum()
    return df
    

def data_to_csv(df = ""):
    df.to_csv(data_dir + "Gronk Historical.csv")



    

