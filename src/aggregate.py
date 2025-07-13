from pymongo import MongoClient
import pandas as pd

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "sentiment_analysis"

def aggregate_data():
    print("Aggregating sentiment data for dashboard...")
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    analyzed_collection = db['tweets_analyzed']
    agg_collection = db['sentiment_agg']

    data = list(analyzed_collection.find())
    if not data:
        print("No analyzed tweets to aggregate.")
        return

    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['day'] = df['date'].dt.date

    agg = df.groupby(['day', 'sentiment']).size().unstack(fill_value=0).reset_index()
    agg_records = agg.to_dict(orient='records')

    agg_collection.delete_many({})
    # Fix: convert datetime.date to string for MongoDB
    for rec in agg_records:
        if 'day' in rec and not isinstance(rec['day'], str):
            rec['day'] = str(rec['day'])
    agg_collection.insert_many(agg_records)

    print(f"Inserted {len(agg_records)} aggregated sentiment records into MongoDB (sentiment_agg).")

if __name__ == "__main__":
    aggregate_data()
