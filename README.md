# SRI_Projet_recettes

## Indexation
Les index sont stockés dans le dossier `indexes` dans ce format pour chaque type de fichier :
```
./indexes
      /doc_indexes
          ap.json
          br.json
          ...
      /faiss_indexes
          index.faiss
          index.pkl
```
## Recherche
Le processus de recherche dans notre système est conçu pour rechercher et classer efficacement les fichiers en fonction de la requête d'un utilisateur. Voici une explication de chaque étape impliquée :

1. **Query Preprocessing Normalization:**  
La requête est convertie en minuscules pour assurer une correspondance insensible à la casse. Suppression des mots vides : Les mots communs (par exemple, "le", "est", "et") qui n'apportent pas de sens à la requête sont supprimés pour se concentrer sur les termes significatifs. Extraction de mots-clés : Les mots-clés résultants servent de base pour faire correspondre les fichiers dans la base d'index. Exemple : Pour la requête "Trouver des recettes au chocolat ou à la vanille", après prétraitement, les mots-clés deviennent :  `["find", "chocolate", "vanilla", "recipes"]`.

2. **Index Loading:**  
Le système identifie les deux premières lettres de chaque mot-clé (par exemple, `["fi", "ch", "va", "re"]`) et charge uniquement les fichiers d'index correspondants (tr.json, ch.json, va.json, re.json) depuis les dossiers d'index appropriés (doc_indexes, img_indexes, vid_indexes). Ce chargement sélectif améliore les performances en limitant l'accès aux fichiers nécessaires

3. **Vector Space Model:**  
Chaque fichier est représenté comme un vecteur où:
    + Les dimensions correspondent aux mots-clés de la requête.
    + Les valeurs sont les fréquences des mots-clés dans le fichier, telles qu'enregistrées dans l'index.
    + La requête est également représentée comme un vecteur, où chaque dimension correspond à la présence ou l'absence du mot-clé dans la requête.

4. **Relevancy Calculation:**  
    + Similarité cosinus : La similarité entre le vecteur de la requête et chaque vecteur de fichier est calculée en utilisant le cosinus de l'angle entre eux. Cela mesure à quel point le fichier correspond à la requête.
    + Score de pertinence : Les fichiers sont classés en fonction de leurs scores de similarité cosinus.

5. **Result Compilation:**  
Le système compile une liste d'identifiants de fichiers (documents, images ou vidéos) pertinents pour la requête.
La liste est triée par ordre décroissant de pertinence, les fichiers les plus pertinents apparaissant en premier.
Exemple
Pour la requête `"Find chocolate or vanilla recipes"`:
```python
    #Preprocessing:
    Keywords = ["find", "chocolate", "vanilla", "recipes"]  

    #Index Loading: 
    fi.json, ch.json, va.json, re.json.  
    
    #Relevancy Calculation: Each file's relevancy is computed based on how frequently the keywords appear in it. Result:
    
        ##The system might return 
        [15, 2, 27]
        ##indicating that files with IDs 15, 2, and 27 are most relevant, in that order.
```
