from utils.initialization import *
import pandas as pd
import mmh3
from utils.similarity import *

def signature(df, dict_docs, num_hashes, on_what):
    """
    Input:
        - dict_docs (dict of str:str): dictionary of {title:document}
        - q (int)
        - num_hashes (int)
    Return: dictionary consisting of document id’s as keys and signatures as values
    """
    dict_signatures = {}
    total_texts = len(list(dict_docs.keys()))
    counter = 1
    for key,text in dict_docs.items():
        # print(f'{counter}/{total_texts} - {key} - Processing...')
        doc_shingles = df[on_what][counter-1]
        minhash_values = minhash2(doc_shingles, num_hashes)
        dict_signatures[key] = minhash_values
        counter += 1
    return dict_signatures



def create_docs(df, level, on):
    if on == 'TFIDF_Words':
        vectorizer = TfidfVectorizer(max_df=0.5, max_features=700, stop_words='english')
        vectors = vectorizer.fit_transform(df.tokens.apply(lambda x: " ".join(x)))
        dict_of_tokens={i[1]:i[0] for i in vectorizer.vocabulary_.items()}
        tfidf_vectors = []  # all deoc vectors by tfidf
        for row in vectors:
            tfidf_vectors.append({dict_of_tokens[column]:value for (column,value) in zip(row.indices,row.data)})
        df['TFIDF_Words'] = [list(tfidf_vectors[i].keys()) for i in range(len(df))]
    elif on == 'tokens':
        pass
   
    dict_docs = {i:j for i,j in zip(df[level],df[on])}
    signature_dict = signature(df, dict_docs,  300, on)
    found_similar_items = similar(signature_dict)
    most_similar_items = sorted(found_similar_items.items(), key=lambda x: x[1], reverse=True)
    most_similar_persons_res = most_similar_persons(found_similar_items)
    return dict_docs,signature_dict

########## Jaccard
def jaccard(name1, name2, signature_dict):
    """
    Input:
        - name1 (str): key of the first document S
        - name2 (str): key of the second document T
        - signatures_dict (dict of str:list): dictionary of signatures
    Return: Jaccard similarity between S and T
    """
    signatures_doc1 = np.array(signature_dict[name1])
    signatures_doc2 = np.array(signature_dict[name2])
    return len(np.intersect1d(signatures_doc1, signatures_doc2))/len(np.union1d(signatures_doc1, signatures_doc2))#, np.setdiff1d(signatures_doc1, signatures_doc2)

def similar(signatures_dict, jaccard_threshold=0.001):
    """
    Input:
        - signatures_dict (dict of str:list): dictionary of signatures
        - jaccard_threshold (float): lower bound for Jaccard similarity score to consider
            two documents as similar
    Return: dictionary of similar items
    """
    list_keys = list(signatures_dict.keys())
    similar_items = {}
    for i in range (len(list_keys)-1):
        for j in range (i+1, len(list_keys)):
            similarity_score = jaccard(list_keys[i], list_keys[j], signatures_dict)
            if similarity_score >= jaccard_threshold:
                similar_items[(list_keys[i], list_keys[j])] = similarity_score
    return similar_items

b,r = 150, 2
# assert k == b*r

def lsh(signatures_dict, jaccard_threshold, seed=10):
    lsh_dict = {}
    for key, values in signatures_dict.items():
        blocks = np.split(np.array(values), b)
        blocks_hash_values = []
        for aBlock in blocks:
            blocks_hash_values.append(mmh3.hash(aBlock, seed))
        lsh_dict[key] = blocks_hash_values
    list_keys = list(lsh_dict.keys())
    similar_items = {}
    for i in range (len(list_keys)-1):
        for j in range (i+1, len(list_keys)):
            common_values = np.intersect1d(lsh_dict[list_keys[i]], lsh_dict[list_keys[j]])
            if len(common_values) > 0:
                # we found a candidate
                similarity_score = jaccard(list_keys[i], list_keys[j], signatures_dict)
                if similarity_score >= jaccard_threshold:
                    similar_items[(list_keys[i], list_keys[j])] = similarity_score
    return similar_items



