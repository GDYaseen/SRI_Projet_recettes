import os
from pypdf import PdfReader
import re
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.stem import SnowballStemmer
import json

path = "./data"
path_index_docs = "./indexes/doc_indexes"

path_filenames_list = []
for dirname,subfolder,filename in os.walk(path) :
    for file in filename :
        path_file = os.path.join(dirname,file)
        path_filenames_list.append(path_file)

stemmer = SnowballStemmer("french")
word_dict = defaultdict(dict)
for file in path_filenames_list :
    reader = PdfReader(file)
    metadata = reader.metadata
    indice_doc = metadata["/indice_doc"]
    print(indice_doc)
    print("*****************")
    page = reader.pages[0]
    content = page.extract_text()
    print(content)
    content = content.lower()
    print("*****************")
    clean_content = re.sub(r"[^\w\sàâäéèêëîïôöùûüç]",' ',content)
    clean_content = re.sub(r"\d",' ',clean_content)
    clean_content = re.sub(r"\s+",' ', clean_content)
    clean_content = re.sub(" o ",' ', clean_content)
    words = clean_content.split()
    print(words)
    print("*****************")
    clean_words = list(filter(lambda token: token not in stopwords.words('french'),words))
    print(clean_words)
    print("*****************")
    clean_words = [stemmer.stem(word) for word in clean_words ]
    print(clean_words)
    print("******************")
    # Construire le dictionnaire de mots avec fréquence et indice_doc
    word_count = defaultdict(int)
    for word in clean_words:
        word_count[word] += 1
    print(word_count)
    print("*****************")
    
    for word, freq in word_count.items():
        prefix = word[:2]  # Les deux premiers caractères du mot
        if word not in word_dict[prefix]:
            word_dict[prefix][word] = []
        word_dict[prefix][word].append([int(indice_doc), freq])
    
print(len(clean_words))
print(len(word_dict))
word_dict

# Écriture des fichiers JSON par préfixe
for prefix, words_data in word_dict.items():
    output_file = os.path.join(path_index_docs, f"{prefix}.json")
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(words_data, json_file, ensure_ascii=False, indent=4)

print("Les fichiers JSON ont été générés avec succès.")