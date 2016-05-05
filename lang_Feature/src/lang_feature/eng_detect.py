# @see http://www.algorithm.co.il/blogs/programming/python/cheap-language-detection-nltk/
import sys,nltk
from sys import stdin

ENGLISH_STOPWORDS = set(nltk.corpus.stopwords.words('english'))
NON_ENGLISH_STOPWORDS = set(nltk.corpus.stopwords.words()) - ENGLISH_STOPWORDS
 
STOPWORDS_DICT = {lang: set(nltk.corpus.stopwords.words(lang)) for lang in nltk.corpus.stopwords.fileids()}

def utf8(str): return unicode(str, 'latin1').encode('utf-8').decode('utf8', 'replace')

def get_language(text):
    words = set(nltk.wordpunct_tokenize(text.lower()))
    return max(((lang, len(words & stopwords)) for lang, stopwords in STOPWORDS_DICT.items()), key = lambda x: x[1])[0]
 
 
def is_english(text):
    text = text.lower()
    words = set(nltk.wordpunct_tokenize(text))
    return len(words & ENGLISH_STOPWORDS) > len(words & NON_ENGLISH_STOPWORDS)

if __name__ == '__main__':
    input_text = utf8(" ".join([x for x in stdin.readlines()]))
    import time
    start = time.clock()
    print is_english(input_text)
    elapsed = time.clock()
    print "Time spent in (function name) is: ", elapsed-start
