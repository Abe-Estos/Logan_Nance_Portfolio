import sys
import re
import pickle
import nltk

#open filename at argv
filename = sys.argv[1]
inData = open(filename, "r",encoding='utf-8')

#process raw text into lowercase tokens without newlines or non alphanumetics
rawText = ""
for ln in inData:
    rawText = rawText + " " + ln;
rawText = re.sub("\n", "", rawText);
unigrams = nltk.word_tokenize(rawText)
#make bigrams
bigrams = list(nltk.ngrams(unigrams,2))
#make dictionaries
uniDic = {u:unigrams.count(u) for u in set(unigrams)}
biDic = {b:bigrams.count(b) for b in set(bigrams)}
#make files for picling
uniData = open(filename + ".unidic", "wb")
biData = open(filename + ".bidic", "wb")
#pickle those files
pickle.dump(uniDic,uniData)
pickle.dump(biDic,biData)
#close remaining files
uniData.close()
biData.close()
inData.close()