# Third Party Imports
The code utilizes the following third-party libraries:

- `requests`: A library for making HTTP requests.
- `MongoClient` from `pymongo`: A MongoDB driver for Python.
- `re`: The built-in Python regular expression library.


# Function: extract_tweet_ids
This function extracts tweet IDs to use it later from a list of tweets URLs.
It uses a simple regex to identify the ID in the link and return a list of these IDs.

## Arguments
- `links` (list): A list of tweets URLs.

## Returns
- `list`: A list of tweet IDs extracted from the URLs.


# Function: fetch_tweet
This function fetches tweet data from the Twitter API using the provided tweet ID, which is the key to get the tweet data.
This function uses a guest token so you need to check on the token every time you use it or you can sign in with cookies file to avoid this problem.

## Arguments
- `id` (str): The ID of the tweet to fetch.

## Returns
- `dict`: A dictionary containing the fetched tweet data in JSON format.


# Function: extract_tweet_info
This function extracts information from the fetched tweet data to filter the needed data points.
If one of these data points is not availabe in the fetched data this function will replace it with None.

## Arguments
- `tweet_data` (dict): A dictionary containing nested JSON of tweet data fetched from the Twitter API.

## Returns
- `dict`: A dictionary containing filtered and organized tweet data.

# Function: search_by_id
Every tweet has a unique ID to identify it.
This function searches for a tweet by its ID in a MongoDB collection to make sure we don't already have this tweet.

## Arguments
- `database_name` (str): The name of the MongoDB database.
- `collection_name` (str): The name of the collection within the database.
- `id_to_search` (str): The ID of the tweet to search for.
- `atlas_connection_uri` (str): The connection URI for MongoDB Atlas.

## Returns
- `bool`: True if the tweet is found in the collection, False otherwise.

# Function: main
The main function of the script that orchestrates the data retrieval and storage process.

No arguments or return values.

#  how to run
- Install Python 3.10 or higher 
- Install the dependencies in the requirements.txt file attached using command 'pip install -r requirements.txt'
- make sure you use proper Guest-token or use cookies file to sign in
- Run the script 

# Tools 
This script uses MongoDB Atlas on cloud to store the data, database_name, collection_name, atlas_connection_uri

# Errors
None
