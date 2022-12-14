from mrjob.job import MRJob
from mrjob.step import MRStep
import nltk
import os
import re
from utils.clean_data import clean_tweet
# from mr3px.csvprotocol import CsvProtocol
# from mr3px.keyedjson import KeyedJsonProtocol
from mrjob.protocol import JSONProtocol, RawValueProtocol

STOPWORDS = nltk.corpus.stopwords.words('danish') # consider also removing enmglish stopwords
more_stopwords = ["http", "jeg", "dig", "vi", "gang", "dit", "kan", "de", "rt", "nåh"]
STOPWORDS.extend(more_stopwords)

def clean_tweet_mrjob(tweet):
    # remove non text related data
    tweet_info = re.findall(r"\d*,\['\d*'\],\d*,", tweet)
    if tweet_info != []:
        tweet = tweet.replace(tweet_info[0], "")
        # return None
    
    if tweet == ",edit_history_tweet_ids,id,text":
        return None

    tweet = clean_tweet(tweet)

    return tweet




class MRDataCleaner(MRJob):
    OUTPUT_PROTOCOL = RawValueProtocol  
    
    def mapper(self, _, line):
        path = str(os.environ['map_input_file'])
        name = os.path.basename(path)
        name = re.sub('_\d.csv', '', name)
        for tweet in line.split("\n"):
            tweet = clean_tweet_mrjob(tweet)
            if tweet is not None:
                yield name, [tweet]

    def reducer(self, key, values):
        
        # Serializing json
        # json_object = json.dumps({key:sum(values, [])}, indent=4)
        
        # Writing to sample.json
        # with open("sample.json", "w") as outfile:
        #     json.dump({0:0}, outfile)
        #     # outfile.write(json_object)
        # with open("sample.txt", "a") as file_object:
        #     # Append 'hello' at the end of file
        #     file_object.write(str({key: sum(values, [])}))

        # yield key, sum(values, [])
        yield None, str({key: sum(values, [])})

if __name__ == '__main__':
    MRDataCleaner.run()