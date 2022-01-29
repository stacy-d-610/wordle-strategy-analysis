# wordle-strategy-analysis

[Wordle](https://www.powerlanguage.co.uk/wordle/) is a game that's taken the internet by storm. It is a simple game where the goal is to guess the 5 letter word of the day within six guesses using the clues given on each guess. 

On each guess, the player is told whether a letter of a given position is in the word or in the position. Thus, for our analysis, we mainly consider the frequency of the letter in all the possible words and the frequency of the letter in each position.

For this analysis, I am using the word bank from Wordle itself. This can be found through the source code, or cleaned found at https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b and https://gist.github.com/cfreshman/cdcdf777450c5b5301e439061d29694c. 

I used this project as a chance to practice SQL. I added SQLite to the Python code to store the words from the text files above and to process some functions faster. 

I first found the top five most frequent words to see if we can form a word using these letters. Here are the letters and the frequency they appeared in the word bank, repeats within the same word were not counted.
[('s', 5936), ('e', 5705), ('a', 5330), ('o', 3911), ('r', 3909)]

AROSE can be formed from these letters and used in the game. However, success in the game means that the player also has to get the letters in the correct positions. Since the game tells you whether or not your letter is in the correct position, it makes sense to narrow down the number of possible positions as much as possible. 

I then ran code to see the top letters in each position:
1. [('s', 1565), ('c', 922), ('b', 909), ('p', 859), ('t', 815)]
2. [('a', 2263), ('o', 2096), ('e', 1628), ('i', 1383), ('u', 1187)]
3. [('a', 1236), ('r', 1198), ('i', 1051), ('o', 993), ('n', 964)]
4. [('e', 2327), ('a', 1074), ('t', 898), ('i', 880), ('n', 788)]
5. [('s', 3958), ('e', 1522), ('y', 1301), ('d', 823), ('t', 727)]

It seems that AROSE is pretty far off the ideal first guess using this criteria. 

Using just the frequencies in each position, it seems that CARES is the best word. However, 'c' is not one of the top letters.
[('s', 5936), ('e', 5705), ('a', 5330), ('o', 3911), ('r', 3909), ('i', 3589), ('l', 3114), ('t', 3033), ('n', 2787), ('u', 2436), ('d', 2298), ('y', 2031), ('c', 1920), ('p', 1885), ('m', 1868), ('h', 1708), ('g', 1543), ('b', 1519), ('k', 1444), ('w', 1028), ('f', 990), ('v', 674), ('z', 391), ('j', 289), ('x', 287), ('q', 111)]

It's hard to say the exact impact of position versus eliminating the letter without going deep into the math. However, we could see that of the top five letters for position one, 't' also appears pretty high up on the overall frequency list. Since it is almost twice as frequent overall than 'c' is, TARES might be a better starting word than CARES. 

You can check out the code and run it yourself using the text files above to come to your own conclusions. Thanks for reading!

