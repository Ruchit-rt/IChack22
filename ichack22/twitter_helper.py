import json

def make_json(json_txt):
    return json.loads(json_txt)

def parse_trends(all_trends):
    trends = all_trends["trends"]
    names_and_tweets = []
    for tweet_dict in trends:
        if (tweet_dict["tweet_volume"] != None):
            names_and_tweets.append((tweet_dict["name"], tweet_dict["tweet_volume"]))
    return names_and_tweets