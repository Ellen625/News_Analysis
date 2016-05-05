#!/usr/bin/env python

'''
test_sample.py - read 100 YQA samples and test language detection, etc.

@author: Zhu
@date: August 1, 2015

'''

import sys,os,csv
from eng_detect import *
import nltk.data
from liwc import *

def read_sample(ifilename = '../../data/100_sample.csv'):
    print 'read from',ifilename
    ifile = open(ifilename,'rU')
    reader = csv.reader(ifile,delimiter=',',quotechar='\"',quoting=csv.QUOTE_MINIMAL)
    rows = []
    for i,fields in enumerate(reader):
	sys.stdout.write("\r                     \r"); sys.stdout.write("%i -" % (i)); sys.stdout.flush()
	title,content = utf8(fields[2]),utf8(fields[3])
	# do not use title becuse the length is too short
	# if not is_english(title): print "NON_ENG title:", title
	lang = 'EN'
	if len(content.strip())== 0: lang = 'NA'
	elif not is_english(content):
	    lang = 'other'
	    # print "NON_ENG content:",lang, content
	fields.append(lang)
	rows.append(fields)
    ifile.close()
    ofilename = '../../output/100_sample.csv'
    ofile = open(ofilename, "w")
    writer = csv.writer(ofile,delimiter=',',quotechar='\"',quoting=csv.QUOTE_MINIMAL)
    writer.writerows(rows)
    ofile.close()
    print 'save to',ofilename
    
def get_lang_feature(ifilename = '../../data/100_sample.csv'):
    # this will generate a set of language feature values for question content (sentence count, word count, dictionary word count, and word count for each category):
    # question_id, sentence count, word count, dictionary word count, function, pronouns, verbs, social, affective, cognative, ... (see LIWC2007LanguageManual.doc Table 1)
    print 'read from',ifilename
    ifile = open(ifilename,'rU')
    reader = csv.reader(ifile,delimiter=',',quotechar='\"',quoting=csv.QUOTE_MINIMAL)
    header = ['id','sentcnt']
    cats = ['wc','dic_wc','funct','ppron','verb','social','affect','cogmech','family','friend','posemo','negemo','anx','anger','sad','body','health','sexual','space','time']
    header.extend(cats)
    rows = [header]
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    
    for i,fields in enumerate(reader):
	sys.stdout.write("\r                     \r"); sys.stdout.write("%i -" % (i)); sys.stdout.flush()
	title,content = utf8(fields[2]),utf8(fields[3])
	# if not is_english(title): print "NON_ENG title:", title
	lang = 'EN'
	if len(content.strip())== 0: lang = 'NA'
	elif not is_english(content):
	    lang = 'other'
	    # print "NON_ENG content:",lang, content
	if lang != 'EN': continue
	title_sents = sent_detector.tokenize(title.strip())
	content_sents = sent_detector.tokenize(content.strip())
	# print i,len(title_sents),len(content_sents)
	text = content
	text_cat2cnt = get_text2cat(cat,dic,text)
	row = [fields[0],len(content_sents)]
	for c in cats:
	    n = 0
	    if c in text_cat2cnt: n = text_cat2cnt[c]
	    row.append(n)
	# print row
	rows.append(row)
    ifile.close()
    ofilename = '../../output/100_sample_content_features.csv'
    ofile = open(ofilename, "w")
    writer = csv.writer(ofile,delimiter=',',quotechar='\"',quoting=csv.QUOTE_MINIMAL)
    writer.writerows(rows)
    ofile.close()
    print 'save to',ofilename

def get_lang_feature_from_file(ifilename = None, ifield = 3):
    # this will generate a set of language feature values for question content (sentence count, word count, dictionary word count, and word count for each category):
    # question_id, sentence count, word count, dictionary word count, function, pronouns, verbs, social, affective, cognative, ... (see LIWC2007LanguageManual.doc Table 1)
    print 'read from',ifilename
    ifile = open(ifilename,'rU')
    reader = csv.reader(ifile,delimiter=',',quotechar='\"',quoting=csv.QUOTE_MINIMAL)
    header = ['sentcnt']
    cats = ['wc','dic_wc','funct','ppron','verb','social','affect','cogmech','family','friend','posemo','negemo','anx','anger','sad','body','health','sexual','space','time']
    header.extend(cats)
    rows = [header]
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    
    for i,fields in enumerate(reader):
	sys.stdout.write("\r                     \r"); sys.stdout.write("%i -" % (i)); sys.stdout.flush()
	content = utf8(fields[ifield])
	# if not is_english(title): print "NON_ENG title:", title
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
	rows.append(row)
    ifile.close()
    ofilename = ifilename.replace('.csv', '_FEATURE.csv')
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
	    get_lang_feature_from_file(ifilename, ifield)
    pass
if __name__ == '__main__': 
    main(sys.argv[1:])
