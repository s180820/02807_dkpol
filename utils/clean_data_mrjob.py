from mrjob.job import MRJob
from mrjob.step import MRStep
import nltk
import os
import re


STOPWORDS = nltk.corpus.stopwords.words('danish') # consider also removing enmglish stopwords
more_stopwords = ["http", "jeg", "dig", "vi", "gang", "dit", "kan", "de", "rt", "nåh"]
STOPWORDS.extend(more_stopwords)

def clean_tweet(tweet):
    # remove non text related data
    tweet_info = re.findall(r"\d*,\['\d*'\],\d*,", tweet)
    if tweet_info == []:
        return None
    tweet = tweet.replace(tweet_info[0], "")
    # remove underscore
    tweet = re.sub('_', '', tweet)
    # Remove tags
    tweet = re.sub("@[A-Za-z0-9]+", " ", tweet)
    # Lowercase
    tweet = tweet.lower()
    # Remove stopwords
    tweet = ' '.join([word for word in tweet.split() if word not in (STOPWORDS)])
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
    # remove leading and trailing spaces
    tweet = tweet.strip()
    # remove empty rows
    tweet = tweet if tweet != '' else None

    # tweet = tweet.replace("\u00e6", "æ")

    return tweet


class MRWordFrequencyCount(MRJob):
    def mapper(self, _, line):
        path = str(os.environ['map_input_file'])
        name = os.path.basename(path)
        name = re.sub('_\d.csv', '', name)
        for tweet in line.split("\n"):
            tweet = clean_tweet(tweet)
            if tweet is not None:
                yield name, [tweet]

    def reducer(self, key, values):
        yield key, sum(values, [])

if __name__ == '__main__':
    MRWordFrequencyCount.run()