# -*- coding: utf-8 -*-
"""Authenticate to Twitter using tokens from .nany configuration file"""
import tweepy
import sys
from twdb.configurator import twdbConfig

OAUTH_TOKEN = twdbConfig['OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = twdbConfig['OAUTH_TOKEN_SECRET']
CONSUMER_KEY = twdbConfig['CONSUMER_KEY']
CONSUMER_SECRET = twdbConfig['CONSUMER_SECRET']


def getTwitterApi(wait=False, notify=False):
    """
    Authenticate to Twitter
    returns: twitter_api
    """
    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=wait,
                         wait_on_rate_limit_notify=notify)
    except Exception as e:
        print("Failed to get Twitter api: %s", e.message)
        sys.exit(1)
    return api
