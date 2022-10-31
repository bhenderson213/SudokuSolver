from tkinter import * 
from random import randint

printAnswers = False

BoxesIJ = {
    1:[[0, 1, 2], [0, 1, 2]]
    ,2: [[0, 1, 2], [3, 4, 5]]
    ,3: [[0, 1, 2], [6, 7, 8]]
    ,4: [[3, 4, 5], [0, 1, 2]]
    ,5: [[3, 4, 5], [3, 4, 5]]
    ,6: [[3, 4, 5], [6, 7, 8]]
    ,7: [[6, 7, 8], [0, 1, 2]]
    ,8: [[6, 7, 8], [3, 4, 5]]
    ,9: [[6, 7, 8], [6, 7, 8]]
}
global savedEntries
savedEntries = []

global setEntries
setEntries = True

global randomTriedPairs
randomTriedPairs = {}
global WON

def DetermineBox(i, j):
    # the boxes are like this: 
    # [1] [2] [3]
    # [4] [5] [6] 
    # [7] [8] [9]
    if i in [0, 1, 2]:
        if j in [0, 1, 2]:
            return 1 
        if j in [3, 4, 5]:
            return 2
        if j in [6, 7, 8]:
            return 3 
    if i in [3, 4, 5]:
        if j in [0, 1, 2]:
            return 4
        if j in [3, 4, 5]:
            return 5
        if j in [6, 7, 8]:
            return 6
    elif j in [0, 1, 2]:
        return 7
    elif j in [3, 4, 5]:
        return 8
    elif j in [6, 7, 8]:
        return 9
    
def LoadEntries():
    entries = []
    for i in range(9):
        entries.append([])
        for j in range(9):
            entry = IntVar()
            if len(savedEntries) == 0:
                entry.set('')
            else: 
                entry.set(savedEntries[i][j])
            entry.trace(mode='w', callback=checkCorrect)
            e = Entry(master, textvar=entry, width = 3)
            e.bind('<Return>', (lambda _: checkCorrect(entries)))
            entries[i].append(e)
            entries[i][j].grid(row=i, column=j)
    return entries 

def getBoxes(entries):
    boxes = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[], 9:[]}
    for i in range(9):
        for j in range(9):
            box = DetermineBox(i, j)
            boxes[box].append(entries[i][j].get())
    return boxes 

def checkCorrect(entries):
    global savedEntries
    if len(savedEntries) == 0:
        for i in range(9):
            savedEntries.append([])
            for j in range(9):
                savedEntries[i].append(entries[i][j].get())
        print("set entries.")
    allCorrect = True
    WON = False 
    entriesCorrect = []
    # First check if double in column or row 
    for i in range(9):
        entriesCorrect.append([])
        for j in range(9):
            entry = entries[i][j].get()
            entryCorrect = True
            for x in range(9):
                if (entry==entries[x][j].get() and x != i and entry!='') or (entry==entries[i][x].get() and x != j and entry!=''):
                    entryCorrect = False
            if not entryCorrect:
                entries[i][j].config({"background":"Red"})
                allCorrect = False
            else:
                entries[i][j].config({"background":"SystemWindow"})
            entriesCorrect[i].append(entryCorrect)
                
    # Check for duplicates in boxes 
    boxes = getBoxes(entries)
    for i in range(9):
        for j in range(9):
            entry = entries[i][j].get()
            box = DetermineBox(i, j)
            if boxes[box].count(entry) > 1 and entry != '':
                entries[i][j].config({"background":"Red"})
                allCorrect = False
            elif entriesCorrect[i][j]:
                entries[i][j].config({"background":"SystemWindow"})
                
    FindEntry(entries)
                    
    # check if all filled 
    allFilled = True
    for i in range(9):
        for j in range(9):
            if entries[i][j].get() == '':
                allFilled = False 
                break
    WON = allFilled and allCorrect 
    
    return allCorrect, WON

def GetPossibleEntries(entries):
    # get possible answers for each cell 
    allPossibilities = []
    for i in range(9):
        allPossibilities.append([])
        for j in range(9):
            if entries[i][j].get() == '':
                box = DetermineBox(i, j)
                possibilities = list(range(1, 10))
                boxes = getBoxes(entries)
                for number in boxes[box]:
                    if number != '':
                        possibilities.remove(int(number))
                # check what is in row
                inRow = []
                for x in range(9):
                    inRow.append(entries[i][x].get())
                for x in inRow:
                    if x != '' and int(x) in possibilities:
                        possibilities.remove(int(x))
                # check what is in column
                inRow = []
                for x in range(9):
                    inRow.append(entries[x][j].get())
                for x in inRow:
                    if x != '' and int(x) in possibilities:
                        possibilities.remove(int(x))
                
                #print("For i"+str(i)+" j"+str(j)+" the possibilities are:")
                #print("\t",possibilities)
            else:
                possibilities = []
                
            allPossibilities[i].append(possibilities)
    return allPossibilities

