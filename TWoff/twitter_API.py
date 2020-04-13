"""Retrieve TWeets, embeddings, and persist in the database."""
import basilica
from .models import DB, Tweet, User
import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

# config TWEEPY 
# http://docs.tweepy.org/en/latest/getting_started.html

TWITTER_AUTH = tweepy.OAuthHandler(os.getenv('TWITTER_CONSUMER_KEY'),
                                   os.getenv('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'),
                              os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)


#  instantiate BASILICA connection obj
BASILICA = basilica.Connection(os.getenv('BASILICA_KEY')) 
