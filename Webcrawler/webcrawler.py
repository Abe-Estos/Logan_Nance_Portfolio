
import re
import nltk
from bs4 import BeautifulSoup
import requests
from nltk.corpus import stopwords
#functions
#gets urls from a soup
def geturls(soup):
    urlList = [] #url list
    # make urls into a list
    for link in soup.find_all('a'):
        linkText = str(link.get('href'))
        if (linkText not in urlList) and (re.search("\Ahttps://",linkText) or re.search("\A/[a-zA-Z]",linkText)):
            urlList.append(linkText)
            print(linkText)
            if len(urlList) > 15:
                break
    return urlList

def getText(urls):
    filenames = [] #list of filenales to return
    counter = 1
    for url in urls:
        filename = "rawSiteText" + str(counter)
        print(filename)
        filenames.append(filename)
        with open(filename, "w") as rawFile:
            soup = BeautifulSoup(requests.get(url).text)
            for scrap in soup(["script"],["style"]):
                scrap.extract()
            rawFile.write(soup.get_text())
        counter = counter + 1
    return filenames

#clean files of tabs and newlines
def cleanFiles(fileList):
    filenames = [] #list of filenales to return
    counter = 1
    for fn in fileList:
        filename = "cleanSiteText" + str(counter)
        print(filename)
        filenames.append(filename)
        with open(filename, "w") as cleanFile:
            with open(fn, "r") as rawFile:
                text = re.sub("[\n\t]", " ", rawFile.read())
                tokens = nltk.sent_tokenize(text)
                for tok in tokens:
                    cleanFile.write(tok + "\n")
        counter = counter + 1
    return filenames

def wordFreq(fileList):
    wordDict = {} #frequency of every word
    for fn in fileList:
        print(fn + " processing")
        with open(fn, "r") as file:
            for ln in file:
                tok = nltk.word_tokenize(ln.lower())
                tok = list([w for w in tok if w.isalpha()])#remove punctuation
                tok = list([w for w in tok if w not in stopwords.words('english')])#remove stopwords
                for t in tok:#sort
                    if (t in wordDict.keys()):
                        wordDict[t] = wordDict[t] + 1
                    else:
                        wordDict[t] = 1
    wordDict = dict(sorted(wordDict.items(), key=lambda item: item[1]))
    return wordDict

url = "https://www.horrorbuzz.com/games/strawberrycubes/"

soup = BeautifulSoup(requests.get(url).text)

urls = geturls(soup)
urls.append(url)

rawFiles = getText(urls)

cleanFileList = cleanFiles(rawFiles)

wordFreqList = wordFreq(cleanFileList)

print(list(wordFreqList.keys())[-40:])

print("Top 10 terms: film, game, theatre, horror, horrorbuzz, events, services, date, view, news")