def recommendation(similar_items, num_similar_persons=3, names = None, level= None, on= None):
    """
    Input:
        - similar_items (dict of tuple:str): dictionary of similar items
        - num_similar_persons (int): number of similar persons to return
        - names (list of str): list of names to include
    Return: dictionary of most similar persons
    """


    most_similar_persons = {}
    for key,value in similar_items.items():

        if key[0] in names:
            if key[1] not in names:
                if key[0] not in most_similar_persons:
                    most_similar_persons[key[0]] = [(key[1], value)]
                else:
                    most_similar_persons[key[0]].append((key[1], value))
        elif key[1] in names:
            if key[0] not in names:
                if key[1] not in most_similar_persons:
                    most_similar_persons[key[1]] =  [(key[0], value)]
                else:
                    most_similar_persons[key[1]].append((key[0], value))
    for key, value in most_similar_persons.items():
        # most_similar_persons[key] = value[:num_similar_persons]
        most_similar_persons[key] = sorted(value, key=lambda x: x[1], reverse=True)[:num_similar_persons]




    most_similar_persons = pd.DataFrame.from_dict(most_similar_persons, orient='index')
    if level == 'name':
        most_similar_persons.columns = ['Most similar person 1', 'Most similar person 2', 'Most similar person 3']
    elif level == 'party':
        most_similar_persons.columns = ['Most similar party 1', 'Most similar party 2', 'Most similar party 3']
    return most_similar_persons[most_similar_persons.index.isin(names)]



###### Visualisation
def barchart_recommendation(res):
    plt.rcParams['figure.figsize'] = [8, 6]
    plt.rcParams.update({'font.size': 12})
    res['Most similar person 3'] = res['Most similar person 3'].fillna(0)
    res['val1'] = res['Most similar person 1'].apply(lambda x: x[1] if x != 0 else 0)
    res['val2'] = res['Most similar person 2'].apply(lambda x: x[1] if x != 0 else 0)
    res['val3'] = res['Most similar person 3'].apply(lambda x: x[1] if x != 0 else 0)

    labels = ['Anders Bjarklev', 'Anders L. M.', 'DTU', 'Peter Mogensen', 'Selma Montgomery', 'Michael Kristiansen']
    men_means = res['val1']
    women_means = res['val2']
    third_means = res['val3']
    zeros = [0,0,0,0,0,0]

    x = np.arange(len(labels))  
    width = 0.25  

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2 - width, men_means, width, label='Men',color = ['blueviolet', 'magenta', 'dodgerblue', 'plum', 'pink', 'darkblue'])
    rects2 = ax.bar(x - width/2, women_means, width, label='Women', color = [ 'purple', 'dodgerblue','magenta', 'dodgerblue', 'purple','turquoise'])
    rects3 = ax.bar(x + width/2, third_means, width, label='thredje', color = [ 'coral', 'plum', 'purple', 'purple','red','blue'])

    legends = []
    colors = ['magenta', 'dodgerblue', 'plum', 'purple', 'blueviolet', 'turquoise', 'coral', 'red'  ,'blue'  , 'pink', 'darkblue']
    for i in range(len(colors)):
        legends.append(ax.bar(x, zeros, width, label='thredje', color = colors[i]))
    ax.set_ylabel('Jaccard similarity')
    ax.set_xticks(x, labels, rotation=-45)
    ax.legend([leg for leg in legends ], ('Monika Rubin', 'Henrik Dahl', 'Jakob Engel Schmidt','Martin Lidegaard', 'Katrine Robsøe','Ole Olesen',  'Jacob Mark',  'Pelle Dragsted','Peter Skaarup', 'Magnus Heunicke','Søren Espersen'))
    fig.tight_layout()
    return plt.show()



