import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "sentiment_analysis"

# Load data from MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
agg = pd.DataFrame(list(db['sentiment_agg'].find()))
tweets = pd.DataFrame(list(db['tweets_analyzed'].find()))

# Preprocess dates
agg['day'] = pd.to_datetime(agg['day'])
tweets['date'] = pd.to_datetime(tweets['date'])

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")
min_date = tweets['date'].min().date()
max_date = tweets['date'].max().date()
date_range = st.sidebar.date_input("Date range", (min_date, max_date), min_value=min_date, max_value=max_date)
keyword = st.sidebar.text_input("Keyword or #hashtag", "")

# Apply filters
mask = (tweets['date'].dt.date >= date_range[0]) & (tweets['date'].dt.date <= date_range[1])
if keyword:
    mask = mask & tweets['text'].str.contains(keyword, case=False, na=False)
tweets_filt = tweets[mask]
agg_filt = agg[(agg['day'] >= pd.to_datetime(date_range[0])) & (agg['day'] <= pd.to_datetime(date_range[1]))]

st.title("Real-Time Twitter Sentiment Dashboard")

# --- SENTIMENT TREND CHART ---
st.subheader("Sentiment Trend Over Time")
if not agg_filt.empty:
    agg_long = agg_filt.melt(id_vars=['day'], value_vars=['positive', 'neutral', 'negative'],
                             var_name='Sentiment', value_name='Number of Tweets')
    fig = px.line(agg_long, x='day', y='Number of Tweets', color='Sentiment')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No data for selected filter.")

# --- SENTIMENT DISTRIBUTION (PIE) ---
st.subheader("Sentiment Distribution (Most Recent Day)")
if not tweets_filt.empty:
    most_recent_day = tweets_filt['date'].dt.date.max()
    recent_tweets = tweets_filt[tweets_filt['date'].dt.date == most_recent_day]
    pie = recent_tweets['sentiment'].value_counts().reset_index()
    pie.columns = ['Sentiment', 'Count']
    fig2 = px.pie(pie, values='Count', names='Sentiment')
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.write("No tweets for selected filter.")

# --- WORD CLOUD ---
st.subheader("Word Cloud (Most Recent Tweets)")
if not tweets_filt.empty:
    text = " ".join(tweets_filt['text'].dropna().values)
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
    plt.figure(figsize=(10, 4))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)
else:
    st.write("No text data for word cloud.")

# --- TOP USERS ---
st.subheader("Top Tweeting Users")
if not tweets_filt.empty:
    top_users = tweets_filt['user'].value_counts().head(10).reset_index()
    top_users.columns = ['User', 'Tweets']
    fig3 = px.bar(top_users, x='User', y='Tweets', color='Tweets')
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.write("No user data.")

# --- SAMPLE TWEETS TABLE ---
st.subheader("Sample Tweets")
if not tweets_filt.empty:
    st.dataframe(tweets_filt[['date', 'user', 'text', 'sentiment']].sort_values("date", ascending=False).head(20))
else:
    st.write("No tweets to show for filter.")

st.caption("Customize further as needed for your project report or demo.")
