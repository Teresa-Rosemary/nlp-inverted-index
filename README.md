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

Specify the following paths: - 
1. Input path of documents
	Line #92: 'C:\SparkChallenge\Dataset\*'
2. Output path to generate word dictionary
	Line #112: 'C:\SparkChallenge\Output\Dictionary\*'

```Py Spark
build_dictionary.py
```

Program to build the inverted index.

Specify the below path: - 
Output path to generate word dictionary
	Line #6: 'C:\SparkChallenge\Output\InvertedIndex\*'

```Py Spark
build_inverted_index.py
```

## Test
