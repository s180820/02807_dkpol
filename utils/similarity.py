from utils.initialization import *
from utils.similarity import *
from utils.recommendation_system import *
import pandas as pd
import mmh3

########### Hashing

def listhash(l,seed):
	val = 0
	for e in l:
		val = val ^ mmh3.hash(e, seed)
	return val 
    
def minhash(shingles_list, seed):
    """
    Input:
        - shingles_list (list of str): set of hashes
        - seed (int): seed for listhash function
    Return: minhash of given shingles
    """
    minhash_value = None
    for aShingle in shingles_list:
        hashcode = listhash([aShingle], seed)
        if minhash_value == None or hashcode < minhash_value:
            minhash_value = hashcode
    return minhash_value

def minhash2(shingles_list, k):
    """
    Input:
        - shingles_list (list of str): set of hashes
        - k (int): seed for listhash function
    Return: sequence of k minhashes
    """
    all_minhash = []
    for i in range(k):
        all_minhash.append(minhash(shingles_list, i))
    return all_minhash



########### Signatures
# k=300

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


# for every person, return the 3 people most similar to him/her
def most_similar_persons(similar_items, num_similar_persons=3):
    """
    Input:
        - similar_items (dict of tuple:str): dictionary of similar items
        - num_similar_persons (int): number of similar persons to return
    Return: dictionary of most similar persons
    """
    most_similar_persons = {}
    for key,value in similar_items.items():
        if key[0] not in most_similar_persons:
            most_similar_persons[key[0]] = [(key[1], value)]
        else:
            most_similar_persons[key[0]].append((key[1], value))
        if key[1] not in most_similar_persons:
            most_similar_persons[key[1]] = [(key[0], value)]
        else:
            most_similar_persons[key[1]].append((key[0], value))
    for key,value in most_similar_persons.items():
        most_similar_persons[key] = sorted(value, key=lambda x: x[1], reverse=True)[:num_similar_persons]
    return most_similar_persons


######## create similarity table


def create_sim_table(df, level, on):
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
    signature_dict = signature(df, dict_docs, num_hashes = 300, on_what = on)
    found_similar_items = similar(signature_dict)
    most_similar_items = sorted(found_similar_items.items(), key=lambda x: x[1], reverse=True)
    most_similar_persons_res = most_similar_persons(found_similar_items)

    # convert most_similar_persons_res to a datamframe for easier visualization
    most_similar_persons_df = pd.DataFrame.from_dict(most_similar_persons_res, orient='index')
    if level == 'name':
        most_similar_persons_df.columns = ['Most similar person 1', 'Most similar person 2', 'Most similar person 3']
    elif level == 'party':
        most_similar_persons_df.columns = ['Most similar party 1', 'Most similar party 2', 'Most similar party 3']
    return most_similar_persons_df


######## create jaccard similarity matrix
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


def jacc_sim_matrix(data):
    dict_docs,signature_dict = create_docs(data,'name','TFIDF_Words')
    n_partym = data.name.unique()
    partym_matrix = np.zeros((len(n_partym), len(n_partym)))
    for i, partm in enumerate(n_partym):
        for j, partm_next in enumerate(n_partym):
            #append to matrix 
            partym_matrix[i,j] = jaccard(data.name.iloc[i], data.name.iloc[j], signature_dict)
    jac_sim = pd.DataFrame(partym_matrix, columns=data.name, index=data.name)
    jac_sim.index.name = None
    return jac_sim