def FindEntry(entries):
    answerRandomly = False
    possibilities = GetPossibleEntries(entries)
    answerExists = False
    global savedEntries
    #global setEntries
    for i in range(9):
        for j in range(9):
            if len(possibilities[i][j]) == 1:
                if printAnswers:
                    print("Found an answer!", end = ' ')
                answerExists = True
                
                possible = possibilities[i][j]
                answer = possible[0]
                if printAnswers: 
                    print("Setting i"+str(i)+" j"+str(j)+" to", answer)
                entries[i][j].insert(0, str(answer))
                break
        if answerExists:
            return 
            break
        
    # only gets here if the others aren't true
    # gets like {box#:{number:[[i, j], [i, j]]}}
    if printAnswers: 
        print("Checking line possibility...", end = ' ')
    linePossibilities = {}
    boxes = getBoxes(entries)
    for i in range(9):
        for j in range(9):
            box = DetermineBox(i, j)
            #print("Box:", box, "i:", i, "j:", j)
            if box not in linePossibilities.keys():
                linePossibilities[box] = {}
            for x in range(1, 9+1): # possible answers
                if x not in linePossibilities[box].keys():
                    #print("Creating", x, "for box", box)
                    linePossibilities[box][x] = [] 
                if str(x) not in boxes[box] and entries[i][j].get()=='':
                    # check if in the lines too, not just box 
                    ok = True
                    for i2 in range(9):
                        if (entries[i2][j].get() == str(x) and i2 != i):
                            #print("No,", x, "is in column", j)
                            ok = False
                        if (entries[i][i2].get() == str(x) and i2 != j):
                            #print("No,", x, "is in row", i)
                            ok = False
                    if ok: 
                        #print("adding", x, "to i", i, "j", j)
                        linePossibilities[box][x].append([i, j])
    for box in boxes.keys(): 
        for x in range(1, 9+1):
            #print("Box:", box, "X="+str(x), linePossibilities[box][x], end = '\t')
            if len(linePossibilities[box][x]) == 1: 
                i = linePossibilities[box][x][0][0]
                j = linePossibilities[box][x][0][1]
                if printAnswers: 
                    print("\tSetting i"+str(i)+" j"+str(j)+" to", str(x))
                entries[i][j].insert(0, str(x))
                return # putting return so it doesn't try to put in multiple options
    
    if setEntries: 
        print("Found no answers...saving state.")
        savedEntries = []
        for i in range(9):
            savedEntries.append([])
            for j in range(9):
                savedEntries[i].append(entries[i][j].get())
        print("set entries.")
    if printAnswers: 
        print("Now trying random answers...")
    FindRandomEntry(entries)
    
def FindRandomEntry(entries):
    if printAnswers:
        print("Choosing random possibility...", end = ' ')
    global setEntries
    if setEntries == True:
        setEntries = False
    i = 0 
    j = 0
    possibilities = GetPossibleEntries(entries)
    while i < 9:
        #print(i, j)
        possible = possibilities[i][j] 
        ### I WAS HERE!!!!!
        if len(possible) > 0:
            for ii in range(len(possible)):
                answer = possible[ii]
                #print('i'+str(i)+' j'+str(j))
                #print(possible, "ii="+str(ii), answer)
                if str([i, j]) in randomTriedPairs.keys():
                    #print(randomTriedPairs[str([i,j])])
                    if answer not in randomTriedPairs[str([i, j])]:
                        if printAnswers: 
                            print("Setting i"+str(i)+" j"+str(j)+" to", answer)
                        entries[i][j].insert(0, str(answer))
                        if str([i, j]) not in randomTriedPairs.keys():
                            randomTriedPairs[str([i, j])] = []
                        randomTriedPairs[str([i, j])].append(answer)
                        return 
                else:
                    if printAnswers: 
                        print("Setting i"+str(i)+" j"+str(j)+" to", answer)
                    entries[i][j].insert(0, str(answer))
                    if str([i, j]) not in randomTriedPairs.keys():
                        randomTriedPairs[str([i, j])] = []
                    randomTriedPairs[str([i, j])].append(answer) 
                    return
        j += 1 
        if j == 9:
            j = 0
            i += 1
    # check if all filled 
    allFilled = True
    for i in range(9):
        for j in range(9):
            if entries[i][j].get() == '':
                allFilled = False 
                break
    WON = allFilled
    
    if not WON:
        print("Found no answers that route. Trying again...",end='')
        entries = LoadEntries()
        print(" loaded entries")
    else: 
        print("WON!!!")
        
master = Tk()

entries = []
for i in range(9):
    entries.append([])
    for j in range(9):
        entry = IntVar()
        if len(savedEntries) == 0:
            entry.set('')
        else: 
            entry.set(savedEntries[i][j])
        entry.trace(mode='w', callback=checkCorrect)
        e = Entry(master, textvar=entry, width = 3)
        e.bind('<Return>', (lambda _: checkCorrect(entries)))
        entries[i].append(e)
        entries[i][j].grid(row=i, column=j)
if len(savedEntries) > 0:
    print("loaded entries.")
else:
    print("?")

mainloop()