# nlp-inverted-index
Implementing an inverted index of a large collection of documents

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
    
2. Build the inverted index that gives the words with the list of documents it appears in

## Installation

```console
# Pre-requisites
pip install psutil
pip install nltk
pip install symspellpy
```

## Usage
Program to build the dictionary.


Specify the input path of documents and the output path where word dictionary is stored
```
build_dictionary.py
```

Program to buid the inverted index.


```
build_inverted_index.py
```
