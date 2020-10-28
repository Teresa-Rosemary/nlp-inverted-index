# nlp-inverted-index
Implementing an inverted index of a large collection of documents.

## Description
Inverted index is build in two stages. <br>

1. Build a dictionary of normalized tokens through following processes : - <br>

    Correcting accented characters <br>
    Conversion of text to lower case <br>
    Different cleansing actions to drop emails, websites, html tags, digits, special characters, roman numerals etc. <br>
    Lemmatization <br>
    Stemming <br>
    Dropping stop words <br>
    Spell check <br>
    
2. Build the inverted index that gives the words with the list of documents it appears in.

## Installation

```console
# Install psutil
pip install psutil

# Install nltk
pip install nltk
# Download wordnet and stopwords through NLTK in python console:
import nltk
nltk.download('wordnet')
nltk.download('stopwords')

# Install symspellspy
pip install symspellpy
```

## Usage
Program to build the Dictionary of Words and Inverted Index.

```Py Spark
spark-submit dictionary_and_invertedindex.py -h
usage: dictionary_and_invertedindex.py [-h] inpath dictpath indexpath

positional arguments:
  inpath      filepath of the input documents
  dictpath    filepath of the output word dictionary
  indexpath   filepath of the output inverted index

optional arguments:
  -h, --help  show this help message and exit
```
Example: spark-submit dictionary_and_invertedindex.py C:\Spark\challenges-data-engineer\dataset C:\Spark\word_dictionary C:\Spark\inverted_index

## Output

```console
Output executed against the documents in the "datset" folder is available in below folders:-

Dictionary of words - "Word_Dictionary"
Inverted Index - "Inverted_Index"
```
