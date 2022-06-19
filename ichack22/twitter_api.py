
import tweepy
import twitter.twitter_helper

WOEID_UK = 23424975

# assinging keys
consumer_key = "oV8E0NbW6CX6M2yemgO6lTZkI"
consumer_secret = "yU2KJVgKU4hbYJON8kHXwKyLRDswkQxVyMLddnI4uyP2dE9e3M"
access_token = "1489969023160881159-yVhDKCMZ5wxkHnj8wRHa0sIXKiZnJp"
access_token_secret = "25YuLpfCne9FVYyoiplHAXgPURIYnIi2nAz5rDFab3Nz3"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def main(country = 1):
    trends = api.get_place_trends(country)[0]
    parsed_trends = twitter.twitter_helper.parse_trends(trends)
    return parsed_trends

if __name__ == "__main__":
    print(main(23424975))