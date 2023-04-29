import random
import tweepy
import time
import requests
import os
import json
import re

# Get your AI API key
API_KEY = os.environ["API_KEY"]
AI_ORG = os.environ["AI_ORG"]

# Get your Twitter API credentials from https://developer.twitter.com/
CONSUMER_KEY = os.environ["CONSUMER_KEY"]
CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]
# UNSPLASH_API_KEY = os.environ["UNSPLASH_API_KEY"]

SUBJECTS = os.environ["SUBJECTS"].split(",")
EXCLUDE = os.environ["EXCLUDE"].split(",")
LANGUAGE = os.environ["LANGUAGE"]

# Create an instance of the AI API
AI_URL = "https://api.openai.com/v1/chat/completions"
AI_HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "OpenAI-Organization": f"{AI_ORG}"
    }

# Create an instance of the Tweepy API
auth = tweepy.OAuth1UserHandler(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Define a function to get the trending topics
def get_trending_tweets(topic):
    try:
        tweets = api.search_tweets(q=topic, lang=LANGUAGE, result_type='popular', count=20)

        filtered_tweets = []
        # Filter tweets based on the keywords
        for tweet in tweets:
            # print("-------------------------")
            # print(f"### {tweet.user.screen_name}:")
            # print(f"{tweet.text}\n")
            # print("-------------------------")

            if not any(re.search(keyword, tweet.text, re.IGNORECASE) for keyword in EXCLUDE):
                filtered_tweets.append(tweet)

        # Check if there are any tweets left after filtering
        twlen = len(filtered_tweets)
        if twlen > 0:
            twused = random.randint(0, twlen - 1)
            tweet = filtered_tweets[twused]
            print("-------------------------")
            print(f"### {tweet.user.screen_name}:")
            print(f"{tweet.text}\n")
            print("-------------------------")
            return tweet.text
        else:
            print("No popular tweets found for this topic after filtering")
    except requests.exceptions.RequestException as e:
        print("No popular tweets found for this topic")
    return None

# Define a function to get AI tweet content
def ask_ai(tweet,topic):
    print(f"Ask AI = {tweet} or topic = {topic}")
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": f"Compose a tweet as a Crypto Tweeter in response to the following tweet: {tweet}. Make sure the response has a positive tone. Verify if the tweet seems like a scam, giveaway, or self-promotion. If that's the case, compose a tweet sharing knowledge about {topic} instead. Provide a response that can be directly copied and posted on Twitter without the 'Response:' prefix, formatted as a user tweet."}
        ],
        "max_tokens": 50,
        "temperature": 0.8
    }
    try:
        response = requests.post(
            AI_URL,
            headers=AI_HEADERS,
            data=json.dumps(data)
        )

        print(response)
        if response.status_code == 200:
            response_json = response.json()
            tweet = response_json["choices"][0]["message"]["content"]
            return tweet.strip()
        else:
            print("Error:", response.status_code)
            return None
    
    except requests.exceptions.RequestException as e:
        print("Cannot connect to AI")
        return None

# Define a function to write a tweet
def write_tweet(tweet,topic):
    tweet_content = ask_ai(tweet,topic).strip('"').strip('Response: ')
    print(f"Tweet = {tweet_content}")
    isNotContent = re.search("As an AI language model", tweet_content, re.IGNORECASE)
    if not(isNotContent):
        try:
            api.update_status(status=f"{tweet_content}")
            return True
        except requests.exceptions.RequestException as e:
            print("Cannot send tweet")
            time.sleep(60)
    return False

# Define a function to run the bot
def run_bot():
    # Sleep for a random amount of time between 30 and 60 minutes
    setidle = random.randint(30, 60) * 60
    for topic in SUBJECTS:
        print(f"#### Search for hot tweet in {topic}")
        # Get the trending topics
        tweet = get_trending_tweets(topic)
        # Write a tweet about the hashtag
        if tweet != None:
            if write_tweet(tweet,topic):
                print(f"Wait for {str(setidle)} secs before search other subject")
                print("===============================================================")
                time.sleep(setidle)

    print(f"Wait for {str(setidle)} secs to start new loop")
    print("###############################################################################")
    time.sleep(setidle)

# Run the bot forever
while True:
    run_bot()
