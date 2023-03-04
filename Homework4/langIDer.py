import pickle
import nltk
import itertools

#combination print and file write for ease of use
def writePrint(file, string):
    print(string)
    file.write(string + "\n")

#get all dictionaries from their pickles.
inData = open("data\LangId.train.Italian.unidic", "rb")
itUniDic = pickle.load(inData)
inData.close()
inData = open("data\LangId.train.Italian.bidic", "rb")
itBiDic = pickle.load(inData)
inData.close()
inData = open("data\LangId.train.French.unidic", "rb")
frUniDic = pickle.load(inData)
inData.close()
inData = open("data\LangId.train.French.bidic", "rb")
frBiDic = pickle.load(inData)
inData.close()
inData = open("data\LangId.train.English.unidic", "rb")
enUniDic = pickle.load(inData)
inData.close()
inData = open("data\LangId.train.English.bidic", "rb")
enBiDic = pickle.load(inData)
inData.close()
#calculate total vocabulary count
totalCount = len(enUniDic) + len(itUniDic) + len(frUniDic)
#get sentences to read
sentData = open("data/LangId.test", "rb")
solData = open("data/LangId.sol", "rb")
outData = open("data/wordLangId.out", "w")
#line total & correct total
lineTotal = 0
corTotal = 0

for sentence, solution in itertools.zip_longest(sentData, solData):
    engProb = 1
    itlProb = 1
    freProb = 1
    guess = ""
    unigrams = nltk.word_tokenize(sentence.decode('utf-8'))
    bigrams = list(nltk.ngrams(unigrams,2))
    for bi in bigrams:
        #calculate english probability
        biEngCount = 0
        if bi in enBiDic:
            biEngCount = enBiDic[bi]
        uniEngCount = 0
        if bi[0] in enUniDic:
            uniEngCount = enUniDic[bi[0]]
        engProb = engProb * (biEngCount + 1)/(uniEngCount + totalCount)
        #calculate french probability
        biFrCount = 0
        if bi in frBiDic:
            biFrCount = frBiDic[bi]
        uniFrCount = 0
        if bi[0] in frUniDic:
            uniFrCount = frUniDic[bi[0]]
        freProb = freProb * (biFrCount + 1)/(uniFrCount + totalCount)
        #calculate italian probability
        biItCount = 0
        if bi in itBiDic:
            biItCount = itBiDic[bi]
        uniItCount = 0
        if bi[0] in itUniDic:
            uniItCount = itUniDic[bi[0]]
        itlProb = itlProb * (biItCount + 1)/(uniItCount + totalCount)
    if(engProb == max(engProb,itlProb,freProb)):
        guess = "English"
    elif (itlProb == max(engProb, itlProb, freProb)):
        guess = "Italian"
    else:
        guess = "French"
    #print guess
    writePrint(outData,guess)
    if(guess == solution.decode('utf-8')[-(len(guess) + 1):-1]):
        corTotal = corTotal + 1
    lineTotal = lineTotal + 1

#print accuracy
writePrint(outData,str(corTotal/lineTotal))

#close all files
sentData.close()
solData.close()
outData.close()