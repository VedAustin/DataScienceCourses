import pylab

# You may have to change this path
WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of uppercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print "  ", len(wordList), "words loaded."
    return wordList

def plotVowelProportionHistogram(wordList, numBins=15):
    """
    Plots a histogram of the proportion of vowels in each word in wordList
    using the specified number of bins in numBins
    """
    x = map(propVowel,wordList)
    pylab.figure()
    pylab.title('Distribution of proportion of vowels in Words')
    pylab.xlabel('proportion')
    pylab.hist(x,bins = numBins)
    


def propVowel(aWord):
    vowels = ['a','e','i','o','u']
    total = 0
    for w in aWord:
        if w in vowels:
            total += 1
    return total/float(len(aWord))

    

if __name__ == '__main__':
    wordList = loadWords()
    plotVowelProportionHistogram(wordList)
    pylab.show()
    print "End"