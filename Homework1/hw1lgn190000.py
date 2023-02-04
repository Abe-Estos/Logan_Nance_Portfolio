import sys
import re
import pickle

#make a class
class Person:
    def __init__(self,l,f,m,i,p):
        self.last = l
        self.first = f
        self.mi = m
        self.id = i
        self.phone = p
    def display(self):
        print("Employee ID: " + self.id)
        print("\t" + self.first + " " + self.mi + " " + self.last)
        print("\t" + self.phone)

#process as requested
def dictionaryCSV(data):
    #make outdict
    outDict = dict()
    #split at commas, format, and inster into dictionart
    for ln in data:
        arr = ln.split(",")
        last = arr[0][0].capitalize() + arr[0][1:].lower()
        first = arr[1][0].capitalize() + arr[1][1:].lower()
        mi = 'X'
        if arr[2].isalpha():
            mi = arr[2][0].capitalize()
        id = arr[3]
        while not (re.search("[A-Z]{2}[0-9]{4}", id) and len(id) == 6):
           id = re.sub("\n","",input("Error: ID is not in the correct format, please enter the corrected ID as two captial letters followed by 4 digits:"))
        pa = re.findall("[0-9]",arr[4])
        phone = pa[0] + pa[1] + pa[2] + "-" + pa[3] + pa[4] + pa[5] + "-" + pa[6] + pa[7] + pa[8] + pa[9]
        #check if duplicate IDs
        if id in outDict:
            print("Error: Dupilicate ID. Aborting")
            exit()
        #Input person into outDict
        outDict.update({id:Person(last, first, mi, id, phone)})
    return outDict

#open file
filename = sys.argv[1]
OldData = open(filename,"r")
OldData.readline()

#make dictionary and newdata file writing in binary
personDict = dictionaryCSV(OldData)
newData = open("data/data.txt", "wb")

#dump dictionaryy to newdata
pickle.dump(personDict,newData)

#change newdata to read in binary
newData.close()
newData = open("data/data.txt", "rb")
loadDict = pickle.load(newData)

#display information
print("Employee list:")
for i in loadDict:
    print("")
    loadDict[i].display()

#close files
newData.close()
OldData.close()