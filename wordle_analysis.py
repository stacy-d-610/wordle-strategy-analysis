import sqlite3 as sl


# get letter stats

# https://stackoverflow.com/questions/13880786/python-sqlite3-string-variable-in-execute
def getTopLettersByPos(pos):
	wordDB = sl.connect('wordlist.db')
	colName = "pos_" + str(pos)
	testresult = wordDB.execute("SELECT %s, COUNT(*) AS 'ltr_counts' FROM WORD_POSITIONS GROUP BY %s ORDER BY COUNT(*) DESC LIMIT 3"  % (colName, colName))
	foundWord = testresult.fetchall()
	print(foundWord)
	wordDB.close()

def getOverallLetterFrequencies(numPos):
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
	return sorted(dictionary.items(), key = lambda kv: kv[1], reverse = True)



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
	(foundWord,) = testresult.fetchone()
	print(foundWord)
	wordDB.close()

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
	# allData()
	# getTopLettersByPos(1)
	# getTopLettersByPos(2)
	# getTopLettersByPos(3)
	# getTopLettersByPos(4)
	# getTopLettersByPos(5)
	print(getOverallLetterFrequencies(1))

main()