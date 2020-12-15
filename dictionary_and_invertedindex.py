# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 21:08:50 2020

@author: teresa
"""

# importing libraries
from pyspark.sql import SparkSession
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer,SnowballStemmer
from symspellpy import SymSpell, Verbosity
import pkg_resources
import unicodedata
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(dest="inpath", help="filepath of the input documents")
parser.add_argument(dest="dictpath", help="filepath of the output word dictionary")
parser.add_argument(dest="indexpath", help="filepath of the output inverted index")
args = parser.parse_args()
inpath = args.inpath + "/*"
dictpath = args.dictpath
indexpath = args.indexpath


spark = SparkSession.builder.appName('BuildDictionaryAndIndex').getOrCreate()
sc = spark.sparkContext

#stopwords for English language
stopword = stopwords.words('english')

def tokenize(text):
    """
    Description : 
    Parameters: text - Input text to be processed
    Returns: normalized_tokens -  list of normalized tokens

    """
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode("utf-8")    #https://godatadriven.com/blog/handling-encoding-issues-with-unicode-normalisation-in-python/
    #Normalisation Form Compatibility Decomposition

    text = text.lower()
    #Remove square brackets as it is mentioned in the documents that the spelling corrections are enclosed within square brackets
    cleansed1 = re.sub(r"[\[\]]",'',text)
    
    #Sustitute 's, email address, website address and html tags with a space
    #Substituted with space other than blank to avoid wrong concatenation between strings
    cleansed2 = re.sub(r"'s\b|\w+@\w+\.\w+|\w+://\S+|<[^<]+?>", ' ', cleansed1)
    
    #Substitute all unwanted special characters with a space
    cleansed3 = re.sub("[^A-Za-z' ]+", ' ', cleansed2)
    
    #Substitute apostrophe at beginning and end of words, roman numerals and onewords with a space
    cleansed4 = re.sub(r"(?<=\s)\'+(?=\w*)|(?<=\S)\'+(?=\s+)|(?<=\s)[ivxlcdm]+(?=\s)|(?<=\s)\w(?=\s)|^\w(?=\s)|(?<=\s)\w$", ' ', cleansed3)
    
    #Remove all the remaining apostrophe
    cleansed5 = re.sub(r"\'",'',cleansed4) 
    
    #Split the text into tokens
    words = list(set(cleansed5.split()))
    
    #Correction = [word.replace("'d","ed") if word[-2:] == "'d" else word for word in words]
    
    #Lemmatization using nltk WordNetLemmatizer
    # Create an instance WordnetLemmatizer which is used for lemmatizing words
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmatized = [wordnet_lemmatizer.lemmatize(word) for word in words]
    
    #Stemming using nltk SnowballStemmer
    # Create a new instance of a English language specific subclass of SnowballStemmer which is used for stemming the words
    snowball_stemmer = SnowballStemmer('english', ignore_stopwords=True)
    stemmed = [snowball_stemmer.stem(word) for word in lemmatized]
    
    #Spell correction using symspellpy
    # Build SymSpell tree which is used for spell correction
    sym_spell = SymSpell(max_dictionary_edit_distance=3, prefix_length=7)
    # Loading dictionary
    dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
    spell_corrected = []
    for word in stemmed:
        suggestions = sym_spell.lookup(word, Verbosity.CLOSEST,max_edit_distance=3, include_unknown=True)
        firstSuggestion  = suggestions[0].term
        spell_corrected.append(firstSuggestion) 
        
    #Removing stopwords using nltk stopwords
    normalized_tokens = [word for word in spell_corrected if word not in stopword]
        
    return normalized_tokens


def getFileName(x):
    """
    Function to extract the filename from the full file path
    """
    fields = x.split('/')
    filename = int(fields[-1])
    return filename

# Create the rdd from the dataset
lines = sc.wholeTextFiles(inpath,30)

# Flatten the values by splitting the text files into normalised tokens
flattenToWords = lines.flatMapValues(tokenize)

# Make the word as the key of the rdd by swaping the values of key and value 
# Extract only the document name(from the full filepath) 
# Group the document names for each word and sort the values
listDocNames = flattenToWords.map(lambda x: (x[1],x[0])).mapValues(getFileName).sortByKey().groupByKey().mapValues(list).mapValues(lambda x: sorted(x))

# Add unique id to the rdd using zipWithIndex 
# Make unique id the key of the pair RDD by swaping key and value
# Now the RDD contains unique wordId as the key and word & associated DocList as the value
wholeData = listDocNames.zipWithIndex().map(lambda x: (x[1],x[0]))

# Word and Unique Id RDD is created by selecting only the word from the values of wholeData RDD
# and swapping the key-value pairs
wordId = wholeData.mapValues(lambda x: x[0]).map(lambda x: (x[1],x[0]))
wordId.coalesce(1).map(lambda row: str(row[0]) + " "*(30-len(row[0])) + str(row[1])).saveAsTextFile(dictpath)
   
# inverted Index(wordId and associated DocList) RDD is created by selecting only the DocList from the values of wholeData RDD
invertedIndex = wholeData.mapValues(lambda x: x[1])
invertedIndex.coalesce(1).map(lambda row: str(row[0]) + "\t" + str(row[1])).saveAsTextFile(indexpath)
    
spark.stop()
        