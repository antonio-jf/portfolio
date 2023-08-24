import nltk
import sys
import os
import string
import math
# Additional requirement
# nltk.download("stopwords")

FILE_MATCHES = 1
SENTENCE_MATCHES = 1
PUNCTUATION = string.punctuation
STOP_WORDS = nltk.corpus.stopwords.words("english")

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dir_path = os.path.split(directory)
    documents_to_load = os.listdir(dir_path[1])
    
    Contents = {}
    
    # Read documents from corpus and load them into memory
    for document in documents_to_load:
        with open(os.path.join(dir_path[1], document), encoding='utf-8') as Doc:
            Contents[document] = Doc.read()
        
    return Contents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokenized = []
    
    # Tokenize the sentence, omits stop_words and punctuation
    for word in nltk.tokenize.word_tokenize(document):
        if word in STOP_WORDS:
            continue
        if word in PUNCTUATION:
            continue
        word_copy = word
        # Remove puntuation
        for i in range(len(word)):
            if word[i] in PUNCTUATION:
                word_copy = word.replace(word[i], '')
                
        if len(word_copy) != 0:
           tokenized.append(word_copy.lower())
            
    return tokenized


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    n_documents = len(documents.keys())
    appears_in = {}
    idfs = {}
    
    for document in documents.keys():
        for word in documents[document]:
            # Check if word is already in dictionary
            if word in STOP_WORDS:
                continue
            
            if word in appears_in.keys():
                # Check if the document is accounted for already
                if document in appears_in[word]:
                    continue
                # Document is not in dictionary, add it to word's values
                appears_in[word].append(document)    
                continue
               
            # Word is not in dictionary
            appears_in[word] = [document]
            
    # Get idfs and add to dictionary
    for key, value in appears_in.items():
        idfs[key] = math.log(n_documents/len(value), math.e)
    
    return idfs    


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = {file: 0 for file in files}
    # Check if query word is in file and add tf-idf score
    for query_word in query:
        for file in files.keys():
            for file_word in files[file]:
                if query_word == file_word and query_word not in STOP_WORDS:
                    tf_idfs[file] += idfs[query_word]
    
    rankings = []
    for key, value in tf_idfs.items():
        rankings.append((key, value))
    
    # Sort list and return top n results, according to tf-idf
    rankings = sorted(rankings, key=lambda x: x[1], reverse=True)
    best_n = [file[0] for file in rankings[:n]]
    
    return best_n


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # Keeps track of the count of words in the sentence for query term density
    sentence_idfs = {sent: 
        {"idf": 0, "count": 0}
        for sent in sentences.keys()
    }
    
    # Iterate over every sentence
    for sentence in sentences.keys():
        # Iterate over every word in the query
        for query_word in query:
            if query_word in sentences[sentence]:
                for word in set(sentences[sentence]):
                    # Add idf score to dict and add counter
                    if word == query_word and word not in STOP_WORDS:
                        sentence_idfs[sentence]["idf"] += idfs[query_word]
                        sentence_idfs[sentence]["count"] += 1

    best = []

    # Iterates over dictionary and appends total idf and count
    for sentence in sentence_idfs.keys():
        idf = 0
        count = 0
        for key, val in sentence_idfs[sentence].items():
            if key == "idf":
                idf += val
            if key == "count":
                count += val
        best.append((sentence, idf, count/len(sentences[sentence])))
        
    # Sort sentences from best to worst
    # Handle sentences with same idf value
    best = sorted(best, key=lambda x: (x[1], x[2]), reverse=True)  
    # Returns top n sentences
    best = [b[0] for b in best[:n]]

    return best[:n]


if __name__ == "__main__":
    main()
