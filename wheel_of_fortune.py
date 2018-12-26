# Andrew Boskovich

import json
import wof_computer
import random

NUM_HUMAN   = 1
NUM_PLAYERS = 3
VOWEL_COST  = 250
VOWELS = ['A', 'E', 'I', 'O', 'U']

# Load the wheel
wheelFile = open('wheel.json', 'r')
wheel = json.loads(wheelFile.read())
wheelFile.close()

# Load the phrase set
phraseFile = open('phrases.json', 'r')
phrases = json.loads(phraseFile.read())
phraseFile.close()
wof_computer.train(phrases)

# Uncomment these to see the structure of wheel and phrases

# print(json.dumps(wheel,indent=3))
# print(json.dumps(phrases,indent=3))

# Get a random item from wheel
def spinWheel():
    return random.choice(wheel)

# Get a random phrase and category
def getCategoryAndPhrase():
    category = random.choice(list(phrases.keys()))
    phrase   = random.choice(phrases[category])
    return (category, phrase.upper())

def createPlayer(isComputer, player_num):
    if isComputer:
        name = 'Computer {}'.format(player_num)
    else:
        name = input('Enter your name: ')

    return WheelOfFortunePlayer(name, isComputer)

# Obscures the phrase
def obscurePhrase(phrase, guessed):
    whole_phrase = []
    phrase = phrase.split() # split the phrase into separate words
    for word in phrase:
        obscured_word = ''.join(letter if letter in guessed or not letter.isalnum() else '_' for letter in word)
        whole_phrase.append(obscured_word)
    obscured_phrase = ' '.join(whole_phrase) # recombine the list
    return obscured_phrase

class WheelOfFortunePlayer():
    def __init__(self, name, isComputer):
        self.name       = name
        self.prizeMoney = 0
        self.prizes     = []
        if isComputer:
            self.computer = wof_computer.WOFComputer(difficulty = random.randint(1,9))
        else:
            self.computer = False


    def addMoney(self, amount):
        self.prizeMoney += amount

    def subtractMoney(self, amount):
        return self.addMoney(-amount)

    def goBankrupt(self):
        self.prizeMoney = 0

    def addPrize(self, prize):
        self.prizes.append(prize)

    def getMove(self, *args, **kwargs):
        if(self.computer):
            return self.computer.getMove(*args, **kwargs)
        else:
            return input('Enter your guess: ').upper()
    def __str__(self):
        return '{} (${})'.format(self.name, self.prizeMoney)

# print('Random spin result:')
# wheelPrize = spinWheel()
# print(wheelPrize)
#
# category, phrase = getCategoryAndPhrase()
# print('\nRandom Category: {}\nRandom Phrase:   {}'.format(category, phrase))
#
# # example code to illustrate how getMove works. You should delete this.
# comp_obscured_phrase = 'R___ ____AR'
# comp_obscured_category = 'Place'
#
# print('\n\nComputer guess for {} ({})'.format(comp_obscured_phrase, comp_obscured_category))
#
# computer_1 = wof_computer.WOFComputer(difficulty = random.randint(1,9))
# computerMove = computer_1.getMove(money=0, category=comp_obscured_category, obscuredPhrase = comp_obscured_phrase,
#                                     guessed=['P','N','X','R','A','Z','S'], wheelPrize=wheelPrize)
# print('Computer says: {}'.format(computerMove))
def guessChar(phrase, guess, guessed):
        count = phrase.count(guess)
        if count:
            if count > 1:
                print('... there are {} {}\'s\n'.format(count, guess))
            else:
                print('... there is 1 {}\n'.format(guess))
        else:
            print('... there 0 {}\'s\n'.format(guess))
        return count

def printWinnings(player):
    prizes = list(set(player.prizes)) # turning it into a set removes the non unique prizes
    if not prizes:
        print('... {} wins ${}'.format(player.name, player.prizeMoney))
    elif len(prizes) == 1:
        print('... {} wins ${} and {}'.format(player.name, player.prizeMoney, prizes[0][0].lower() + prizes[0][1:]))
    elif len(prizes) == 2:
        print('... {} wins ${}, {}, and {}'.format(player.name, player.prizeMoney, prizes[0][0].lower() + prizes[0][1:-1], prizes[1][0].lower() + prizes[1][1:]))
    exit()

def playGame():
    players = [createPlayer(player_num>=NUM_HUMAN, player_num+1) for player_num in range(NUM_PLAYERS)]
    guessed = []
    category, phrase = getCategoryAndPhrase()
    playerIndex = 0
    player = players[playerIndex]

    while True:

        while True:
            wheelPrize = spinWheel()

            if wheelPrize['type'] == 'cash':
                obscuredPhrase = obscurePhrase(phrase, guessed)
                print('Guessed: {}'.format(','.join(guessed)))
                print('Category is {}: '.format(category))
                print(obscuredPhrase)
                print('Spin: {}'.format(wheelPrize['text']))

                print(player)
                print('='*40)

                while True:
                    if player.computer:
                        guess = player.computer.getMove(player.prizeMoney, category, obscuredPhrase, guessed, wheelPrize)
                    else:
                        guess = input('Enter your guess: ').upper()
                    # Check if it's a letter or a phrase
                    if len(guess) == 1:
                        if guess in guessed:
                            print('... {} has already been guessed. Try again'.format(guess))
                        elif not guess.isalnum():
                            print('... {} is not a letter. Try again'.format(guess))
                        else:
                            if guess in VOWELS:
                                if player.prizeMoney < VOWEL_COST:
                                    print ('...Need at least ${}. Try again.'.format(VOWEL_COST))
                                    continue
                                else:
                                    player.prizeMoney -= VOWEL_COST
                            numCor = guessChar(phrase, guess, guessed)
                            guessed.append(guess)
                            player.addMoney(wheelPrize['value']*numCor)
                            if wheelPrize['prize']:
                               player.addPrize(wheelPrize['prize'])
                            break
                    elif len(guess) == 0: # invalid
                        print ('... Not a valid guess. Try again')
                    else: # phrase
                        if guess == "PASS":
                            print ('= {} passes ='.format(player.name))
                            break
                        if guess == phrase:
                            printWinnings(player)
                        else:
                            print('{} is not the phrase'.format(guess))
                            break
                break
            elif wheelPrize['type'] == 'bankrupt':
                print('= {} spins bankrupt =\n'.format(player.name))
                player.goBankrupt()
                break
            elif wheelPrize['type'] == 'loseturn':
                print('= {} loses a turn = \n'.format(player.name))
        playerIndex += 1
        playerIndex = playerIndex%len(players)
        player = players[playerIndex]
        print ('...{} spins...\n'.format(player.name))

playGame()
