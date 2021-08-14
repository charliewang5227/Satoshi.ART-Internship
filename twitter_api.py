# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 10:31:37 2021

@author: Charlie
"""
import tweepy
import datetime


api_key = "1WQSTrzQ9xTrF1lKtGbgp1pIa"
secret_key = "6JlP9jWEnA3WaRHXa4uaywilT0RTOsi323bVQeTn9eQbSoRvfW"
access_token= "1407730823244271617-XJ4yFZNPECXyy5w6vNj6EGVgarGnUQ"
access_token_secret = "VZ6sciA7LNBEypdhLD7Lkrd5ZZZezM38cW7Aq6500HZbx"

auth = tweepy.OAuthHandler(api_key, secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_social_score(name = "", date = ""):
    
    # follower_count = user.followers_count
    
    endDate = date - datetime.timedelta(30)
    
    retweets = 0
    favorites= 0
    
    past_month_tweets = []
    
    pulledTweets = api.user_timeline(name)
    for tweet in pulledTweets:
        if tweet.created_at <= date and tweet.created_at >= endDate:
            try:
                tweet.retweeted_status
            except:
                past_month_tweets.append(tweet)
                retweets = retweets + tweet.retweet_count
                favorites = favorites + tweet.favorite_count
    maxid = pulledTweets[-1].id
    
    complete = False
    while(not complete):
        pulledTweets = api.user_timeline(name, max_id = maxid)
        for tweet in pulledTweets:
            if tweet.created_at < date and tweet.created_at > endDate:
                try:
                    tweet.retweeted_status
                except:
                    past_month_tweets.append(tweet)
                    retweets = retweets + tweet.retweet_count
                    favorites = favorites + tweet.favorite_count
        if len(pulledTweets) > 0:
            maxid = pulledTweets[-1].id
            complete = pulledTweets[-1].created_at < endDate
    
    return retweets + favorites
            
def social_score_change(name = "", start_date = "", end_date = "", scaler = 0.25):
    
    start_score = get_social_score(name , start_date)
    end_score = get_social_score(name, end_date)
    
    percent_change = ((end_score - start_score) / start_score)
    
    scaled_change = percent_change * scaler
    return scaled_change
