from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "sentiment_analysis"

def get_sentiment_label(score):
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    else:
        return "neutral"

def analyze_sentiment():
    print("Running sentiment analysis with VADER...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    clean_collection = db['tweets_clean']
    analyzed_collection = db['tweets_analyzed']

    analyzer = SentimentIntensityAnalyzer()
    to_insert = []

    for tweet in clean_collection.find():
        vs = analyzer.polarity_scores(tweet['text'])
        sentiment = get_sentiment_label(vs['compound'])
        analyzed_tweet = {
            'id': tweet['id'],
            'date': tweet['date'],
            'user': tweet['user'],
            'text': tweet['text'],
            'vader_compound': vs['compound'],
            'vader_pos': vs['pos'],
            'vader_neu': vs['neu'],
            'vader_neg': vs['neg'],
            'sentiment': sentiment
        }
        to_insert.append(analyzed_tweet)
    if to_insert:
        analyzed_collection.insert_many(to_insert)
        print(f"Inserted {len(to_insert)} analyzed tweets into MongoDB (tweets_analyzed).")
    else:
        print("No analyzed tweets to insert.")

if __name__ == "__main__":
    analyze_sentiment()
