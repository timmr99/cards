#! /usr/bin/env python3

import sys
import pytest
from mock import patch
from types import SimpleNamespace

from cards import card_game

def test_parse_args_defaults():
    testargs = ['card_game.py']
    with patch.object(sys, 'argv', testargs):
        options = card_game.parse_command_line()
        assert options is not None
        assert options.num_of_cards is None
        assert options.players is None
        assert options.range is None
        assert options.suits is None

def test_parse_args_debug():
    testargs = ['card_game.py']
    with patch.object(sys, 'argv', testargs):
        options = card_game.parse_command_line()
        assert options is not None
        assert options.num_of_cards is None
        assert options.players is None
        assert options.range is None
        assert options.suits is None

def test_parse_args_other_args():

    testargs = ['card_game.py',
                '--players=2',
                '--number_of_cards=2',
                '--range=15',
                '--suits=diamonds:4,hearts:3,spades:2,clubs:1']
    with patch.object(sys, 'argv', testargs):
        options = card_game.parse_command_line()
        assert options is not None
        assert options.num_of_cards == '2'
        assert options.players == '2'
        assert options.range == '15'
        assert options.suits == "diamonds:4,hearts:3,spades:2,clubs:1"

def test_initialize_variables_default():
    options = SimpleNamespace()
    options.debug = False
    options.num_of_cards = None
    options.players = None
    options.range = None
    options.suits = None
    d = card_game.initialize_variables(options)
    assert d is not None

def test_initialize_variables_with_options():
    options = SimpleNamespace()
    options.debug = False
    options.num_of_cards = '2'
    options.players = '2'
    options.range = '13'
    options.suits = 'diamonds:4,hearts:3,spades:2,clubs:1'

    g, p, d = card_game.initialize_variables(options)
    assert d is not None
    assert g is not None
    assert p is not None

    assert g.get_num_cards_per_hand() == 2

    assert d.get_card_range() == 13
    assert d.get_suits() == {'diamonds':4,'hearts':3,'spades':2,'clubs':1}
    assert d.get_deck() is not None

    assert p.get_players() is not None

def test_card_default():
    c = card_game.Card('Red',2,10)
    assert c is not None
    assert c.get_suit_name() == 'Red'
    assert c.get_suit_rank() == 2
    assert c.get_value() == 10

def test_card_str():
    c = card_game.Card('Red',2,10)
    test_str = 'Card: suit: {:10s} rank: {} value: {:3d}'.format('Red',2,10)
    assert c.__str__() == test_str

def test_deck_default():
    d = card_game.Deck(14, {'diamonds':4,'hearts':3,'spades':2,'clubs':1})
    assert d is not None
    test_str = "Card/range: {}, Suits: {}".format(14,{'diamonds':4,'hearts':3,'spades':2,'clubs':1})
    assert d.__str__() == test_str

def test_deck_shuffle():
    d = card_game.Deck(14, {'diamonds':4,'hearts':3,'spades':2,'clubs':1})
    deck = d.get_deck()
    first_card = deck[0]
    last_card = deck[len(deck)-1]
    d.shuffle()
    first_after_shuffle = deck[0]
    last_after_shuffle = deck[len(deck)-1]
    assert d is not None
    assert first_card != first_after_shuffle
    # sometime, with a random shuffle, the last card is still the last card
    if last_card != last_after_shuffle:
        assert last_card != last_after_shuffle

def test_get_top_card():
    d = card_game.Deck(14, {'diamonds':4,'hearts':3,'spades':2,'clubs':1})
    deck = d.get_deck()
    first_card = deck[0]
    other = d.get_top_card()
    assert d is not None
    assert first_card == other


def test_sort_cards_by():
    d = card_game.Deck(14, {'diamonds':4,'hearts':3,'spades':2,'clubs':1})
    result = d.sort_cards_by(['clubs', 'spades', 'hearts', 'diamonds'])
    assert result is True
    deck = d.get_deck()
    first_card = deck[0]
    assert d is not None
    assert first_card.get_suit_name() == 'clubs'
    assert first_card.get_suit_rank() == 1
    assert first_card.get_value() == 1

    result = d.sort_cards_by(['green'])
    assert result == False

def test_player_default():
    p = card_game.Player()
    assert p is not None
    test_hand = [card_game.Card('hearts',3,10), card_game.Card('hearts',3,11)]
    p.hand(test_hand)
    assert p.get_hand() == test_hand
    p.score(2)
    assert p.get_score() == 2

def test_players():
    p = card_game.Players(2)
    assert p is not None
    assert p.get_number_of_players() == 2
    assert len(p.get_players()) == 2
    assert p.get_player(0) is not None

    result = p.get_player(99)
    assert result is not False

def test_game_init():
    options = SimpleNamespace()
    options.debug = True
    options.num_of_cards = '2'
    options.players = '2'
    options.range = '13'
    options.suits = 'diamonds:4,hearts:3,spades:2,clubs:1'
    g,p,d = card_game.initialize_variables(options)

    assert g is not None
    assert g.get_num_cards_per_hand() == 2

    assert d is not None
    assert d.get_card_range() == 13
    assert d.get_suits() == {'diamonds':4, 'hearts':3, 'spades':2, 'clubs':1}
    assert d.get_deck() is not None

    assert p is not None
    assert p.get_number_of_players() == 2

def test_game_play():
    options = SimpleNamespace()
    options.debug = False
    options.num_of_cards = '2'
    options.players = '2'
    options.range = '13'
    options.suits = 'diamonds:4,hearts:3,spades:2,clubs:1'
    g,p,d = card_game.initialize_variables(options)

    g.play(p,d)

def test_game_play_3_players():
    options = SimpleNamespace()
    options.debug = False
    options.num_of_cards = '2'
    options.players = '3'
    options.range = '13'
    options.suits = 'diamonds:4,hearts:3,spades:2,clubs:1'
    g,p,d = card_game.initialize_variables(options)

    g.play(p,d,True)

def test_game_play_red_white_blue():
    options = SimpleNamespace()
    options.debug = True
    options.num_of_cards = '2'
    options.players = '2'
    options.range = '3'
    options.suits = 'red:4,white:3,blue:2'
    g,p,d = card_game.initialize_variables(options)

    g.play(p,d,True)






# eos
