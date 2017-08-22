#!//anaconda/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed May  3 09:09:49 2017

@author: nextwork
"""

from wordcloud import WordCloud
import re,os
#logging.basicConfig(format='%(asctime)s : %(Levelname)s: %(message)s', level=logging.INFO)
import numpy as np
import snowballstemmer
import glob
from PIL import Image
from nltk.corpus import stopwords
import gensim
import random
from wordcloud import (WordCloud, get_single_color_func)
import matplotlib.pyplot as plt



#==============================================================================

import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('utf-8')
#==============================================================================

#create corpus & dict

#==============================================================================

from gensim import corpora


def any2unicode(text, encoding='utf-8', errors='strict'):
    """Convert a string (bytestring in `encoding` or unicode), to unicode."""
    if isinstance(text, unicode):
        return text
    return unicode(text, encoding, errors=errors)
to_unicode = any2unicode



def raw_tokenize(text):
    text= to_unicode(text)
    text = text.lower()
    # tokenize + punctuation
    from nltk.tokenize import RegexpTokenizer
    tokenizer = RegexpTokenizer(r'\w+') # remove punctuation
    return tokenizer.tokenize(text)
	
def tokenize(text):
    text = raw_tokenize(text)
    # remove stopwords
    from nltk.corpus import stopwords
    stops = stopwords.words('danish') + stopwords.words('english')
    text = [ w.replace (" ", "_") for w in text if w.lower() not in stops]
    # Exclude numbers
    text = [s for s in text if not re.search(r'\d',s)]
    #remove word with less than 3letters
    text = [s for s in text if len(s) > 2]
    # stemmer (Den her har med lemmatizeren at gøre) 
    #lmtzr = snowballstemmer.DanishStemmer()
    #text =  lmtzr.stemWords(t for t in text)
    return text


#=
def iter_documents(top_directory):
    """Iterate over all documents, yielding a document (=list of utf8 tokens) at a time."""
    for root, dirs, files in os.walk(top_directory):
        for file in filter(lambda file: file.endswith('.txt'), files):
            document = open(os.path.join(root, file)).read() # read the entire document, as one big string
            doc_tokenized=tokenize(document) # or whatever tokenization suits you
            yield doc_tokenized
            
            
class MyCorpus(object):
    def __init__(self, top_dir):
        self.top_dir = top_dir
        self.dictionary = gensim.corpora.Dictionary(iter_documents(top_dir))
        #self.dictionary.filter_extremes(no_below=1, keep_n=30000) # check API docs for pruning params
        self.dictionary.save(path+'/dictionary.dict')

    def __iter__(self):
        for tokens in iter_documents(self.top_dir):
            yield self.dictionary.doc2bow(tokens)



#prompt input for path
prompt = '> '
print "Input file path." 
path = raw_input(prompt)


#uses code above to create tfidf corpus out of .csv files
def create_corpus(path):
    corpus = MyCorpus(path) # create a dictionary
    return gensim.corpora.MmCorpus.serialize(path+'/test.mm', corpus)
    
create_corpus(path)
print "corpus created !"

#==============================================================================


#creates weights for range of documents
all_weights= {}



def pairs(num):
    weights=[]
    for x in range(0,num):
        corpus=corpora.MmCorpus(path+'/test.mm')
        tfidf = gensim.models.TfidfModel(corpus)
        dictionary=corpora.Dictionary.load(path+'/dictionary.dict')
        weights=tfidf[corpus[x]]
        weights=[(dictionary[pair[0]], pair[1]) for pair in weights]
        weights=[n for n in weights if n[1] >= 0.005]
        all_weights[x]=weights
    return all_weights






print "How many documents do you have?"
pairs(int(raw_input(prompt)))
print len(all_weights)

from wordcloud import (WordCloud, get_single_color_func)
import matplotlib.pyplot as plt


class SimpleGroupedColorFunc(object):
    """Create a color function object which assigns EXACT colors
       to certain words based on the color to words mapping

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)

#==============================================================================

class GroupedColorFunc(object):
    """Create a color function object which assigns DIFFERENT SHADES of
       specified colors to certain words based on the color to words mapping.

       Uses wordcloud.get_single_color_func

       Parameters
       ----------
       color_to_words : dict(str -> list(str))
         A dictionary that maps a color to the list of words.

       default_color : str
         Color that will be assigned to a word that's not a member
         of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)


color_to_words = {
    # words below will be colored with a green single color function
    '#00ff00': ['beautiful', 'explicit', 'simple', 'sparse',
                'readability', 'rules', 'practicality',
                'explicitly', 'one', 'now', 'easy', 'obvious', 'better'],
    # will be colored with a red single color function
    'red': ['ugly', 'implicit', 'complex', 'complicated', 'nested',
            'dense', 'special', 'errors', 'silently', 'ambiguity',
            'guess', 'hard']
}

# Words that are not in any of the color_to_words values
# will be colored with a grey single color function


print "Which color would you like the wordcloud in?"
default_color = raw_input(prompt)

# Create a color function with single tone
# grouped_color_func = SimpleGroupedColorFunc(color_to_words, default_color)

# Create a color function with multiple tones
grouped_color_func = GroupedColorFunc(color_to_words, default_color)
#==============================================================================



def wordcloud_generator(dic):
    for key, item in dic.iteritems():
        mask=np.array(Image.open("/Users/nextwork/Desktop/JA/circle.png"))
        wc=WordCloud(
                    background_color="white",
                    max_words=2000,
                    width = 1024,
                    height = 720,
                    mask=mask,
                    )
        wc.generate_from_frequencies(item)
        wc.recolor(color_func=grouped_color_func, random_state=3)
        wc.to_file(path+"/"+str(key)+"word_cloud.png")


def flatten(dic):
    res = []  # Result list
    if isinstance(dic, dict):
        for key, val in dic.items():
            res.extend(flatten(val))
    elif isinstance(dic, list):
        res = dic
    else:
        raise TypeError("Undefined type for flatten: %s"%type(dic))

    return res


alle=flatten(all_weights)
a={"all":alle}


wordcloud_generator(all_weights)
#wordcloud_generator(a)





