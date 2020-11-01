#! /usr/bin/env python3

import argparse
import logging
import random
import sys


# setup python logging for debug at this point
root = logging.getLogger()
root.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler.setFormatter(formatter)

# default values
DEFAULT_NUMBER_OF_PLAYERS = 2
DEFAULT_NUMBER_OF_CARDS_PER_HAND = 3
DEFAULT_SUITS = "diamonds:4,hearts:3,spades:2,clubs:1"
DEFAULT_RANGE_OF_CARDS = 14

# Exceptions

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class KeySortError(Error):
    """Raised by sorting and the specified key is not in the collection of cards """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class ObjectNotFound(Error):
    """Raised when an object is not found where expected"""
    def __init__(self, message):
        self.message = message


# Classes

class Card:
    def __init__(self, suit, suit_value, value):
        self.__card_suit_name = suit
        self.__card_suit_rank = suit_value
        self.__card_value = value

    def __str__(self):
        return 'Card: suit: {:10s} rank: {} value: {:3d}'.format(
            self.__card_suit_name,
            self.__card_suit_rank,
            self.__card_value )

    def get_suit_name(self):
        return self.__card_suit_name

    def get_suit_rank(self):
        return self.__card_suit_rank

    def get_value(self):
        return self.__card_value


class Deck:
    def __init__(self, card_range, suits):
        self.__card_range = card_range
        self.__suits = suits
        self.__stack = []
        for suit in self.__suits.keys():
            for i in range(1,self.__card_range):
                self.__stack.append(Card(suit, self.__suits[suit], i))
        self.shuffle()

    def __str__(self):
        return "Cards/hand: {}, Card/range: {}, Suits: {}".format(self.card_range,self.suits)

    def get_card_range(self):
        return self.__card_range

    def get_suits(self):
        return self.__suits

    def get_deck(self):
        return self.__stack

    def shuffle(self):
        for i in reversed(range(1, len(self.__stack))):
            j = int(random.random() * (i+1))
            self.__stack[i], self.__stack[j] = self.__stack[j], self.__stack[i]

    def get_top_card(self):
        c = self.__stack.pop(0)
        self.__stack.append(c)
        return c

    def sort_cards_by(self, sort_by):
        # get cards seperated by suit
        cards = {}
        for s in self.__suits.keys():
            cards[s] = []

        for c in self.__stack:
            cards[c.get_suit_name()].append(c)

        # sort by card value
        def get_value(c):
            return c.get_value()

        for i in cards.keys():
            cards[i].sort(key=get_value)

        # make sure all the sort_by suits are in the card deck
        # if not raise an exception
        for s in sort_by:
            if s not in cards.keys():
                raise KeySortError('Sort parameter {} is not in available suits {}'.format(s, cards.keys()))

        # now create list order as specified in sort_by
        new_deck = []
        for s in sort_by:
            for c in cards[s]:
                new_deck.append(c)
        self.__stack = new_deck


class Player:
    def __init__(self, cards=[]):
        self.__hand = []
        self.__score = 0

    def hand(self, cards):
        self.__hand = cards

    def get_hand(self):
        return self.__hand

    def score(self, value):
        self.__score = value

    def get_score(self):
        return self.__score

    def zero_score(self):
        self.__score = 0


class Players:
    def __init__(self, number_of_players):
        self.__players = []
        self.__number_of_players = number_of_players
        for i in range(1,self.__number_of_players+1):
            self.__players.append(Player())

    def get_players(self):
        return self.__players

    def get_player(self, idx):
        if -1 < idx < len(self.__players):
            return self.__players[idx]
        raise ObjectNotFound('No object at index {}'.format(idx))

    def get_number_of_players(self):
        return self.__number_of_players


class Game:
    def __init__(self, number_of_players, cards_per_hand):
        self.__num_players = number_of_players
        self.__num_cards_per_hand = cards_per_hand

    def get_num_players(self):
        return self.__num_players

    def get_num_cards_per_hand(self):
        return self.__num_cards_per_hand

    def play(self, deck):
        # d = deck
        # score = []
        # for i in self.get_num_players():


        return 1


def parse_command_line ():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--players', dest='players', help='number of players')
    parser.add_argument('-n', '--number_of_cards', dest='num_of_cards', help='number of cards to play per hand')
    parser.add_argument('-d', '--debug',  action='store_true', dest='debug', help='output debug info')
    parser.add_argument('-l', '--level', dest='logging_level',
                        help='set logging level, values can be CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET')
    parser.add_argument('-r', '--range', dest='range',
                        help='range of numbers to use, default: 14 (that means there are 14 cards)')
    parser.add_argument('-s', '--suits', dest='suits',
                        help='list of suits to use with the value of the suite, default: "diamonds:4,hearts:3,spades:2,clubs:1"')

    options = parser.parse_args()

    if options.logging_level in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']:
        handler.setLevel(options.logging_level)

    return options


def initialize_variables(options):

    players = DEFAULT_NUMBER_OF_PLAYERS
    num_of_cards_per_hand = DEFAULT_NUMBER_OF_CARDS_PER_HAND
    suits = DEFAULT_SUITS
    card_range = DEFAULT_RANGE_OF_CARDS

    if options.players is not None:
        players = options.players
    if options.num_of_cards is not None:
        num_of_cards_per_hand = options.num_of_cards
    if options.range is not None:
        card_range = options.range
    if options.suits is not None:
        suits = options.suits

    card_suits = suits.split(',')
    temp = {}
    for suit in card_suits:
        idx = suit.index(':')
        t = suit[:idx]
        v = suit[idx+1:]
        temp[t] = int(v)

    suits = temp

    if options.debug:
        logging.info('Options:')
        logging.info('\tNumber of players:        {} {}'.format(players,type(players)))
        logging.info('\tNumber of cards per hand: {} {}'.format(num_of_cards_per_hand,type(num_of_cards_per_hand)))
        logging.info('\tSuits:                    {} {}'.format(suits,type(suits)))
        logging.info('\tRange of cards:           {} {}'.format(card_range,type(card_range)))

    d = Deck(int(card_range), suits)
    g = Game(int(players), int(num_of_cards_per_hand))

    return g,d


def main():
    options = parse_command_line()

    game, deck = initialize_variables(options)

    return game.play(deck)


if __name__ == '__main__':
    return_value = main()
    sys.exit(return_value)

# eof

