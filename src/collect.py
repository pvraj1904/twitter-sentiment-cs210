import pandas as pd
import os
from pymongo import MongoClient

import tweepy
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "sentiment_analysis"
HISTORICAL_CSV = "data/historical/sentiment140.csv"  # Update if your dataset is different

def collect_historical():
    print("Loading historical Kaggle dataset...")
    df = pd.read_csv(HISTORICAL_CSV, encoding='latin-1', header=None)
    df.columns = ['sentiment', 'id', 'date', 'query', 'user', 'text']
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db['tweets_raw']
    records = df[['id', 'date', 'user', 'text', 'sentiment']].to_dict(orient='records')
    collection.insert_many(records)
    print(f"Inserted {len(records)} tweets into MongoDB.")

def collect_stream():
    print("Collecting up to 100 live tweets using Twitter API (free access)...")
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        print("Twitter API credentials not found. Skipping live tweet collection.")
        return

    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    query = "python OR data OR AI OR sports"

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db['tweets_raw']

    tweet_count = 0
    for tweet in tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode='extended').items(100):
        data = {
            'id': tweet.id_str,
            'date': tweet.created_at,
            'user': tweet.user.screen_name,
            'text': tweet.full_text,
            'sentiment': None
        }
        collection.insert_one(data)
        tweet_count += 1

    print(f"Inserted {tweet_count} live tweets into MongoDB.")

if __name__ == "__main__":
    collect_historical()
    collect_stream()
