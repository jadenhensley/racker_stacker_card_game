import random
import copy
import os
import time
import curses
from curses import wrapper

def clearScreen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def get_config_speed():
    words = []
    with open("./config/speed.txt") as f:
        lines = f.readlines()
        # print(lines)
        if len(lines) > 0:
            for n, line in enumerate(lines):
                [words.append(i) for i in line.split()]
    if len(words) >= 3:
        if words[0] == "speed":
            if words[1] == "is":
                return words[2]

def get_config_players():
    players = []
    playerOne, playerTwo, playerThree, playerFour = None, None, None, None
    with open("./config/players.txt") as f:
        lines = f.readlines()
        if len(lines) > 0:
            for n, line in enumerate(lines):
                line = line.strip("\n")
                if n == 0:
                    playerOne = line
                if n == 1:
                    playerTwo = line
                if n == 2:
                    playerThree = line
                if n == 3:
                    playerFour = line
    for player in [playerOne, playerTwo, playerThree, playerFour]:
        if player != None:
            players.append(player)

    return players

class Cards:
    def __init__(self):
        self.cards = []
        self.stack = []
        self.max = 0

    def generate_cards(self, max=60):
        if max % 4 == 0:
            cards = []
            for i in range(max):
                cards.append(i+1)
            self.cards = copy.deepcopy(cards)

            self.max = max
      
            return cards
        else:
            print("ERROR: number of cards must be multiple of 4.")
      
            return -1

    def shuffle_cards(self):
        shuffled = copy.deepcopy(self.cards)

        max = len(shuffled)

        for i in range(max):
            
            randomNumberA = random.randint(0,max-1)
            randomNumberB = random.randint(0,max-1)
            
            if randomNumberA != randomNumberB:
                
                tempA = shuffled[randomNumberA]
                tempB = shuffled[randomNumberB]
                
                shuffled[randomNumberA] = tempB
                shuffled[randomNumberB] = tempA

        self.cards = copy.deepcopy(shuffled)
        return shuffled

    def give_deck_cards(self, deck):
        for i in range(deck.size):
            deck.cards.append(self.cards.pop(-1))

    def put_card_in_stack(self, card):
        self.stack.append(card)
    
    def time_to_shuffle(self):
        arrayCopy = copy.deepcopy(self.stack)
        for i in arrayCopy:
            self.cards.append(i)

        self.shuffle_cards()
        self.stack.clear()

    def pull_card_from_cards(self):
        return self.cards.pop(-1)
    
    def pull_card_from_stack(self):
        return self.stack.pop(-1)

class Player:
    def __init__(self, cards, name, id, is_AI=False):
        self.cards = cards
        self.name = name
        self.id = id
        self.deck = Deck(self, self.cards)
        self.is_AI = is_AI

    def set_name(self, name):
        self.name = name

class Deck:
    def __init__(self, player, cards, size=10):
        self.player = player
        self.cards = []
        self.size = size
        cards.give_deck_cards(self)

