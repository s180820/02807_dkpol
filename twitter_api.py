import requests
import json
import pandas as pd

search_url = "https://api.twitter.com/2/users/155584627/tweets?max_results=6&pagination_token=7140dibdnow9c7btw4232twnluqa1fddrkv35qibt8th1"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev','tweet.fields': 'author_id'}
query_params = { #'query': keyword,
                #'start_time': start_date,
                #'end_time': end_date,
                # 'max_results': 100,
                # 'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                # 'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                # 'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                # 'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                # 'next_token': {}
                
                }

def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {'AAAAAAAAAAAAAAAAAAAAAIJzOQEAAAAAFZS0RG%2Blcaga154yEHMq7F6VbDY%3DYWv6Zea0cyjaqFN1bCRGEAKeIvojewrRBZ9lcZjGQQj5TWQqpl'}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def main():
    json_response = connect_to_endpoint(search_url, query_params)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()


