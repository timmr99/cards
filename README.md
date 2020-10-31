`# Card Game for Essex Interview

## Problem Statement

Code interview question: Work with the programing language you are most familiar with.

Create a card game which supports 3 of the operations below.
1.	Shuffle cards in the deck: randomly mix the cards in the card deck, and return a whole deck of cards with a mixed order
2.	Get a card from the top of the deck: get one card from top of the card deck, return a card, and if there is no card left in the deck return error or exception. 
3.	Sort cards: take a list of color as parameter and sort the card in that color order. Numbers should be in ascending order. 
    i.e. If the deck has a card contains with following order  (red, 1), (green, 5), (red, 0), (yellow, 3), (green, 2)
    Sort cards([yellow, green, red]) will return the cards with following order (yellow, 3), (green, 0), (green, 5), (red, 0), (red, 1) 
4.	Determine winners: 2 players play the game. They will draw 3 cards by taking turns.

Whoever has the high score wins the game. (color point calculation, red = 3, yellow =2, green = 1) the point is calculated by color point * number in the card.  

Testing: Create test cases to test the above operations.

Please put the code in an online repository and provide the link before the interview: github, gitlab, etc.

## Solution

* Built using Python 3.8.5

* Create card class ✅

* Create deck class ✅
  * takes a list of card colors or suits and number of cards

* Methods
  * shuffle - shuffle deck of cards, return deck
  * get_top_card - return top card of the current deck, return top card or if no cards, throw exception
  * sort_cards(sort_by) - Sorts deck by colors listed in sort_by
    * sort by the colors specified, then numerically
  * score_hand - score a hand of cards (1-n cards), returns score of hand
    * point is calculated by taking card color point (red=3, yellow=2, green=1) times the number on the cards
  * play = play a game of cards
    * Whoever has the high score wins the game  .
    * play by drawing three cards, calculate each hands score

# Things to do next
* Contine writing tests
* Flesh out objects
* Flesh out play
* Document!!

# Record of time spent on project

* 10/29/2020 - 2 hours
* 10/30/2020 - 3 hours
* 10/31/2020 - 1245
