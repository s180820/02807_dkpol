import requests
import pandas as pd
import numpy as np
import time
import os

from Data.id_dict import twitter_ids

# Twitter authentication
bearer_token = "None of your business"

def search_url(user_id, max_results = 100, pagination_token = None): 
    """ API endpoint based on user """
    if pagination_token:
        return f"https://api.twitter.com/2/users/{user_id}/tweets?max_results={max_results}&pagination_token={pagination_token}"
    else:
        return f"https://api.twitter.com/2/users/{user_id}/tweets?max_results={max_results}"

def bearer_oauth(r):
    """Authentication header"""
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    """Call to API with json response"""
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_tweets(user_id, max_results = 100, pagination_token = None, query_params = {}):
    new_url = search_url(user_id, max_results, pagination_token)
    json_response = connect_to_endpoint(new_url, query_params)
    return json_response

def get_all_tweets(user_id, max_results = 100, pagination_token = None, query_params = {}):
    """Gets all publicly available tweets from a user based on the users id. 
    This is done iteratively by updating the pagination token given in the json response"""
    
    all_tweets = np.array([])

    while True:
        json_response = get_tweets(user_id, max_results, pagination_token, query_params)
        if 'next_token' in json_response['meta']:
            pagination_token = json_response['meta']['next_token']
        else:
            break
        try:
            text = [tweet['text'] for tweet in json_response['data']]
        except:
            print("error, potentially missed some tweets")
            break
        all_tweets = np.append(all_tweets, text)

    return all_tweets

def write_to_csv(party, name, max_results = 100, pagination_token = None, query_params = {}):
    """Create .csv file for a specific person with all tweets from that person"""
    user_id = twitter_ids[party][name]
    all_tweets = get_all_tweets(user_id, max_results, query_params)
    df = pd.DataFrame(all_tweets, columns = ['tweets'])
    column_name = name.replace(" ", "_")
    df.to_csv(f"src/Data/{party}/{column_name}.csv", index = False)

def create_folders(twitter_ids):
    """.csv's are saved here"""
    for party in twitter_ids:
        if not os.path.exists(f"Data/{party}"):
            os.makedirs(f"Data/{party}")

def get_all(twitter_ids):
    """Get all tweets for all people in the twitter_ids dictionary"""
    for party in twitter_ids:
        for name in twitter_ids[party]:
            write_to_csv(party, name, max_results = 100, pagination_token = None, query_params = {})
        time.sleep(10)

if __name__ == "__main__":
    create_folders(twitter_ids)
    get_all(twitter_ids)
