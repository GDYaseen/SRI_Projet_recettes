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
    print(f"query_words : {query_words}")

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

    return index_data

# Function to build the query vector using the index base
def build_query_vector(query_words, index_base):
    query_vector = defaultdict(int)  # Store frequency of words in the query
    
    for word in query_words:
        prefix = word[:2]  # Use the first two characters to determine the prefix (e.g., 'ch' -> 'ch.json')
        
        if prefix in index_base:  # Only look at relevant prefix files
            if word in index_base[prefix]:
                for doc_id, freq in index_base[prefix][word]:
                    query_vector[doc_id] += freq  # Add frequency to the corresponding document
                    print(f"Word: {word}, Doc ID: {doc_id}, Frequency: {freq}")  # Debug
        else:
            print(f"[DEBUG] No matching prefix found for '{word}'")  # Debug: no matching prefix

    print("Query Vector:", query_vector)  # Debug
    return query_vector

# Function to build document vectors (based on the index base)
def build_document_vectors(index_base):
    doc_vectors = defaultdict(lambda: defaultdict(int))  # Document ID -> {word: frequency}
    
    for prefix in index_base:
        for word in index_base[prefix]:
            for doc_id, freq in index_base[prefix][word]:
                doc_vectors[doc_id][word] = freq

    return doc_vectors

# Function to calculate cosine similarity between two vectors
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
    return similarity

# Function to rank documents based on relevance to the query
def rank_documents(query, index_base):
    query_words = preprocess_query(query)  # Preprocess the query
    query_vector = build_query_vector(query_words, index_base)  # Build query vector
    
    doc_vectors = build_document_vectors(index_base)  # Build document vectors
    
    # Compute cosine similarity for each document
    similarities = []
    for doc_id, doc_vector in doc_vectors.items():
        sim = cosine_similarity(query_vector, doc_vector)  # Calculate cosine similarity
        similarities.append((doc_id, sim))  # Store document id and its similarity score
    
    # Sort documents by similarity score in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)
    
    # Return the list of document ids sorted by relevance (similarity score)
    ranked_docs = [doc_id for doc_id, _ in similarities]
    return ranked_docs

# Example usage (assuming the index base files are available)
if __name__ == "__main__":
    # Example query
    query = "poulet"
    query_words = preprocess_query(query)
    
    # Load the index files from the specified directories
    doc_index_dir = './indexes/doc_indexes'
    #img_index_dir = './indexes/img_indexes'
    #vid_index_dir = './indexes/vid_indexes'
    
    # Load the index data
    doc_index_base = load_index_files(doc_index_dir,query_words)
    #img_index_base = load_index_files(img_index_dir,query_words)
    #vid_index_base = load_index_files(vid_index_dir,query_words)
    
    # Combine all index data into a single base
    #index_base = {**doc_index_base, **img_index_base, **vid_index_base}
    index_base = {**doc_index_base}
    
    # Debug
    print("Combined Index Base:")
    for prefix, words in index_base.items():
        print(f"Prefix: {prefix}, Words: {words}")
        
    # Rank the documents based on relevance to the query
    ranked_docs = rank_documents(query, index_base)
    
    print("Ranked Documents by Relevance:", ranked_docs)
