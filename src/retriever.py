import os
import json
import numpy as np
from collections import defaultdict
from nltk.stem import SnowballStemmer
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

stemmer = SnowballStemmer("french")

# Function to preprocess the query (normalize and remove stop words)
def preprocess_query(query):

    query = query.lower()  # Convert to lowercase

    #retenir que les lettres alphabetiques en francais et supprimer les chiffres et les espaces supplementaires
    query = re.sub(r"[^\w\sàâäéèêëîïôöùûüç]",' ',query)
    query = re.sub(r"\d",' ',query)
    query = re.sub(r"\s+",' ', query)

    query_words = query.split()  # Split into words

    #supprimer les stopwords francais comme : de, le, la, un ....
    query_words = list(filter(lambda token: token not in stopwords.words('french'),query_words))

    #radicalisation des mots 
    query_words = [stemmer.stem(word) for word in query_words ]
    # print(f"query_words : {query_words}")

    return query_words


# Function to load index files from a directory
def load_index_files(index_dir,query_words):
    prefixes_to_load = {word[:2] for word in query_words}  # Get the first two characters of each word in the query
    index_data = defaultdict(dict)  # Index data structure: {prefix: {word: [(doc_id, freq)]}}
    
    for filename in os.listdir(index_dir):
        if filename.endswith(".json"):
            prefix = filename.split('.')[0]  # Use the file name as the prefix (e.g., 'a.json' -> 'a')
            if prefix in prefixes_to_load:
                file_path = os.path.join(index_dir, filename)
            
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    print(f"Loaded data from {file_path}: {data}")  # Debug
                    index_data[prefix] = data  # Store the word frequency data under the prefix
    print(f"[INDEX_DATA] {index_data}\n")
    return index_data

# Function to build the query vector using the index base
def build_query_vector(query_words, index_base):
    query_vector = defaultdict(float)
    query_length = len(query_words)
    
    for word in query_words:
        query_vector[word] += 1 / query_length  # Normalized frequency

    print("Query Vector:", query_vector)  # Debug
    return query_vector

# Function to build document vectors (based on the index base)
def build_document_vectors(index_base):
    doc_vectors = defaultdict(lambda: defaultdict(float))  # Document ID -> {word: normalized frequency}
    
    for prefix in index_base:
        for word in index_base[prefix]:
            for doc_id, freq in index_base[prefix][word]:
                doc_vectors[doc_id][word] += freq  # Sum frequencies (if split across prefixes)
    
    # Normalize term frequencies by document length
    for doc_id, terms in doc_vectors.items():
        doc_length = sum(terms.values())  # Total terms in the document
        for word in terms:
            terms[word] /= doc_length  # Normalize frequency

    return doc_vectors

# Function to calculate cosine similarity between two vectors (Fonction du matching)
def cosine_similarity(vec1, vec2):
    common_terms = set(vec1.keys()).intersection(set(vec2.keys()))
    if not common_terms:
        return 0.0  # No common terms, similarity is 0
    
    dot_product = sum([vec1[term] * vec2[term] for term in common_terms])
    norm1 = np.sqrt(sum([vec1[term]**2 for term in vec1]))
    norm2 = np.sqrt(sum([vec2[term]**2 for term in vec2]))
    
    if norm1 == 0 or norm2 == 0:
        return 0.0  # If either vector is zero, similarity is 0
    
    similarity = dot_product / (norm1 * norm2)
    print(f"\nVEC1 {vec1} ---- VEC2 {vec2} |||  {similarity}\n")
    return similarity

# Function to rank documents based on relevance to the query
def rank_documents(query, index_base):
    print("[**********RANKING**********]")
    query_words = preprocess_query(query)  # Preprocess the query
    query_vector = build_query_vector(query_words, index_base)  # Build query vector
    doc_vectors = build_document_vectors(index_base)  # Build document vectors
    print(f"[VECTORS]  words:{query_words} --|-- query:{query_vector} --|-- doc:{doc_vectors}")
    
    # Compute cosine similarity for each document
    similarities = []
    for doc_id, doc_vector in doc_vectors.items():
        sim = cosine_similarity(query_vector, doc_vector)  # Calculate cosine similarity
        if(sim != 0):
            similarities.append((doc_id, sim))  # Store document id and its similarity score
    
    # Sort documents by similarity score in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Return the list of document ids sorted by relevance (similarity score)
    ranked_docs = [doc_id for doc_id, _ in similarities]
    return ranked_docs

