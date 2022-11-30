import pandas as pd
import numpy as np
import nltk
from Data.twitter_ids import twitter_ids
import re
import simplemma

STOPWORDS = nltk.corpus.stopwords.words('danish') # consider also removing enmglish stopwords
STOPWORDS.extend(nltk.corpus.stopwords.words('english'))
more_stopwords = ["http", "jeg", "dig", "vi", "gang", "dit", "kan", "de", "rt", "nåh", "så", "det", "tweets", "mig"]
STOPWORDS.extend(more_stopwords)
STOPWORDS.extend(["ste", "sto", "henholdsvis", "pga", "sep", "øh", "haha", "okay", "dfår", "att"]) # from wordclouds

def clean_tweet(tweet):
    # remove emojis
    tweet = remove_emoji(tweet)
    # remove underscore
    tweet = re.sub('_', '', tweet)
    #remove quotes
    tweet = tweet.replace('"','').replace("'", "")
    # Remove tags
    tweet = re.sub("@[A-Za-z0-9]+", " ", tweet)
    # Lowercase
    tweet = tweet.lower()
    # Remove URLs
    tweet = re.sub(r'http\S+', '', tweet)
    # Remove punctuation
    tweet = re.sub('[^\w\s]','', tweet)
    # Remove numbers
    tweet = re.sub('\d+', '', tweet)
    # remove new line
    tweet = tweet.replace('\n', '')
    # remove multiple spaces
    tweet = re.sub(' +', ' ', tweet)
    # Remove stopwords and endings on words 
    tweet = ' '.join([simplemma.lemmatize(word, lang='da') for word in tweet.split() if word not in (STOPWORDS)])
    # remove leading and trailing spaces
    tweet = tweet.strip()
    # remove empty rows
    tweet = tweet if tweet != '' else None


    return tweet


def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r' ', string)



def clean_data(df):
    # remove underscore
    df['tweets'] = df['tweets'].str.replace('_', '', regex = True)
    # Remove tags
    df['tweets'] = df['tweets'].str.replace("@[A-Za-z0-9]+", " ", regex = True)
    # Lowercase
    df['tweets'] = df['tweets'].str.lower()
    # Remove stopwords
    df['tweets'] = df['tweets'].apply(lambda x: ' '.join([word for word in x.split() if word not in (STOPWORDS)]))
    # Remove URLs
    df['tweets'] = df['tweets'].str.replace(r'http\S+', '', case=False , regex = True)
    # Remove punctuation
    df['tweets'] = df['tweets'].str.replace('[^\w\s]','', regex = True)
    # Remove numbers
    df['tweets'] = df['tweets'].str.replace('\d+', '', regex = True)
    # remove new line
    df['tweets'] = df['tweets'].str.replace('\n', '', regex = True)
    # remove multiple spaces
    df['tweets'] = df['tweets'].str.replace(' +', ' ', regex = True)
    # remove leading and trailing spaces
    df['tweets'] = df['tweets'].str.strip()
    # remove empty rows
    df = df[df['tweets'] != '']

    return df


def combine():
    
    rows = 0
    for party in twitter_ids:
        for person in twitter_ids[party]:
            rows += 1

    columns = ["Party","Person","Tweets"]
    df = pd.DataFrame(index = range(rows),columns = columns)

    row = 0
    for party in twitter_ids:
        for person in twitter_ids[party]:
            df_person = pd.read_csv(f'src/Data/{party}/{person}.csv')
            df_person = clean_data(df_person)
            tweets = [df_person["tweets"].iloc[i] for i in range(len(df_person["tweets"]))]
            df["Tweets"].iloc[row] = tweets
            df["Party"].iloc[row] = party
            df["Person"].iloc[row] = person
            row += 1

    df.to_csv('src/Data_cleaned/Giant.csv', index = False)

    return df



# combine()

# df = pd.read_csv('src/Data_cleaned/Giant.csv')

