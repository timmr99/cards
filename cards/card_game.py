#! /usr/bin/env python3
"""
This program is a card game similar to the game of war
(https://en.wikipedia.org/wiki/War_(card_game)) in that each player draws two cards and accumulates
the score for each hand. The scoring is the suit rank times the card value. For example, with a suit
rank of 4 and a card value of 10, the score of the card is 40. The total score is done after all
cards are drawn.
"""

import argparse
import random
import sys

# default values
DEFAULT_NUMBER_OF_PLAYERS = 2
DEFAULT_NUMBER_OF_CARDS_PER_HAND = 3
DEFAULT_SUITS = "diamonds:4,hearts:3,spades:2,clubs:1"
DEFAULT_RANGE_OF_CARDS = 14

# get some names for the players, cannot stand to not have names
NAMES = ['Liam', 'Amelia', 'Olivia', 'Noah', 'Emma', 'Oliver', 'Ava', 'William', 'Sophia',
         'Elijah', 'Isabella', 'James', 'Charlotte', 'Benjamin', 'Amelia', 'Lucas', 'Amelia',
         'Mia', 'Mason', 'Harper', 'Ethan', 'Evelyn' ]


# Classes

class Card:
    """
    This class represents a card for this game

    ...

    Attributes
    ----------
    __card_suit_name: str
        the name of the suit this card represents

    __card_suit_rank: int
        the rank of the suit, used in score calculations

    __card_value: int
        the face value of the card

    Methods
    -------
    get_suit_name()
        returns the suit name

    get_suit_rank()
        returns the suit rank

    get_value()
        returns the value of the card

    """
    def __init__(self, suit, suit_value, value):
        """
        Parameters
        ----------
        suit: str
            the suit name for this card

        suit_value: int
            the suit ranke for this card

        value: int
            card's face value

        """
        self.__card_suit_name = suit
        self.__card_suit_rank = suit_value
        self.__card_value = value

    def __str__(self):
        """
        Returns string representation of this card
        """
        return 'Card: suit: {:10s} rank: {} value: {:3d}'.format(
            self.__card_suit_name,
            self.__card_suit_rank,
            self.__card_value )

    def get_suit_name(self):
        """
        Returns the card's suit name
        """
        return self.__card_suit_name

    def get_suit_rank(self):
        """
        Returns the card's suit's rank
        """
        return self.__card_suit_rank

    def get_value(self):
        """
        Returns the card's value
        """
        return self.__card_value


class Deck:
    """
    This class represents the deck for the game.

    ...

    Attributes
    ----------
    __card_range: int
        the range of the cards to use, it represents the cards from 1 to __card_range

    __suits: str
        the suits and suit rank to use for the deck.

    __stack: list
        the actual deck, a list of cards

    Methods
    -------
    get_card_range:
        returns the __card_range value

    get_suits:
        returns the __suits value

    get_deck:
        returns the __stack

    """
    def __init__(self, card_range, suits):
        """
        Parameters
        ----------
        card_range: int
            the value for __card_range

        suits: str
            the card suits and rank to use for the cards
        """
        self.__card_range = card_range
        self.__suits = suits
        self.__stack = []
        for suit in self.__suits.keys():
            for i in range(1,self.__card_range+1):
                self.__stack.append(Card(suit, self.__suits[suit], i))
        self.shuffle()

    def __str__(self):
        """
        Returns the string representation for the Deck
        """
        return "Card/range: {}, Suits: {}".format(
            self.__card_range,self.__suits)

    def get_card_range(self):
        """
        Return the value of __card_range
        """
        return self.__card_range

    def get_suits(self):
        """
        Return the value of __suits
        """
        return self.__suits

    def get_deck(self):
        """
        Return the value of __stack
        """
        return self.__stack

    def shuffle(self):
        """
        Does a random shuffle on the deck
        """
        for i in reversed(range(1, len(self.__stack))):
            j = int(random.random() * (i+1))
            self.__stack[i], self.__stack[j] = self.__stack[j], self.__stack[i]

    def get_top_card(self):
        """
        Get the top card off the stack, watching out for an empty deck. If the
        deck doesn't contain any more cards, return None
        """
        stack_size = len(self.__stack)
        if stack_size == 0:
            return None
        c = self.__stack.pop(0)
        return c

    def sort_cards_by(self, sort_by):
        """
        Sorts the cards in the order specified by sort_by

        Parameters
        ----------
        sort_by: list of str, required
            A list of suits that specifies what order to sort the deck. The
            sorted cards are also sorted by card value

        """
        cards = {}
        # get the suits to order the deck by
        for s in self.__suits.keys():
            cards[s] = []

        # split the deck into entries in a dict, the key is the suit
        # and the contents of the entry are the cards of the suita
        for c in self.__stack:
            cards[c.get_suit_name()].append(c)

        # subfunction for sorting by card value
        def get_value(c):
            return c.get_value()

        # sort the cards
        for i in cards.keys():
            cards[i].sort(key=get_value)

        # make sure all the sort_by suits are in the card deck
        # if not return False
        for s in sort_by:
            if s not in cards.keys():
                return False

        # now create list order as specified in sort_by
        new_deck = []
        for s in sort_by:
            for c in cards[s]:
                new_deck.append(c)
        # and assign it back to the stack
        self.__stack = new_deck

        return True


