# Racker Stacker Card Game

# What is it?

This game is a digital card game inspired by the family card game Racko, and is primarily different in that it can be played in the terminal or by yourself against computer AI. (there is also multiplayer support) This is not a true replacement to the physical board game and is less ideal for social events.

- I programmed this game during Thanksgiving Eve 2022 and Thanksgiving Day 2022 (September 23rd -> September 24th, 2022).

The source code of this game is licensed under the "GNU Affero General Public License" described in the LICENSE.md file.

I may revisit this idea in the future and make digital card games in the future, but instead of it being in the terminal it would have a *graphical user interface* as well as have *online multiplayer* or *better graphics*. I also plan to make more terminal based games going forward.

***For more information: please read the section below titled "Notes from Myself"***

# How to Play - Step 0: Configuration

- Before you play, you must have configured the list of players and speed settings by modifying the files included in the "config" directory. 

- speed.txt should look like this if you want normal speed (recommended):

```
speed is normal
```

- speed.txt should look like this if you want instant speed:

```
speed is instant
```

- players.txt should look like this for one player:

```
nameGoesHere
```

- players.txt should look like this for four players:

```
firstNameGoesHere
secondNameGoesHere
thirdNameGoesHere
fourthNameGoesHere
```

- when players.txt is left empty, robot AI's will play the game.

# How to Play - Rules:

- Each player has a turn.

- Each player has a rack of cards.

- At the beginning of the game all 60 cards are shuffled. Each player is then given 10 cards in random order that get put in their "rack"/"deck". The remaining 20 cards are put in the "cards" pile to be pulled from in top-down order.

- On each turn, the player must draw a card either from the cards pile that the game starts with or the cards stack that cards are put in when they get swapped out with the card being pulled.

- When player pulls a card from either pile or stack and assigns it to a slot in the rack, the previous card that was in said slot gets put on top of the cards stack. The player after this one can rely on this and pull from the stack the card that was previously belonging to the previous player.

- When the original "cards" pile is empty, the "stack" pile gets shuffled and put in to the original "cards" pile.

- The player who first has all of the cards in their rack sorted leatest to greatest wins the game! (win condition)

Note:

In this game, the right pile of cards (original cards) and the left pile of cards (stack of swapped cards) are differentiated by the terms "cards" and "stack" respectively.

# Notes from Myself, The Programmer

***Good luck playing and I hope you have lots of fun with this digital card game I programmed! Feel free to look at the source code. -Jaden*** 

Please respect my code license (you must use the GNU Affero GPL License if you use this source code or a derivative of it in another project) and contact me when you want to do anything with this project to change it in any important way. -Jaden

***This game is not a replacement to the equivalent physical card game that is better for playing with family or friends. The code license to this game is only the license for the code, and does not mean I own the "game concept" / "game idea" / "game design" that has originated from another physical card game.***
