import random
import re
import time
import math

letters=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
            'Q','R','S','T','U','V','W','X','Y','Z']
VOWELS = ['A', 'E', 'I', 'O', 'U']

phrases = {}
VOWEL_COST  = 250

def getGuessableLetters(guessed):
    return [l for l in letters if l not in guessed]

def train(p):
    global phrases
    phrases = p

class WOFComputer():
    def __init__(self, difficulty=5):
        self.difficulty = difficulty

    def smartCoinFlip(self):
        return random.randint(1, 10) <= self.difficulty
    def dumbCoinFlip(self):
        return not self.smartCoinFlip()

    def getMove(self, *args, **kwargs):
        time.sleep(1)
        if self.smartCoinFlip():
            return self.getOptimalMove(*args, **kwargs)
        else:
            return self.getRandomMove(*args, **kwargs)

    def getOptimalMove(self, money, category, obscuredPhrase, guessed, wheelPrize):
        categoryPhrases = phrases[category]
        possiblePhrases = [p.upper() for p in categoryPhrases if self.dumbCoinFlip() or re.match('^'+obscuredPhrase.replace('_', '\w')+'$', p.upper())]

        if len(possiblePhrases) == 1 and self.smartCoinFlip():
            return possiblePhrases[0]

        letter_frequencies = {}
        for phrase in possiblePhrases:
            for c in phrase:
                if c.isalnum():
                    letter_frequencies[c] = letter_frequencies.get(c, 0)+1


        letters = letter_frequencies.keys()
        letters = random.sample(letters, random.randint(max(1,math.ceil(len(letters)*self.difficulty/10.0)), len(letters)))

        guess_preferences = sorted([c for c in letters if c not in guessed], key=lambda c:letter_frequencies[c], reverse=True)
        if money < VOWEL_COST:
            guess_preferences = [c for c in guess_preferences if c not in VOWELS]




        if len(guess_preferences) == 0:
            return 'PASS'
        else:
            return guess_preferences[0]

    def getRandomMove(self, money, category, obscuredPhrase, guessed, wheelPrize):
        possibleLetters = getGuessableLetters(guessed)
        if money < VOWEL_COST:
            possibleLetters = [l for l in possibleLetters if l not in VOWELS]

        if len(possibleLetters) == 0:
            return 'PASS'
        else:
            return random.choice(possibleLetters)
