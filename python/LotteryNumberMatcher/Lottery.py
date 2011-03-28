#!/usr/bin/python

def getMatchCount(nlist, olist, max):
    maxCount = max
    count = 0
    matched = []
    for n in nlist: # user-input number
        for o in olist: # the lottery number in the pre-defined text file
            #print "element of nlist: [" + n + "] , element of olist: [" + o + "]"
            if int(n) == int(o):
                #print "bingo!!"
                count = count + 1
                matched.append(n)
                break
    if count > maxCount:
        maxCount = count
    return count, matched, maxCount


input = raw_input("Lottery number? ")
numberList = input.split(' ')

fin = open('LotteryNumber.txt', 'r')
officialList = fin.readline().split(' ')
bingoList = []
maxCount = 0
while len(officialList) != 1:
    #print "==========================================================="
    
    matchCount, matchedList, maxCount = getMatchCount(numberList, officialList, maxCount)
    if matchCount == 6:
        bingoList = matchedList

    #print "Yours: ",
    #for n in numberList: 
    #    print n, 
    #print 
    #print "       ",
    #for o in officialList:
    #    print o,

    #print "Match count: " + str(matchCount) ,

    #print ",   [",
    #for m in matchedList:
    #    print m + " ", 
    #print "]"

    officialList = fin.readline().split(' ')

if len(bingoList) != 0:
    print "Bingo!!!  ",
    for b in bingoList:
        print b,
else:
    print "Good Luck! Max count: " + str(maxCount)
