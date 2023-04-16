# This is a sample Python script.
import random

import wikipedia
import pickle
import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
class User:
    def __init__(self, name = "N/A", likes = {}, interests = []):
        self.name = name
        self.likes = likes
        self.interests = interests

def listString(ls):  #assumes string isn't 0
    if len(ls) <= 1: return ls[0]
    if len(ls) == 2: return ls[0] + " and " + ls[1]
    return ls[0] + ", " + listString(ls[1:])

users = []
curUser = User()
state = "start"  # show's state
reply = ""
name = ""
mood = 0.0

if __name__ == '__main__':
    #unpickle users
    try:
        usersFile = open("users", "rb")
    except FileNotFoundError:
        users = []
    else:
        users = pickle.load(usersFile)
        usersFile.close()
    #make sentiment intensity analyser
    sid = SentimentIntensityAnalyzer()
    # introduce yourself
    print("Hello! I'm Wuntoothry, who are you? (Just type your name please.)")
    while (True):
        reply = input(">")
        if (reply == "exit"): break
        match state:
            case "idle":
                match word_tokenize(reply.lower()):
                    case ["goodbye" | "bye", *_]:  # say goodbye
                        print("Goodbye " + name + ", and hello new user! Could you tell me your name?")
                        state = "start"
                    case ["who","am","i", *_]:
                        print("You are {}.".format(curUser.name))
                        if(len(curUser.interests) > 0):
                            print("You are interested in {}.".format(listString(curUser.interests)))
                    case ["what"|"who","is", subj, *_]:
                        try:
                            print(wikipedia.summary(wikipedia.search(subj)[0], sentences=3))
                            curUser.interests.append(subj)
                            curUser.interests = list(set(curUser.interests))
                        except Exception:
                            print("I'm sorry but I cannot find information about {}.".format(subj))
                    case ["tell", "me", "something", "cool"|"neat"|"interesting", *_]:
                        print(wikipedia.summary(wikipedia.search(random.choice(curUser.interests))[0], sentences=3))
                    case ["what"|"who","are","you", *_]:
                        print("I am Wuntoothry. An AI chatbot made by Abe Estos. While I am very simple, I still store information about users and use it in my conversations.")
                    case other:
                        feeling = sid.polarity_scores(reply)["compound"]
                        if feeling > 0.2:
                            print("Glad you feel that way!")
                        elif feeling < -0.2:
                            print("I'm so sorry that's the case.")
                            if mood < -3:
                                print("Are you having a bad day? Why don't you tell me about it?")
                                mood = 0.0
                        else:
                            print("I'm not sure how to feel about that.")
                        mood = mood + feeling
            case "start":
                mood = 0.0 #reset mood if restarting.
                name = reply
                if(name != "exit"):
                    prevUser = False
                    for u in users:
                        if (u.name == name):
                            prevUser = True
                            curUser = u
                    if(prevUser):
                        print("Hello {}! Glad you're back!".format(name))
                    else:
                        print("Hello {}! Nice to meet you!".format(name))
                        curUser = User(name)#add users and append them
                        users.append(curUser)
                state = "idle"
            case other:
                print("Whoopsies, you found a bug. Abe probably misspelled a state somewhere, let's start over, shall we?")
                state = "start"
    usersFile = open("users", "wb")
    pickle.dump(users, usersFile)
    usersFile.close()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
