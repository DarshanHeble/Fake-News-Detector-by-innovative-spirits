import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm
import numpy 
from scipy.sparse import coo_matrix

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = nltk.WordNetLemmatizer()

# Tokenization, Normalization, Capitalization, Non-alphanumeric removal, Stemming-Lemmatization
def preprocess(string):
    # to lowercase, non-alphanumeric removal
    step1 = " ".join(re.findall(r'\w+', string, flags=re.UNICODE)).lower()
    step2 = [lemmatizer.lemmatize(t).lower() for t in nltk.word_tokenize(step1)]

    return step2

# Function for extracting word overlap
def extract_word_overlap(headlines, bodies):
    word_overlap = []
    for i, (headline, body) in tqdm(enumerate(zip(headlines, bodies))):
        preprocess_headline = preprocess(headline)
        preprocess_body = preprocess(body)
        
        # Length of common words b/w body and headline / Length of all the words of body & headline
        features = len(set(preprocess_headline).intersection(preprocess_body)) / float(len(set(preprocess_headline).union(preprocess_body)))
        word_overlap.append(features)
        
        # Convert the list to a sparse matrix (in order to concatenate the cos sim with other features)
        word_overlap_sparse = coo_matrix(numpy.array(word_overlap)) 
    return word_overlap_sparse

# Function for extracting the cosine similarity between bodies and headlines. 
def extract_cosine_similarity(headlines, bodies):
    vectorizer = TfidfVectorizer(ngram_range=(1,2), lowercase=True, stop_words='english')#, max_features=1024)
    
    cos_sim_features = []
    for i in range(0, len(bodies)):
        body_vs_headline = []
        body_vs_headline.append(bodies[i])
        body_vs_headline.append(headlines[i])
        tfidf = vectorizer.fit_transform(body_vs_headline)
        
        cosine_similarity = (tfidf * tfidf.T).toarray()
        cos_sim_features.append(cosine_similarity[0][1])

    # Convert the list to a sparse matrix (in order to concatenate the cos sim with other features)
    cos_sim_array = coo_matrix(numpy.array(cos_sim_features)) 

    return cos_sim_array

# Function for combining features of various types (lists, coo_matrix, np.array etc.)
def combine_features(tfidf_vectors, cosine_similarity, word_overlap):
    combined_features =  sparse.bmat([[tfidf_vectors, word_overlap.T, cosine_similarity.T]])
    return combined_features