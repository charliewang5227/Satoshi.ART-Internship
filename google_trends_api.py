# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 11:35:21 2021

@author: Charlie
"""
from pytrends.request import TrendReq
import datetime

pytrends = TrendReq(hl = "en-US", tz = 360)

def get_interest_over_time(search = "", start_date = None, end_date = None):
        
    start = start_date.strftime("%Y-%m-%d")
    end = end_date.strftime("%Y-%m-%d")
    
    total_time = " ".join([start, end])
    
    pytrends.build_payload(kw_list = [search], timeframe = total_time)    
    df = pytrends.interest_over_time()
    
    interest_start = df[search].iloc[0]
    interest_end = df[search].iloc[-1]
    
    return interest_start, interest_end
    
def interest_over_time_change(search = "", start_date = None, end_date = None, scaler = 0.25):
    
    start_score, end_score = get_interest_over_time(search, start_date, end_date)
    
    percent_change = ((end_score - start_score) / start_score)
    scaled_change = percent_change * scaler
    return scaled_change
