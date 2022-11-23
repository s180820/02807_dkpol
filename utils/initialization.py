# IMPORTS
from IPython.display import display
import pandas as pd
# import requests
import re
# from urllib.request import urlopen
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
#from fa2 import ForceAtlas2
# from scipy import stats
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
# import io
from tqdm import tqdm
# from heapq import nlargest 
import seaborn as sns
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

# PLOT SETTINGS
sns.set()

# NLTK PACKAGES
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')

# OWN FUNCTIONS
from utils.clean_data import clean_tweet
from utils.clean_data import STOPWORDS