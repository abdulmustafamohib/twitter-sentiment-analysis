import tweepy
from textblob import TextBlob

with open("bearer.txt", "r") as file:
    bearer_token = file.read().strip()

client = tweepy.Client(bearer_token=bearer_token)

search_term = "stocks"
tweet_amount = 200

response = client.search_recent_tweets(query=search_term, max_results=100, tweet_fields=['lang'])

tweets = response.data

polarity = 0
positive = 0
negative = 0
neutral = 0

if tweets:
    for tweet in tweets:
        final_text = tweet.text.replace("RT", " ")
        if tweet.lang == "en":
            if final_text.startswith("@"):
                position = final_text.index(":")
                final_text = final_text[position+2:]
            if final_text.startswith("@"):
                position = final_text.index(" ")
                final_text = final_text[position+2:]
        analysis = TextBlob(final_text)
        tweet_polarity = analysis.sentiment.polarity
        if tweet_polarity > 0.00:
            positive += 1
        elif tweet_polarity < 0.00:
            negative += 1
        elif tweet_polarity == 0.00:
            neutral += 1
        polarity += tweet_polarity
        print(f"{final_text} → {tweet_polarity:.2f}")

    print(polarity)
    print(f"Amount of positive tweets: {positive}")
    print(f"Amount of negative tweets: {negative}")
    print(f"Amount of neutral tweets: {neutral}")

else:
    print("No tweets found.")