class Game:
    def __init__(self, wrapper, cardsMaxAmount=60):
        self.wrapper = wrapper

        self.cards = Cards()

        self.cards.generate_cards()
        self.cards.shuffle_cards()

        self.playerOne = None
        self.playerTwo = None
        self.playerThree = None
        self.playerFour = None

        self.players = [self.playerOne, self.playerTwo, self.playerThree, self.playerFour]

        self.playerChoiceInput = None
        self.slotChosenInput = None

        self.cardPulled = None
        self.cardToSwap = None

        self.cardsInitiated = False
        self.playerOneInitialized = False
        self.playerTwoInitialized = False
        self.playerThreeInitialized = False
        self.playerFourInitialized = False

        self.gameInitialized = False
        self.gameStarted = False
        self.gameIsOver = False
        self.gameIsWon = False
        self.playerWhoWon = None
        self.shuffleCards = False

        self.names_taken = []
        self.names_ai = ["roberto","timmy","jimmy","john","adam","karen","billy","joel","bruce","springsteen","tyler","childers","zach","bryan","riley","harambe","shiba","doge","prime","evan","tony","kevin","ken"]

        self.speedText = "normal"

        self.introASCII = """
 _____            _             _____ _             _              
 |  __ \          | |           / ____| |           | |            
 | |__) |__ _  ___| | _____ _ _| (___ | |_ __ _  ___| | _____ _ __ 
 |  _  // _` |/ __| |/ / _ \ '__\___ \| __/ _` |/ __| |/ / _ \ '__|
 | | \ \ (_| | (__|   <  __/ |  ____) | || (_| | (__|   <  __/ |   
 |_|__\_\__,_|\___|_|\_\___|_|_|_____/ \__\__,_|\___|_|\_\___|_|   
  / ____|            | |  / ____|                                  
 | |     __ _ _ __ __| | | |  __  __ _ _ __ ___   ___              
 | |    / _` | '__/ _` | | | |_ |/ _` | '_ ` _ \ / _ \             
 | |___| (_| | | | (_| | | |__| | (_| | | | | | |  __/             
  \_____\__,_|_|  \__,_|  \_____|\__,_|_| |_| |_|\___|             
                                                                   
                                                                   
-GAME MADE BY @jadenhensley (GitHub) / @hensleycoding (Twitter)      
        
        Must configure game settings using the files in config
        -If confused, read the README for help.

           --type in "start" to begin game!--                          
                                                                   
                                                                   
                                                                   """
        self.gameStartASCII = """

   _____                         _____ _             _   _ _ _ 
  / ____|                       / ____| |           | | | | | |
 | |  __  __ _ _ __ ___   ___  | (___ | |_ __ _ _ __| |_| | | |
 | | |_ |/ _` | '_ ` _ \ / _ \  \___ \| __/ _` | '__| __| | | |
 | |__| | (_| | | | | | |  __/  ____) | || (_| | |  | |_|_|_|_|
  \_____|\__,_|_| |_| |_|\___| |_____/ \__\__,_|_|   \__(_|_|_)
                                                               
                                                               """
        self.gameWinASCII = """
 __     __          __          ___       _ 
 \ \   / /          \ \        / (_)     | |
  \ \_/ /__  _   _   \ \  /\  / / _ _ __ | |
   \   / _ \| | | |   \ \/  \/ / | | '_ \| |
    | | (_) | |_| |    \  /\  /  | | | | |_|
    |_|\___/ \__,_|     \/  \/   |_|_| |_(_)
                                            
                                  
                                             """

    def generate_player_with_random_name(self, player_slot):
        name = random.choice(self.names_ai)
        nameIsValid = False
        while not nameIsValid:
            if name not in self.names_taken:
                self.names_taken.append(name)
                player = Player(self.cards, name, player_slot, False)
                nameIsValid = True
            else:
                name = random.choice(self.names_ai)
        return player

    def initialize_game(self, playerNames, speedText):
        if not self.gameInitialized:
            if 1 <= len(playerNames) <= 4:
                for i in range(len(playerNames)):
                    if i == 0:
                        self.playerOne = Player(self.cards, playerNames[i], i+1)
                        self.playerOneInitialized = True
                    if i == 1:
                        self.playerTwo = Player(self.cards, playerNames[i], i+1)
                        self.playerTwoInitialized = True
                    if i == 2:
                        self.playerThree = Player(self.cards, playerNames[i], i+1)
                        self.playerThreeInitialized = True
                    if i == 3:
                        self.playerFour = Player(self.cards, playerNames[i], i+1)
                        self.playerFourInitialized = True

            if not self.playerOneInitialized:
                self.playerOne = self.generate_player_with_random_name(1)
                self.playerOne.is_AI = True
                self.playerOneInitialized = True
            
            if not self.playerTwoInitialized:
                self.playerTwo = self.generate_player_with_random_name(2)
                self.playerTwo.is_AI = True
                self.playerTwoInitialized = True

            if not self.playerThreeInitialized:
                self.playerThree = self.generate_player_with_random_name(3)
                self.playerThree.is_AI = True
                self.playerThreeInitialized = True
            
            if not self.playerFourInitialized:
                self.playerFour = self.generate_player_with_random_name(4)
                self.playerFour.is_AI = True
                self.playerFourInitialied = True

        self.players = [self.playerOne, self.playerTwo, self.playerThree, self.playerFour]
        self.speedText = speedText

        self.gameInitialized = True

    def check_for_win_condition(self, player):
        max = player.deck.size

        countIsGreater = 0

        iterable = 0

        # player.deck.cards = [0,1,2,3,4,5,6,7,8,9]

        while iterable < max:
            current = player.deck.cards[iterable]
            if iterable > 0:
                previous = player.deck.cards[iterable-1]
                if current > previous:
                    countIsGreater += 1
            iterable += 1
        
        if countIsGreater == max-1:
            print("player should be winning")
            if self.playerWhoWon == None:
                self.playerWhoWon = player
            self.gameIsWon = True
            self.gameIsOver = True
            return True
        else:
            return False

    def run(self):
        while self.gameInitialized and not self.gameIsOver:
            if not self.gameStarted:
                clearScreen()
                print(self.introASCII)
                inputIsValid = False
                while not inputIsValid:
                    i = input("\nprompt: \n->")
                    if i == "start":
                        inputIsValid = True
                self.gameStarted = True
            else:
                while not self.gameIsOver:
                    clearScreen()
                    print(self.gameStartASCII)
                    print(f"Welcome, {self.playerOne.name}")
                    if self.speedText == "normal":
                        time.sleep(2)
                    while not self.gameIsOver:
                        for player in self.players:
                            clearScreen()
                            if self.check_for_win_condition(player):
                                continue
                            print(f"{player.name.capitalize()}'s Turn")
                            if not player.is_AI:
                                print(f"RACK \t CARD \t KEY(NUMPAD)")
                                rack_slots_text = []
                                for i in range(player.deck.size):
                                    n = i+1
                                    num = i
                                    rack_slots_text.append(f"{n*5}: \t {player.deck.cards[i]} \t {num}")
                                for i in range(len(rack_slots_text)):
                                    print(rack_slots_text[-i-1])

                                inputIsValid = False
                                while not inputIsValid:
                                    if len(self.cards.cards) > 0:
                                        if len(self.cards.stack) > 0:
                                            i = input(f'\nThe top card in cards is hidden.\nThe top card in stack is {self.cards.stack[-1]}. \n\nWhat choice are you making, {player.name.capitalize()}? \n(options: "pull from cards","pull from stack") \n->')
                                            if i in ["pull from cards", "pull from stack"]:
                                                self.playerChoiceInput = i
                                                inputIsValid = True
                                            else:
                                                print("Choice not recognized. Try something else.")
                                        else:
                                            i = input(f'\nThe top card in cards is hidden.\nThere is no card in the stack. \n\nWhat choice are you making, {player.name.capitalize()}? \n(options: "pull from cards") \n->')
                                            if i in ["pull from cards"]:
                                                self.playerChoiceInput = i
                                                inputIsValid = True
                                            else:
                                                print("Choice not recognized. Try something else.")
                                    else:
                                        clearScreen()
                                        print(f"\nAll cards have been pulled. Time to shuffle the cards and put them back!\n")
                                        self.playerChoiceInput = "shuffle"
                                        inputIsValid = True
                                if self.speedText == "normal":
                                    time.sleep(1.5)

                                if (self.playerChoiceInput == "shuffle"):
                                    self.shuffleCards = True

                                if self.shuffleCards:
                                    self.cards.time_to_shuffle()
                                    inputIsValid = False
                                    self.shuffleCards = False




                                if self.playerChoiceInput == "pull from cards":
                                    self.cardPulled = self.cards.pull_card_from_cards()
                                if self.playerChoiceInput == "pull from stack":
                                    self.cardPulled = self.cards.pull_card_from_stack()
                                
                                clearScreen()

                                if (self.playerChoiceInput == "pull from cards" or self.playerChoiceInput == "pull from stack"):
                                    print(f"RACK \t CARD \t KEY(NUMPAD)")

                                    for i in range(len(rack_slots_text)):
                                        print(rack_slots_text[-i-1])

                                    if self.playerChoiceInput == "pull from cards":
                                        print(f"\nYOU PULLED A {self.cardPulled} FROM THE CARDS!")
                                    if self.playerChoiceInput == "pull from stack":
                                        print(f"\nYOU PULLED A {self.cardPulled} FROM THE STACK!")

                                    print(f"\nWhich rack slot do you want to put the pulled card in?\n")

                                    inputIsValid = False
                                    while not inputIsValid:
                                        i = input(f"\nrack slot: \n->")
                                        if i in ["0","1","2","3","4","5","6","7","8","9"]:
                                            self.slotChosenInput = i
                                            inputIsValid = True

                                    self.cardToSwap = player.deck.cards[int(self.slotChosenInput)]

                                    self.cards.stack.append(self.cardToSwap)
                                    player.deck.cards[int(self.slotChosenInput)] = self.cardPulled

                                    print(f"Swapping Card {self.cardToSwap} with Card {self.cardPulled}. \nCard {self.cardPulled} is going in slot {self.slotChosenInput}. \nCard {self.cardToSwap} was put on top of the stack.")
                                if self.speedText == "normal":
                                    time.sleep(5)
                            if player.is_AI:
                                print(f"\n{player.name.capitalize()} is making a decision.\n")
                                
                                if len(self.cards.cards) == 0:
                                    self.cards.time_to_shuffle()
                                    print(f"\nCards were shuffled.")
                                if len(self.cards.stack) > 0:
                                    aiChoiceCardsOrStack = random.choice(["cards","stack"])
                                else:
                                    if len(self.cards.cards) > 0:
                                        aiChoiceCardsOrStack = "cards"
                                
                                
                                if aiChoiceCardsOrStack == "cards":
                                    self.cardPulled = self.cards.pull_card_from_cards()
                                    print(f"{player.name.capitalize()} pulled card {self.cardPulled} from cards.")
                                if aiChoiceCardsOrStack == "stack":
                                    self.cardPulled = self.cards.pull_card_from_stack()
                                    print(f"{player.name.capitalize()} pulled card {self.cardPulled} from stack.")


                                aiChoice = random.randint(1,3)
                                aiChoiceSmartOrDumbStrategy = None
                                # 33.33 percent chance to play dumb and make random decision
                                # 66.66 percent chance to play smart and use "rack slot within range" strategy
                                if aiChoice == 1:
                                    aiChoiceSmartOrDumbStrategy = "dumb"
                                if aiChoice == 2 or aiChoice == 3:
                                    aiChoiceSmartOrDumbStrategy = "smart"

                                if aiChoiceSmartOrDumbStrategy == "dumb":
                                    i = random.randint(0,9)
                                    self.cardToSwap = player.deck.cards[i]
                                    self.cards.stack.append(self.cardToSwap)
                                    player.deck.cards[i] = self.cardPulled
                                if aiChoiceSmartOrDumbStrategy == "smart":
                                    subranges = []
                                    for i in range(player.deck.size):
                                        subranges.append((i+1)*5)
                                    
                                    iterable = 0
                                    while iterable < len(subranges):
                                        if iterable != len(subranges)-1:
                                            
                                            if subranges[iterable] <= self.cardPulled <= subranges[iterable+1]:
                                                self.slotChosenInput = iterable
                                            if (iterable == 0) and (self.cardPulled <= subranges[iterable]):
                                                self.slotChosenInput = iterable

                                        if iterable >= len(subranges)-1:
                                            if self.cardPulled >= subranges[iterable]:
                                                self.slotChosenInput = iterable
                                        iterable += 1
                                    
                                    self.cardToSwap = player.deck.cards[int(self.slotChosenInput)]
                                    self.cards.stack.append(self.cardToSwap)
                                    player.deck.cards[int(self.slotChosenInput)] = self.cardPulled

                                print(f"\n{player.name.capitalize()} swapped card {self.cardToSwap} with card {self.cardPulled}.")

                                if self.speedText == "normal":
                                    time.sleep(2)
        if self.gameIsOver:
            clearScreen()
            if self.gameIsWon:
                print(f"\n Congratulations, {self.playerWhoWon.name}! You won Racker Stacker Card Game!\n")
                print(self.gameWinASCII)

speed = get_config_speed()
players = get_config_players()
print(players)
game = Game(wrapper, 60)
game.initialize_game(playerNames=players, speedText=speed) # up to four players. any empty slots will be made random AI.
# also, can supply speed variable, which is normal by default but can also be instant
game.run()