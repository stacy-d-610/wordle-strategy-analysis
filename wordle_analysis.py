import sqlite3 as sl
import itertools


# def bestWordByOverallFrequency():



def bestWordByPositionFrequency():
	topLettersList = []
	for i in range(1,6):
		topLettersList.append(getTopLettersByPos(i)[0:5])


	allCombi = itertools.product(*topLettersList)

	bestFrequency = 0
	bestWord = ""

	for r in allCombi:
		currentWord = ""
		currentFrequency = 0
		repeats = []
		hasRepeat = False
		for ltrTuple in r:
			currentWord += ltrTuple[0]
			currentFrequency += ltrTuple[1]
			if(ltrTuple[0] in repeats):
				hasRepeat = True
			repeats.append(ltrTuple[0])
		if searchWordBank(currentWord) and currentFrequency > bestFrequency and not hasRepeat:
			bestWord = currentWord
			bestFrequency = currentFrequency


	return (bestWord, bestFrequency)



# https://stackoverflow.com/questions/13880786/python-sqlite3-string-variable-in-execute
def getTopLettersByPos(pos, numShown=-1):
	wordDB = sl.connect('wordlist.db')
	colName = "pos_" + str(pos)
	testresult = wordDB.execute("SELECT %s, COUNT(*) AS 'ltr_counts' FROM WORD_POSITIONS GROUP BY %s ORDER BY COUNT(*) DESC"  % (colName, colName))
	foundWord = testresult.fetchall()
	wordDB.close()
	if(numShown == -1):
		return foundWord
	return foundWord[0:numShown]

def getLetterPositionFrequencies(ltr, pos = -1):
	wordDB = sl.connect('wordlist.db')
	frequencies = [ltr]
	for i in range(1, 6):
		colName = "pos_" + str(i)
		testresult = wordDB.execute("SELECT %s, COUNT(*) AS 'ltr_counts' FROM WORD_POSITIONS GROUP BY %s" % (colName, colName))
		foundWord = testresult.fetchall()
		frequencies.append(dict(foundWord)[ltr])
	wordDB.close()

	if pos > 0:
		return frequencies[pos]

	return frequencies


def getOverallLetterFrequencies(numShown=-1):
	dictionary = {}
	wordDB = sl.connect('wordlist.db')
	for i in range(1, 6):
		colName = "pos_"
		colName += str(i)
		testresult = wordDB.execute("SELECT %s, COUNT(*) AS 'ltr_counts' FROM WORD_POSITIONS GROUP BY %s" % (colName, colName))
		if len(dictionary) == 0:
			dictionary = dict(testresult.fetchall())
		else:
			tempDictionary = dict(testresult.fetchall())
			for ltr in tempDictionary.keys():
				if(ltr in dictionary.keys()):
					dictionary[ltr] = tempDictionary[ltr] + dictionary[ltr]
				else:
					dictionary[ltr] = tempDictionary[ltr]
	wordDB.close()

	if numShown == -1:
		return sorted(dictionary.items(), key = lambda kv: kv[1], reverse = True)
	# add a part where it has no repeats
	return sorted(dictionary.items(), key = lambda kv: kv[1], reverse = True)[0:numShown]

def getOverallLetterFrequenciesNoRepeatCount(numShown=-1):
	dictionary = {}
	wordDB = sl.connect('wordlist.db')
	testresult = wordDB.execute("SELECT word FROM WORD_POSITIONS")
	for w in testresult:
		(word, ) = w
		ltrs = set(word)
		for l in ltrs:
			if(l in dictionary.keys()):
				dictionary[l] += 1
			else:
				dictionary[l] = 1
	wordDB.close()

	if numShown == -1:
		return sorted(dictionary.items(), key = lambda kv: kv[1], reverse = True)

	return sorted(dictionary.items(), key = lambda kv: kv[1], reverse = True)[0:numShown]


def populateWordDatabase(wordArray):
	wordDB = sl.connect('wordlist.db')
	wordTupleArray = []
	for w in wordArray:
		wordTupleArray.append((w, w[0], w[1], w[2], w[3], w[4]))

	wordDB.execute("""CREATE TABLE WORD_POSITIONS(
			word STRING NOT NULL,
			pos_1 STRING,
			pos_2 STRING,
			pos_3 STRING,
			pos_4 STRING,
			pos_5 STRING
		); 
	""")
	populateSQL = 'INSERT INTO WORD_POSITIONS (word, pos_1, pos_2, pos_3, pos_4, pos_5) VALUES (?, ?, ?, ?, ?, ?)'
	wordDB.executemany(populateSQL, wordTupleArray)
	wordDB.commit()
	wordDB.close()


def searchWordBank(searchTerm):
	wordDB = sl.connect('wordlist.db').cursor()
	testresult = wordDB.execute("SELECT word FROM WORD_POSITIONS WHERE word = ?", (searchTerm,))
	testresultVal = testresult.fetchone()
	foundWord = False
	if(testresultVal != None):
		foundWord = True
	wordDB.close()
	return foundWord


