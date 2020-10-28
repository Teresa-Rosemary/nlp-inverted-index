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
Program to build the dictionary.

```Py Spark
spark-submit build_dictionary.py --h
usage: build_dictionary.py [-h] inpath outpath

positional arguments:
  inpath      filepath of the input documents
  outpath     filepath of the output word dictionary

optional arguments:
  -h, --help  show this help message and exit
```

Program to build the inverted index.

```Py Spark
spark-submit build_inverted_index.py --h
usage: build_dictionary.py [-h] inpath outpath

positional arguments:
  inpath      filepath of the input documents
  outpath     filepath of the output word dictionary

optional arguments:
  -h, --help  show this help message and exit
```
