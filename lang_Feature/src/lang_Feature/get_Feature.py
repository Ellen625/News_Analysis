#!/usr/bin/env python

'''
get_lang_feature.py - read text file and output language features into file

@author: Zhu
@date: Sep 3, 2015

Usage: $ python get_lang_feature.py -g <input-filename> <content-field>
  The <input-filename> is th name of the input filename. It is expected to be in CSV format. Each line contains one document.
  The <content-field> specifies which field is the content of the document to be processed. Default is 0. If the input CSV file only has single field in each line, <content-field> should be 0.
  The output will be saved into <input-filename>_FEATURE.csv. Each line contains 21 language feature values for the corresponding document content.
  The features are: (sentence count, word count, dictionary word count, and word count for each category).
  The categories are: function, pronouns, verbs, social, affective, cognative, ... (see LIWC2007LanguageManual.doc Table 1)
Example:
  $ python get_lang_feature.py -g ../../data/100_sample.csv 2 ## this will generate features for sample question title text
  $ python get_lang_feature.py -g ../../data/100_sample.csv 3 ## this will generate features for sample question content text
'''

import sys,os,csv
from eng_detect import *
import nltk.data
from liwc import *



def get_lang_feature_from_file(ifilename = None):
    # this will generate a set of language feature values for question content (sentence count, word count, dictionary word count, and word count for each category):
    # question_id, sentence count, word count, dictionary word count, function, pronouns, verbs, social, affective, cognative, ... (see LIWC2007LanguageManual.doc Table 1)
    print 'read from',ifilename
    ifile = open(ifilename,'rU')
    reader = csv.reader(ifile,delimiter=',',quotechar='\"',quoting=csv.QUOTE_MINIMAL)
    header = ['sentcnt']
    cats = ['wc','dic_wc','funct','ppron','verb','social','affect','cogmech','family','friend','posemo','negemo','anx','anger','sad','body','health','sexual','space','time']
    newID = ['ID']
    newDate = ['date']
    header.extend(cats)
    header.extend(newID)
    header.extend(newDate)
    rows = [header]
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    
    for i,fields in enumerate(reader):
	sys.stdout.write("\r                     \r"); sys.stdout.write("%i -" % (i)); sys.stdout.flush()
	content = utf8(fields[1])
	ID = utf8(fields[0])
	# if not is_english(title): print "NON_ENG title:", title
	#print content
	lang = 'EN'
	if len(content.strip())== 0: lang = 'NA'
	elif not is_english(content):
	    lang = 'other'
	    # print "NON_ENG content:",lang, content
	if lang != 'EN': continue
	content_sents = sent_detector.tokenize(content.strip())
	# print i,len(title_sents),len(content_sents)
	text = content
	text_cat2cnt = get_text2cat(cat,dic,text)
	row = [len(content_sents)]
	for c in cats:
	    n = 0
	    if c in text_cat2cnt: n = text_cat2cnt[c]
	    row.append(n)
	# print row
	for c in newID:
		m = 0
		m = ID
		row.append(m)
	rows.append(row)
    ifile.close()
    ofilename = ifilename.replace('.csv', '_FEATURE3.csv')
    ofile = open(ofilename, "w")
    writer = csv.writer(ofile,delimiter=',',quotechar='\"',quoting=csv.QUOTE_MINIMAL)
    writer.writerows(rows)
    ofile.close()
    print 'save to',ofilename    

def main(argv):
    args = set( a.lower() for a in sys.argv[1:] )
    for i,arg in enumerate(argv):
	if arg in ['-h','--help']: print 'usage:'
	if arg in ['-t','--test']: read_sample()
	if arg in ['-f','--feature']: get_lang_feature()
	if arg in ['-g','--getfeature']:
	    try: ifilename = argv[i+1]
	    except:
		print 'Error: no input file!'; exit(1)
	    if not os.path.exists(ifilename):
		print 'Error: input file not found!'; exit(1)
	    try: ifield = int(argv[i+2])
	    except: ifield = 0
	    get_lang_feature_from_file(ifilename)
    pass
if __name__ == '__main__': 
    main(sys.argv[1:])
