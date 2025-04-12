import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
import argparse
from datetime import datetime
from tqdm import tqdm
from transformers import pipeline

def load_transformer_model():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def analyze_sentiment(text, model=None):
    if model:
        result = model(text)[0]
        label = result["label"]
        if label == "POSITIVE":
            return "Positive", result["score"]
        elif label == "NEGATIVE":
            return "Negative", result["score"]
        else:
            return "Neutral", result["score"]
    else:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            return "Positive", polarity
        elif polarity < 0:
            return "Negative", polarity
        else:
            return "Neutral", polarity

def main():
    parser = argparse.ArgumentParser(description="Tweet Sentiment Analyzer")
    parser.add_argument("--query", type=str, required=True, help="Search term")
    parser.add_argument("--max", type=int, default=300, help="Max tweets (default: 300)")
    parser.add_argument("--transformer", action="store_true", help="Use HuggingFace transformer model")
    args = parser.parse_args()

    with open("bearer.txt", "r") as file:
        bearer_token = file.read().strip()

    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    model = load_transformer_model() if args.transformer else None
    print(f"🔍 Searching tweets for '{args.query}' using {'Transformers' if model else 'TextBlob'}...")

    data = {
        "timestamp": [],
        "tweet": [],
        "sentiment": [],
        "score": []
    }

    pos = neg = neu = 0

    paginator = tweepy.Paginator(
        client.search_recent_tweets,
        query=args.query + " -is:retweet lang:en",
        max_results=100,
        tweet_fields=["created_at"],
        limit=args.max // 100
    )

    for response in tqdm(paginator, desc="Fetching tweets"):
        if response.data:
            for tweet in response.data:
                text = tweet.text.strip()
                timestamp = tweet.created_at

                sentiment, score = analyze_sentiment(text, model)
                if sentiment == "Positive":
                    pos += 1
                elif sentiment == "Negative":
                    neg += 1
                else:
                    neu += 1

                data["timestamp"].append(timestamp)
                data["tweet"].append(text)
                data["sentiment"].append(sentiment)
                data["score"].append(score)

    df = pd.DataFrame(data)
    filename = f"sentiment_{args.query}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    print(f"\n📁 Saved to: {filename}")

    df["sentiment"].value_counts().plot(kind="bar", color=["green", "gray", "red"])
    plt.title(f"Sentiment Distribution for '{args.query}'")
    plt.ylabel("Count")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

    print(f"\nSummary: {pos} positive, {neg} negative, {neu} neutral")

if __name__ == "__main__":
    main()
