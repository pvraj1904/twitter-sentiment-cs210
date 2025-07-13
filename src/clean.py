import re
from pymongo import MongoClient
from langdetect import detect, LangDetectException

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "sentiment_analysis"

def clean_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'[^\w\s.,!?]', '', text)
    text = text.strip()
    return text

def is_english(text):
    try:
        return detect(text) == 'en'
    except LangDetectException:
        return False

def clean_tweets(max_tweets=10000):  # Only process 10k for test
    print("Cleaning tweets from MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    raw_collection = db['tweets_raw']
    clean_collection = db['tweets_clean']

    cleaned = []
    for idx, tweet in enumerate(raw_collection.find()):
        if idx >= max_tweets:
            break
        text = clean_text(tweet['text'])
        if len(text) > 5 and is_english(text):
            cleaned_tweet = {
                'id': tweet['id'],
                'date': tweet['date'],
                'user': tweet['user'],
                'text': text,
                'sentiment': tweet.get('sentiment')
            }
            cleaned.append(cleaned_tweet)
        if (idx+1) % 1000 == 0:
            print(f"Processed {idx+1} tweets...")
    if cleaned:
        clean_collection.insert_many(cleaned)
        print(f"Inserted {len(cleaned)} cleaned tweets into MongoDB (tweets_clean).")
    else:
        print("No tweets cleaned/inserted.")

if __name__ == "__main__":
    clean_tweets()