def allData():
	wordDB = sl.connect('wordlist.db').cursor()
	tablePrintTest = wordDB.execute('SELECT * from WORD_POSITIONS')
	print(tablePrintTest.fetchall())
	wordDB.close()

def main():
	f = open('wordle_word_possibilities.txt', 'r')
	words = f.read()
	wordArray1 = words.split("\n")
	f.close()

	f = open('wordle-answers-alphabetical.txt', 'r')
	words = f.read()
	wordArray2 = words.split("\n")
	f.close()

	populateWordDatabase(wordArray1 + wordArray2)


	print("Here are the top 5 letters by overall frequency with no repeats.")
	print(getOverallLetterFrequenciesNoRepeatCount(5))
	print("Let's also check the top 5 letters by overall frequency to see if there is a difference in the top 5.")
	print(getOverallLetterFrequencies(5))
	print("Since there is no difference in the order of frequency, we will use the no repeat result. Intuitively, there are too many letters and not enough repeat patterns to test duplicates on the first try.")
	print("The letters can be rearranged to be 'arose'.")
	print("Let's check if arose is in the word bank.")
	print(searchWordBank("arose"))
	print("Let's also check top letters by position. This is important because if they differ, we should calculate the pool of words narrowed down.")
	print(getTopLettersByPos(1, 1))
	print(getTopLettersByPos(2, 1))
	print(getTopLettersByPos(3, 1))
	print(getTopLettersByPos(4, 1))
	print(getTopLettersByPos(5, 1))
	print("Upon first glance, 's', 'a', and 'e' appear in the top letters by position list. Our word 'arose' does not align any top letter with the position they are most often seen in.")
	print("Let's also take a look at the top 5 letters for each position.")
	print(getTopLettersByPos(1, 5))
	print(getTopLettersByPos(2, 5))
	print(getTopLettersByPos(3, 5))
	print(getTopLettersByPos(4, 5))
	print(getTopLettersByPos(5, 5))
	print("From looking at the dictionaries above, we see that our word doesn't eliminate all of the words in the individual positions. There are also repeats for each.")
	print("The feedback provided by the game always eliminates letters, however, position is also important in ultimately guessing the word. Getting the position correct gives us the most useful feedback at the first stage for guessing later words. This is how many words arose can potentially eliminate from our list based on the positions (not checking for overlap between letters).")
	print("Here's a list of the frequencies of each letter of 'arose' in their respective positions:")
	print([getLetterPositionFrequencies("a", 1), getLetterPositionFrequencies("r", 2), getLetterPositionFrequencies("o", 3), getLetterPositionFrequencies("s", 4), getLetterPositionFrequencies("e", 5)])
	print("From here, let's run a function that can find the word that will help maximize the number of words eliminated based on the letter frequencies of each position. We will be checking the word against the word bank to see if it would be a valid answer. Since the game doesn't penalize the player for using words outside of the word bank, this is reflective of what would be accepted in the game.")
	print("We will run this with the no-repeat frequencies. (You may have to wait for the script to run for a bit).")
	print(bestWordByPositionFrequency())
	print("Since the most frequent letters are also in the top position frequencies, let's look for a word that has the least tradeoffs.")
	print(getOverallLetterFrequenciesNoRepeatCount())
	print("Based on the letters above, it seems that 'tares' would be the ideal word to start with. Without diving into deeper math, it's hard to know how much the position of the word should be valued over the frequency of the letter in the overall word. However, we can see that there are about twice as many words with 't' in it than 'c', and much less for the first position. Thus, our current conclusion is that 'tares' is the optimal starting word.")
	print("Since there have been plenty of articles on the best starting word for Wordle, I wanted to compare one such example to 'tare'.")
	print("Here you see a comparison of the two.")
	print("By position:")
	print("tares: " + str([getLetterPositionFrequencies("t", 1), getLetterPositionFrequencies("a", 2), getLetterPositionFrequencies("r", 3), getLetterPositionFrequencies("e", 4), getLetterPositionFrequencies("s", 5)]))
	print("later:" + str([getLetterPositionFrequencies("l", 1), getLetterPositionFrequencies("a", 2), getLetterPositionFrequencies("t", 3), getLetterPositionFrequencies("e", 4), getLetterPositionFrequencies("r", 5)]))
	print("By overall frequency:")
	taresTotal = 0
	for l in "tares":
		taresTotal += dict(getOverallLetterFrequencies())[l]
	print("tares: " + str(taresTotal))
	laterTotal = 0
	for l in "later":
		laterTotal += dict(getOverallLetterFrequencies())[l]
	print("later: " + str(laterTotal))
	print("We can see that judging by both criteria, 'tares' is the better option.")
main()
