import os
import json
import random

# Sample curated list of food-related words (you can expand this as needed)
food_related_words = [
    "apple", "banana", "orange", "grape", "carrot", "potato", "spinach", "lettuce", "cucumber", 
    "tomato", "onion", "garlic", "ginger", "pepper", "cinnamon", "clove", "turmeric", "oregano", 
    "basil", "rosemary", "thyme", "chicken", "beef", "pork", "fish", "salmon", "tuna", "shrimp", 
    "lobster", "steak", "bacon", "cheese", "milk", "butter", "cream", "yogurt", "bread", "pasta", 
    "rice", "noodles", "soup", "salad", "sandwich", "pizza", "burger", "fries", "chips", "pie", 
    "cake", "cookie", "ice cream", "chocolate", "coffee", "tea", "wine", "beer", "whiskey", "cocktail", 
    "smoothie", "juice", "soda", "water", "spaghetti", "lasagna", "sushi", "curry", "soup", "salsa", 
    "chili", "taco", "burrito", "pasta", "ramen", "dumplings", "samosa", "couscous", "paella", "tiramisu",
    "quiche", "frittata", "sorbet", "mousse", "pudding", "salmon", "risotto", "roast", "grill", "steamed", 
    "baked", "fried", "boiled", "sauteed", "stew", "braised", "stir-fried", "smoked"
]

# Function to generate mock index with only food-related words
def generate_index(file_type, words, num_docs=50, num_words=100):
    # Group words by their first two alphabetic letters
    word_dict = {}
    
    for word in words[:num_words]:  # Limit to num_words for the example
        # Only consider the first two alphabetic characters of the word
        prefix = word[:2].lower()
        
        # Skip words that don't have alphabetic characters in the first two positions
        if not prefix.isalpha():
            continue
        
        # Skip words that aren't in the curated food-related list
        if word not in food_related_words:
            continue
        
        # Skip words that don't start with the intended prefix
        if prefix not in word_dict:
            word_dict[prefix] = {}
        
        # Randomly assign document IDs with different frequencies
        doc_id = random.randint(1, num_docs)  # Document IDs between 1 and 50
        freq = random.randint(1, 10)  # Frequency between 1 and 10
        
        if word not in word_dict[prefix]:
            word_dict[prefix][word] = []
        
        # Add this word's document ID and frequency to the list
        word_dict[prefix][word].append([doc_id, freq])

    # Save each group as a JSON file only if it has entries
    for prefix, words_dict in word_dict.items():
        # Ensure the folder exists
        folder = f'{file_type}_indexes'
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        filename = f'{folder}/{prefix}.json'
        
        # Write the file only if there are actual entries
        with open(filename, 'w') as f:
            json.dump(words_dict, f, indent=4)

# Example list of real words (for now, we use the curated list of food-related words)
words = food_related_words

# Create directories for doc_indexes, img_indexes, and vid_indexes
base_dirs = ['doc_indexes', 'img_indexes', 'vid_indexes']
for dir in base_dirs:
    if not os.path.exists(dir):
        os.makedirs(dir)

# Generate mock indexes with real words related to food and multiple entries per word
generate_index('doc', words, num_docs=50, num_words=100)  # For document files
generate_index('img', words, num_docs=50, num_words=100)  # For image files
generate_index('vid', words, num_docs=50, num_words=100)  # For video files

print("Example indexes with food-related words and multiple document entries generated!")
