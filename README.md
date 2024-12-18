# README: Information Retrieval Code

## Introduction
This project implements an **Information Retrieval (IR) System** in Python. It processes multiple text documents, builds **inverted** and **positional indices**, and allows the user to search for terms using:

- **Single-word queries**
- **Sentence queries**
- **Boolean queries** (e.g., "term1 AND term2")

The system acts as a **search engine** for a set of files, enabling users to search for specific inputs efficiently. It uses stemming, tokenization, and stopword removal to preprocess the text, ensuring efficient and accurate results.

---

## How to Run the Code

### 1. Prerequisites
Ensure you have Python installed on your system (version 3.6 or later).

Install the required libraries using the following command:

```bash
pip install nltk
```

### 2. Folder Setup
Create a folder containing text files to be processed. Each file should have textual content for the search operations.

Update the variable `folder_path` in the code with the path to your folder. For example:

```python
folder_path = r'C:\Users\Mina Mahrous\Desktop\IR Files'
```

### 3. Running the Code
Run the script in your terminal or Python IDE:

```bash
python <script_name>.py
```

The program will prompt you to enter queries. Type your query and press `Enter`.

To exit, type `exit` and press `Enter`.

---

## Functions and Their Usage

### 1. `read_files_from_folder(folder_path)`
Reads all text files in the specified folder and returns a dictionary where keys are document IDs and values are file contents.

- **Input:** Folder path
- **Output:** Dictionary of documents

### 2. `remove_stopwords(tokens)`
Removes common stopwords (e.g., "the", "is") from a list of tokens.

- **Input:** List of tokens
- **Output:** List of tokens without stopwords

### 3. `tokenize_with_stopwords_and_stemming(text)`
Tokenizes the text, removes stopwords, and stems each word.

- **Input:** Text string
- **Output:** List of processed tokens

### 4. `build_inverted_index(docs)`
Creates an inverted index that maps each token to the set of document IDs where it appears.

- **Input:** Dictionary of documents
- **Output:** Inverted index (dictionary with tokens as keys and sets of document IDs as values)

### 5. `build_positional_index(docs)`
Creates a positional index that maps each token to the list of its positions in all documents.

- **Input:** Dictionary of documents
- **Output:** Positional index (dictionary with tokens as keys and lists of (document ID, position) tuples as values)

### 6. `search_with_positions(word, positional_index, docs)`
Searches for a single word in the documents and displays its positions.

- **Input:** Word, positional index, document dictionary
- **Output:** Positions of the word in documents

### 7. `analyze_sentence(sentence, positional_index)`
Displays the positional index for each term in a sentence.

- **Input:** Sentence, positional index
- **Output:** Positional index of each term

### 8. `boolean_retrieval_with_positions(query, positional_index, total_docs)`
Processes Boolean queries (using `AND`, `OR`, `NOT`) and returns matching documents and positions.

- **Input:** Query string, positional index, total document set
- **Output:** Matching documents and term positions

### 9. `display_results_with_positions(result_set, docs, term_positions)`
Displays matching documents and their positional indices for terms.

- **Input:** Matching document IDs, document dictionary, term positions
- **Output:** Prints results

---

## Data Structures Used

1. **Dictionary (`dict`)**
   - Used for storing documents and their content.
   - Also used for inverted and positional indices.

2. **Default Dictionary (`defaultdict`)**
   - Provides default values for inverted and positional indices.

3. **Set (`set`)**
   - Used in the inverted index to store unique document IDs for each token.

4. **List (`list`)**
   - Stores token positions in the positional index.

5. **Tuple
   - Appends a tuple consisting of (doc_id, position) for each token.

---

## Programming Language Used
- **Python**

---

## Sample Inputs and Outputs

### Case 1: Single Word Query
**Input:** `football`

**Output:**
```
Word 'football' found in:
  Document 1 at position 5
  Document 2 at position 12
```

### Case 2: Sentence Query
**Input:** `machine learning models`

**Output:**
```
Positional Index for terms in the input sentence:
'machin': [(1, 4), (2, 7)]
'learn': [(1, 5), (3, 2)]
'model': [(1, 8), (2, 10)]
```

### Case 3: Boolean Query
**Input:** `football AND machine`

**Output:**
```
Matching Documents and Positional Indices:

Document 1: Content of Document 1
Positional Indices:
  Term 'football' at positions: 5
  Term 'machine' at positions: 8

Document 2: Content of Document 2
Positional Indices:
  Term 'football' at positions: 12
  Term 'machine' at positions: 15
```

---

## Additional Notes
1. The code automatically normalizes and stems user queries for matching.
2. The program handles both case-sensitive and insensitive queries.