class Player:
    """
    This class represents a game player

    ...

    Attributes
    ----------
    __hand: list
        the last hand drawn by the player

    __score: int
        the cummulative score for the player

    __id: str
        the player's name

    Methods
    -------
    get_id:
        returns the players id/name

    hand:
        sets the current value of __hands

    get_hand:
        returns the value of __hands

    score:
        sets the value of __score

    get_score:
        returns the value of __score

    score_hand(hand):
        scores the specified hand of cards

    """

    def __init__(self):
        self.__hand = []
        self.__score = 0
        self.__id = random.choice(NAMES)

    def get_id(self):
        """
        return the player's name
        """
        return self.__id

    def hand(self, cards):
        """
        set the current player's hand
        """
        self.__hand = cards

    def get_hand(self):
        """
        return the current hand
        """
        return self.__hand

    def score(self, value):
        """
        set the current score
        """
        self.__score = value

    def get_score(self):
        """
        return the current score
        """
        return self.__score

    def score_hand(self, hand):
        """
        Score the specified hand of cards

        The score is the cummulative score of all cards. A card's score
        is the value of the suit's rank multiplied by the value of the
        card
        """
        score = 0
        for card in hand:
            rank = card.get_suit_rank()
            value = card.get_value()
            score += rank * value
        self.__score += score
        self.__hand = hand

class Players:
    """
    This class represents the game players

    ...

    Attributes
    ----------
    __players: list of Players
        list of the current players

    __number_of_players: int
        the number of players for the current game

    Methods
    -------
    get_players():
        sets the list of players

    get_player(idx):
        return the player at the specified index

    get_number_of_players():
        returns the value of __number_of_players
    """

    def __init__(self, number_of_players):
        """
        Parameters
        ----------
        number_of_players: int
            number of players in the game
        """
        self.__players = []
        self.__number_of_players = number_of_players
        for i in range(1,self.__number_of_players+1):
            self.__players.append(Player())

    def get_players(self):
        """
        Returns the list of players
        """
        return self.__players

    def get_player(self, idx):
        """
        Returns the player at specified index. If the index is out of
        range return None
        """
        if -1 < idx < len(self.__players):
            return self.__players[idx]
        return None

    def get_number_of_players(self):
        """
        Return the number of players
        """
        return self.__number_of_players


