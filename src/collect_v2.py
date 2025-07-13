import os
import tweepy
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

BEARER_TOKEN = os.getenv('BEARER_TOKEN')
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "sentiment_analysis"

def collect_recent_tweets_v2(query="python OR AI OR data", max_results=1):
    if not BEARER_TOKEN:
        print("No Bearer Token found. Please set BEARER_TOKEN in your .env file.")
        return
    client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)
    response = client.search_recent_tweets(
        query=query,
        max_results=min(max_results, 100),  # v2 API: max 100 per request, even less for free tier!
        tweet_fields=["created_at", "author_id", "text", "lang"]
    )
    tweets = response.data or []
    print(f"Fetched {len(tweets)} tweets.")
    mongo = MongoClient(MONGO_URI)
    db = mongo[DB_NAME]
    collection = db['tweets_raw']
    for tweet in tweets:
        if tweet.lang == "en":
            data = {
                "id": tweet.id,
                "date": tweet.created_at,
                "user": tweet.author_id,
                "text": tweet.text,
                "sentiment": None
            }
            collection.insert_one(data)
    print("Inserted tweets into MongoDB (tweets_raw).")

if __name__ == "__main__":
    collect_recent_tweets_v2()
