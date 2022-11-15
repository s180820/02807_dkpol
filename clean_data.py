import pandas as pd
import numpy as np
import nltk
from Data.twitter_ids import twitter_ids


STOPWORDS = nltk.corpus.stopwords.words('danish')
more_stopwords = ["http", "jeg", "dig", "vi", "gang", "dit", "kan", "de", "rt", "nåh"]
STOPWORDS.extend(more_stopwords)

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