class Game:
    """
    This class represents the actual game and contains the logic for it

    Attributes
    ----------
    __num_cards_per_hand: int
        the number of cards to draw for a hand

    Methods
    -------

    get_num_cards_per_hand:
        returns the number of cards to use in a hand

    play:
        play the game

    """
    def __init__(self, cards_per_hand):
        """
        Attributes
        ----------
        cards_per_hand:
            the number of cards to use in a hand
        """
        self.__num_cards_per_hand = cards_per_hand

    def get_num_cards_per_hand(self):
        """
        Returns the number of cards to use in a hand
        """
        return self.__num_cards_per_hand

    def play(self, players, deck, debug=False):
        """
        play the game. The game's logic is that each player draws the
        number of cards to be used in  a hand. Each hand is individually
        scored. The game is played until all cards have been drawn.
        """
        d = deck
        p = players

        # play game. Each player draws the specified number of cards
        # by talking the cards off the top of the deck. Once the deck
        # is empty, leave the draw cards loop and score the hand
        done = False
        iterations = 0
        while not done:
            for player in p.get_players():
                hand = []
                if debug:
                    print(40 * '-')
                    print('{} Playing: {}'.format(iterations, player.get_id()))
                    iterations += 1
                counter = 0
                for i in range(1,self.get_num_cards_per_hand()+1):
                    card = deck.get_top_card()
                    if not card:
                        done = True
                        break
                    if debug:
                        print('\t{} card:{} rank:{} value:{}'.format(counter,
                                                    card.get_suit_name(),
                                                    card.get_suit_rank(),
                                                    card.get_value()))
                        counter += 1
                    hand.append(card)
                player.score_hand(hand)
                if debug:
                    print('\tScore {}'.format(player.get_score()))
            if done: break
        # score the game and determine the winner
        if debug: print('Scoring...')
        max_score = 0
        max_id = 0

        for player in p.get_players():
            score = player.get_score()
            if debug:
                print('Score for {} is {}'.format(player.get_id(), score))
            if score > max_score:
                max_score = player.get_score()
                max_id = player.get_id()

        print('Game won by {} with a score of {}'.format(max_id, max_score))
        return


def parse_command_line ():
    """
    Parse the command line. There are enough arguments to define the
    total parapeters for the game
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--players', dest='players', help='number of players')
    parser.add_argument('-n', '--number_of_cards', dest='num_of_cards', help='number of cards to play per hand')
    parser.add_argument('-d', '--debug',  action='store_true', dest='debug', help='output debug info')
    parser.add_argument('-r', '--range', dest='range',
                        help='range of numbers to use, default: 13')
    parser.add_argument('-s', '--suits', dest='suits',
                        help='list of suits to use with the value of the suite, default: "diamonds:4,hearts:3,spades:2,clubs:1"')

    options = parser.parse_args()

    return options


def initialize_variables(options):
    """
    Initialize the game's variables and create thet game, players and card deck
    """
    # set the games defaults
    players = DEFAULT_NUMBER_OF_PLAYERS
    num_of_cards_per_hand = DEFAULT_NUMBER_OF_CARDS_PER_HAND
    suits = DEFAULT_SUITS
    card_range = DEFAULT_RANGE_OF_CARDS

    # check to see if any of the defaults are to be overridden
    if options.players is not None:
        players = options.players
    if options.num_of_cards is not None:
        num_of_cards_per_hand = options.num_of_cards
    if options.range is not None:
        card_range = options.range
    if options.suits is not None:
        suits = options.suits

    # convert the input suit string to a dictionary
    card_suits = suits.split(',')
    temp = {}
    for suit in card_suits:
        idx = suit.index(':')
        t = suit[:idx]
        v = suit[idx+1:]
        temp[t] = int(v)

    suits = temp

    if options.debug:
        print('Options:')
        print('\tNumber of players:        {} {}'.format(players,type(players)))
        print('\tNumber of cards per hand: {} {}'.format(num_of_cards_per_hand,type(num_of_cards_per_hand)))
        print('\tSuits:                    {} {}'.format(suits,type(suits)))
        print('\tRange of cards:           {} {}'.format(card_range,type(card_range)))

    # Create the components and return them
    g = Game(int(num_of_cards_per_hand))
    p = Players(int(players))
    d = Deck(int(card_range), suits)

    return g,p,d


def main():
    options = parse_command_line()
    game, players, deck = initialize_variables(options)
    game.play(players, deck, options.debug)


if __name__ == '__main__':
    main()
    quit()

# eof

