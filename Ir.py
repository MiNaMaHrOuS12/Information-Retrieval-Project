import os
import re
from collections import defaultdict
from nltk.stem import PorterStemmer

# Function to read multiple files from a folder
def read_files_from_folder(folder_path):
    docs = {}
    for idx, file_name in enumerate(os.listdir(folder_path), start=1):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                docs[idx] = file.read()  # Use file index as document ID
    return docs


# Initialize the Porter Stemmer 
stemmer = PorterStemmer()


# Stopwords removal function
def remove_stopwords(tokens):
    stopwords = {'is','are','a','in','on','an','was','were','the','at','of','with','and','for','from','to','by'}
    return [word for word in tokens if word not in stopwords]


# Tokenization with stemming
def tokenize_with_stopwords_and_stemming(text):
    # Remove dashes and dots
    text = re.sub(r'[-\.]', '', text) 
    text = re.sub(r"'s\b", '', text)
    # Tokenize the text
    tokens = re.findall(r'\w+', text.lower()) 

    # Remove stopwords
    filtered_tokens = remove_stopwords(tokens)

    # Apply stemming
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]

    return stemmed_tokens



# Update index construction functions to use stemming
def build_inverted_index(docs):
    inverted_index = defaultdict(set) 
    for doc_id, text in docs.items():
        tokens = tokenize_with_stopwords_and_stemming(text)  # Updated function
        for token in tokens:
            inverted_index[token].add(doc_id)
    return inverted_index

def build_positional_index(docs):
    positional_index = defaultdict(list)
    for doc_id, text in docs.items():
        tokens = tokenize_with_stopwords_and_stemming(text)  # Updated function
        for position, token in enumerate(tokens):
            positional_index[token].append((doc_id, position))
    return positional_index


# Folder path containing multiple files
folder_path = r'C:\Users\Mina Mahros\Desktop\IR Files'  # Update with your folder path

# Read files and build document dictionary
docs = read_files_from_folder(folder_path)

# Build the indices
inverted_index = build_inverted_index(docs)
positional_index = build_positional_index(docs)

# Function to search and show positions of a word in each document
def search_with_positions(word, positional_index, docs):
    # Normalize and stem the word (to match positional index)
    normalized_word = tokenize_with_stopwords_and_stemming(word)[0]  # Single word query
    if normalized_word in positional_index:
        positions = positional_index[normalized_word]
        print(f"Word '{word}' found in:")
        for doc_id, position in positions:
            print(f"  Document {doc_id} at position {position}")
    else:
        print(f"Word '{word}' not found in any document.")


# Enhanced Query Processing with Additional Features

def analyze_sentence(sentence, positional_index):
    """
    Analyze a sentence and display the positional index for each term.
    """
    tokens = tokenize_with_stopwords_and_stemming(sentence)
    print("\nPositional Index for terms in the input sentence:")
    for token in tokens:
        if token in positional_index:
            print(f"'{token}': {positional_index[token]}")
        else:
            print(f"'{token}': Not found in any document.")


def boolean_retrieval_with_positions(query, positional_index, total_docs):
    """
    Perform Boolean retrieval with 'AND', 'OR', and 'NOT' operators.
    Includes positional indices for matched terms in the results.
    """
    query = query.lower()
    # Split the query into terms based on Boolean operators
    terms = re.split(r'\band\b|\bor\b|\bnot\b', query)
    terms = [term.strip() for term in terms]  # Clean up terms
    tokens_list = [tokenize_with_stopwords_and_stemming(term) for term in terms]

    # Map tokens to their corresponding document sets and positional indices
    doc_sets = []
    term_positions = defaultdict(lambda: defaultdict(list))  # {doc_id: {term: [positions]}}
    for tokens in tokens_list:
        term_docs = set()
        for token in tokens:
            if token in positional_index:
                for doc_id, pos in positional_index[token]:
                    term_docs.add(doc_id)
                    term_positions[doc_id][token].append(pos)
        doc_sets.append(term_docs)

    # Process Boolean operators
    operators = re.findall(r'\band\b|\bor\b|\bnot\b', query)
    result_set = doc_sets[0]  # Start with the first term's document set

    for op, term_docs in zip(operators, doc_sets[1:]):
        if op == "and":
            result_set &= term_docs  # Intersection
        elif op == "or":
            result_set |= term_docs  # Union
        elif op == "not":
            result_set -= term_docs  # Difference

    # Filter term positions to include only documents in the result set
    filtered_positions = {
        doc_id: {term: positions for term, positions in terms.items()}
        for doc_id, terms in term_positions.items()
        if doc_id in result_set
    }

    return result_set, filtered_positions



def display_results_with_positions(result_set, docs, term_positions):
    """
    Display matching documents and their positional indices for terms.
    """
    if not result_set:
        print("\nNo matching documents found.")
    else:
        print("\nMatching Documents and Positional Indices:")
        for doc_id in result_set:
            print(f"\nDocument {doc_id}: {docs[doc_id]}")
            if doc_id in term_positions:
                print("Positional Indices:")
                for term, positions in term_positions[doc_id].items():
                    positions_str = ", ".join(map(str, positions))
                    print(f"  Term '{term}' at positions: {positions_str}")

def process_query(query):
    """
    Process the query to determine if it includes Boolean operators and handle appropriately.
    """
    query = query.strip().lower()  # Remove leading/trailing spaces and convert to lowercase

    # Check for Boolean operators ('and', 'or', 'not') in the exact form
    if re.search(r'\b(and|or|not)\b', query):
        # If the query contains Boolean operators, return True (for Boolean retrieval)
        return True
    return False


if __name__ == "__main__":
    # Build indices
    docs = read_files_from_folder(folder_path)
    inverted_index = build_inverted_index(docs)
    positional_index = build_positional_index(docs)
    total_docs = set(docs.keys())

    # Query input loop
    while True:
        query = input("\nEnter your query (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break
        
        if process_query(query):
            matching_docs, term_positions = boolean_retrieval_with_positions(query, positional_index, total_docs)
            display_results_with_positions(matching_docs, docs, term_positions)
        elif len(query.split()) > 1:
            analyze_sentence(query, positional_index)
        else:
            search_with_positions(query, positional_index, docs)

