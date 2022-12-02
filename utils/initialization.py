# IMPORTS
from IPython.display import display
import pandas as pd
import re
# import csv
import os
import numpy as np
# import io
# from tqdm import tqdm
# from heapq import nlargest 

from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import scipy.spatial.distance as ssd

# PLOTS
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# NLTK
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')

# OWN FUNCTIONS
from utils.data import *
from utils.similarity import *
from utils.clustering import *
from utils.topic_modelling import *
from utils.recommendation_system import *
# from utils.clean_data import STOPWORDS