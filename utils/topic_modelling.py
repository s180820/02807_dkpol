from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
from utils.data import STOPWORDS

class LSA:
    def __init__(self, docs,
        n_topics = 9, # number of topics
        **vectorizer_kwargs
    ):
        self.docs = docs
        self.org_vocab = list(set([d for doc in docs for d in doc.split()]))
        self.n_topics = n_topics
        self.vectorizer_kwargs = vectorizer_kwargs

        # create model and topics
        self.create_vectorizer()
        self.create_X()
        self.create_model()
        self.create_topics()


    def create_vectorizer(self):
        # create tfidf vectorizer
        max_df = self.vectorizer_kwargs.pop("max_df", 0.2) # ignore terms with larger than 0.2 as this likely a stopword
        self.vectorizer = TfidfVectorizer(stop_words=STOPWORDS, max_df=max_df, **self.vectorizer_kwargs)
    
    def create_X(self):
        # create data
        self.X = self.vectorizer.fit_transform(self.docs)
        self.terms = self.vectorizer.get_feature_names()

        # print some stats
        print("Number of documents: ", self.X.shape[0])
        print("Number of stopwords removed: ", len(self.org_vocab) - self.X.shape[1])
        print("Number of words in new corpus: ", self.X.shape[1])
        print("Percentage of non-zero elements: ", (self.X.toarray() != 0).sum()/(self.X.shape[0]*self.X.shape[1])*100, "%")

    def create_model(self):
        self.svd_model = TruncatedSVD(n_components=self.n_topics, algorithm='randomized', n_iter=100, random_state=122)
        self.svd_model.fit(self.X)

    def create_topics(self):#, n_words = 10)
        self.topics = {}
        self.topic_component = {}
        self.sorted_terms = {}
        for i, comp in enumerate(self.svd_model.components_): # components = right singular vectors (term-topic matrix)
            terms_comp = zip(self.terms, comp)
            sorted_terms = sorted(terms_comp, key= lambda x:x[1], reverse=True)#[:10] # use 10 most important words for each topic
            # self.topics[i] = [t[0] for t in sorted_terms]
            # self.topic_component[i] = [t[1] for t in sorted_terms]
            self.sorted_terms[i] = dict(sorted_terms)
            self.topics[i], self.topic_component[i] = zip(*self.sorted_terms[i].items())
        # print("Topic "+str(i)+": ")
        # print([t[0] for t in sorted_terms[:10]])

    def describe_topics(self, n_words = 10):
        return {topic : self.topics[topic][:n_words] for topic in self.topics}

    def visualize_topics(self, ncols = 3, n_topics = None, figsize = None):
        n_topics = self.n_topics if n_topics is None else n_topics

        nrows = self.svd_model.n_components//ncols
        figsize = (3*ncols, 3*nrows) if figsize is None else figsize
        fig, axes = plt.subplots(nrows, ncols, figsize = figsize)

        for i, topic in enumerate(list(self.topics.keys())[:n_topics]):
            wc = WordCloud(
                # max_font_size=50, 
                # max_words=100, 
                background_color="white",
                width = 1000,
                height = 800,
            ).generate_from_frequencies(self.sorted_terms[topic])
            ax = axes[i//ncols, i%ncols] #if n_topics == n_topics%nrows else axes[i]# visualize by row
            ax.imshow(wc)
            ax.set_axis_off()
            ax.set_title(f"Topic {topic}")
        plt.show()

    def visualize_topic_importance(figsize = (7.5, 5)):
        fig, ax = plt.subplots(1,1,figsize = figsize)

        ax.bar(range(self.svd_model.n_components), self.svd_model.singular_values_)
        ax.set_title("Singular values")
        ax.set_xlabel("Latent component (topic)")
        ax.set_ylabel("Importance of topic")

        plt.show()