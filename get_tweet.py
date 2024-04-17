# THIRD PARTY IMPORTS
import requests
from pymongo import MongoClient
import re

def extract_tweet_ids(links):
    """
    Extracts tweet IDs from a list of Twitter URLs.

    Args:
    - links (list): A list of Twitter URLs.

    Returns:
    - list: A list of tweet IDs extracted from the URLs.
    """
    tweet_ids = []
    for link in links:
        # Extract tweet ID using regular expression
        tweet_id_match = re.search(r'/status/(\d+)', link)
        if tweet_id_match:
            tweet_ids.append(tweet_id_match.group(1))
    return tweet_ids

def fetch_tweet(id):
    """
    Fetches tweet data from Twitter API using the provided tweet ID.

    Args:
    - id (str): The ID of the tweet to fetch.

    Returns:
    - dict: A dictionary containing the fetched tweet data in JSON format.
    """
    cookies = {
        'guest_id_marketing': 'v1%3A170221258011488403',
        'guest_id_ads': 'v1%3A170221258011488403',
        'guest_id': 'v1%3A170221258011488403',
        'gt': '1776802263937286604',
        'external_referer': 'padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D',
        '_ga': 'GA1.2.883017831.1712457660',
        '_gid': 'GA1.2.512449431.1712457660',
        'personalization_id': '"v1_V4fMKQ+P3HAt453TcHS3RQ=="',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'content-type': 'application/json',
        # 'cookie': 'guest_id_marketing=v1%3A170221258011488403; guest_id_ads=v1%3A170221258011488403; guest_id=v1%3A170221258011488403; gt=1776802263937286604; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D; _ga=GA1.2.883017831.1712457660; _gid=GA1.2.512449431.1712457660; personalization_id="v1_V4fMKQ+P3HAt453TcHS3RQ=="',
        'origin': 'https://twitter.com',
        'referer': 'https://twitter.com/',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-client-transaction-id': 'fY4u4gV1OLHtaNDvqss2J6QkAFxqFh8Ph9vQS52J/nxq/gBENezPqSLhIYyF4rbulB3Zv3xtbgvLmojlC6X0wWI+mPEUfA',
        # we use guest token so it won't be valid for too mcuh 
        # we can avoid this by using cookies to sign in then we won't have this problem s
        'x-guest-token': '1777502914883301836',##
        'x-twitter-active-user': 'yes',
        'x-twitter-client-language': 'en',
    }

    params = {# Tweet ID is the key 
        'variables': f'{{"tweetId":"{id}","withCommunity":false,"includePromotedContent":false,"withVoice":false}}',
        'features': '{"creator_subscriptions_tweet_preview_api_enabled":true,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"rweb_tipjar_consumption_enabled":false,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_enhance_cards_enabled":false}',
        'fieldToggles': '{"withArticleRichContentState":true,"withArticlePlainText":false}',
    }

    response = requests.get(
        'https://api.twitter.com/graphql/7ieDirzd5dipfzjuv3VSmw/TweetResultByRestId',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    # Parse the JSON response
    tweet_data = response.json()
    return tweet_data

def extract_tweet_info(tweet_data):
    extracted_info = {}
    try:
        # Extracting required information
        extracted_info['tweet_id'] = tweet_data['data']['tweetResult']['result']['rest_id']
        extracted_info['user_id'] = tweet_data['data']['tweetResult']['result']['core']['user_results']['result']['rest_id']
        extracted_info['created_at'] = tweet_data['data']['tweetResult']['result']['core']['user_results']['result']['legacy']['created_at']
        extracted_info['name'] = tweet_data['data']['tweetResult']['result']['core']['user_results']['result']['legacy']['name']
        extracted_info['unique_user'] = tweet_data['data']['tweetResult']['result']['core']['user_results']['result']['legacy']['screen_name']
        extracted_info['tweet_text'] = tweet_data['data']['tweetResult']['result']['legacy']['full_text']
        extracted_info['favorite_count'] = tweet_data['data']['tweetResult']['result']['legacy']['favorite_count']
        extracted_info['lang'] = tweet_data['data']['tweetResult']['result']['legacy']['lang']
        extracted_info['quote_count'] = tweet_data['data']['tweetResult']['result']['legacy']['quote_count']
        extracted_info['reply_count'] = tweet_data['data']['tweetResult']['result']['legacy']['reply_count']
        extracted_info['retweet_count'] = tweet_data['data']['tweetResult']['result']['legacy']['retweet_count']
    except KeyError as e:
        print(f"KeyError: {e} not found. Setting default value.")
        # Setting default values for missing keys
        extracted_info['tweet_id'] = None
        extracted_info['user_id'] = None
        extracted_info['created_at'] = None
        extracted_info['name'] = None
        extracted_info['unique_user'] = None
        extracted_info['tweet_text'] = None
        extracted_info['favorite_count'] = None
        extracted_info['lang'] = None
        extracted_info['quote_count'] = None
        extracted_info['reply_count'] = None
        extracted_info['retweet_count'] = None

    return extracted_info

def search_by_id(database_name, collection_name, id_to_search, atlas_connection_uri):
    """
    Searches for a tweet by its ID in a MongoDB collection.

    Args:
    - database_name (str): The name of the MongoDB database.
    - collection_name (str): The name of the collection within the database.
    - id_to_search (str): The ID of the tweet to search for.
    - atlas_connection_uri (str): The connection URI for MongoDB Atlas.

    Returns:
    - bool: True if the tweet with the specified ID is found in the collection, False otherwise.
    """
    # Connect to MongoDB Atlas
    client = MongoClient(atlas_connection_uri)
    
    # Access the specified database
    db = client[database_name]
    
    # Access the specified collection
    collection = db[collection_name]
    
    # Search for the ID
    result = collection.find_one({"tweet_id": id_to_search})
    
    if result:
        return True
    else:
        return False



def main():
    # Create a list  to store all tweet dictionaries
    all_tweets_list = []
    # Provide your database name, collection name, ID to search, and Atlas connection string
    database_name = "tweets_DB"
    collection_name = "tweets"
    atlas_connection_uri = "mongodb+srv://username:password@cluster0.8m3ub4b.mongodb.net/?retryWrites=true&w=majority"
    # tweet URLs to scrape 
    urls = ['https://twitter.com/D_ghaith/status/1228753352940564480','https://twitter.com/iNajem76/status/867095897527734275',
            'https://twitter.com/Dana_hailam/status/1385711915905732613?lang=ar']
    #clean links
    id_list = extract_tweet_ids(urls)

    for i in id_list:
        res = search_by_id(database_name,collection_name,i,atlas_connection_uri)
        print(f"DO WE HAVE THIS TWEET? {res}")
        if res:
            pass 
        else:
            # get all Data
            tweet_data = fetch_tweet(i)
            # filter Data
            tweet_dict = extract_tweet_info(tweet_data)
            # organize all dicts
            all_tweets_list.append(tweet_dict)

    if all_tweets_list:
        # connect to Mongo DB Atlas
        client = MongoClient(atlas_connection_uri)
        db = client[database_name]
        collection = db[collection_name]
        # insert the data into the collection
        collection.insert_many(all_tweets_list)
    else:
        print("No new tweets to insert.")
                

if __name__ == "__main__":
    main()


    
    
