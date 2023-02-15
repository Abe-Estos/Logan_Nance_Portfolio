import nltk
import random
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import sys
#
def getNouns(rawText):
    textTok = nltk.word_tokenize(rawText.lower())#lowercase and tokenise
    # remove all stopwords, nonwrds, and words shorter than 6
    textTok = [w for w in textTok if (w.isalpha() and (len(w) > 5) and (w not in stopwords.words("english")))]
    #lemmatize text & make unique
    lemma = WordNetLemmatizer()
    textLem = set([lemma.lemmatize(w) for w in textTok])
    #pos tagging
    posTags = nltk.pos_tag(textLem)
    print(posTags[:20])
    #get nouns
    posNouns = [n[0] for n in posTags if (n[1] == "NN")]
    print("Number of tokens: " + str(len(textTok)) + "\nNumber of unique nouns: " + str(len(posNouns)))
    return textTok, posNouns

#Exits if not enough arguments
if(len(sys.argv) < 2):
    print("Error: no argument provided for source file.")
    exit()

fileInPath = sys.argv[1]
fileIn = open(fileInPath, "rt")
fileInRaw = fileIn.read()
fileInTok = nltk.word_tokenize(fileInRaw.lower())#makes lower case for ease of use.
fileText = nltk.Text(fileInTok)
#makes a set of words, counts the unique ones, then divides it by the total and outputs it as a format
fileTextWords = [w for w in fileText if w.isalpha()]
print("The lexical diversity of the given text is {0:.2f}.\n".format(len(set(fileTextWords))/len(fileTextWords)))
#run getNouns
tok, noun = getNouns(fileInRaw)

#get 50 most common nouns
#caounts number of occurances
dictNouns = dict()
for t in tok:
    if(t in noun):
        if(t in dictNouns.keys()):
            dictNouns[t] = dictNouns[t] + 1
        else:
            dictNouns[t] = 1
#sort nouns by number
dictNouns = dict(sorted(dictNouns.items(), key = lambda item: item[1]))

#initial game set up
guess = ""
score = 5
goal = random.choice(list(dictNouns.keys())[-50:]) # gets 50 most common nouns
guessed = list()
#run game
while (guess != "!") and (score > -1):
    if guess == "":
        print("Let's play a word guessing game!")
        guessed = ["_" for c in goal]
    for c in guessed:print(c + " ", end = "")
    print()
    guess = input("Guess a letter")[0]
    correct = False # will become true if a letter is guessed
    finished = True # will become false if a letter isn't alphanumeric
    for i in range(len(goal)):
        if guess == goal[i]:
            correct = True
            guessed[i] = guess
        if not guessed[i].isalpha():
            finished = False
    #runs code if correct
    if correct:
        print("Right! ", end = "")
        score = score + 1
    else:
        print("Sorry. Guess again! ", end = "")
        score = score - 1
    print("Score is " + str(score))
    #will get new word if word is finished
    if finished:
        print("Concragulations(sic), You guessed that word correctly!")
        for c in guessed: print(c + " ", end="")
        print("\n")
        guess = ""
        goal = random.choice(list(dictNouns.keys())[-50:]) # gets 50 most common nouns
        guessed = list()

fileIn.close()
