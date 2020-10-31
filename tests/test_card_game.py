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
        assert options.debug is False
        assert options.logging_level is None
        assert options.num_of_cards is None
        assert options.players is None
        assert options.range is None
        assert options.suits is None

def test_parse_args_debug():
    testargs = ['card_game.py','--debug']
    with patch.object(sys, 'argv', testargs):
        options = card_game.parse_command_line()
        assert options is not None
        assert options.debug is True
        assert options.logging_level is None
        assert options.num_of_cards is None
        assert options.players is None
        assert options.range is None
        assert options.suits is None

def test_parse_args_other_args():

    testargs = ['card_game.py',
                '--debug',
                '--players=2',
                '--number_of_cards=2',
                '--level=DEBUG',
                '--range=15',
                '--suits="diamonds:4,hearts:3,spades:2,clubs:1"']
    with patch.object(sys, 'argv', testargs):
        options = card_game.parse_command_line()
        assert options is not None
        assert options.debug is True
        assert options.logging_level == 'DEBUG'
        assert options.num_of_cards == '2'
        assert options.players == '2'
        assert options.range == '15'
        assert options.suits == "diamonds:4,hearts:3,spades:2,clubs:1"

def test_initialize_variables_default():
    options = SimpleNamespace()
    options.debug = True
    options.logging_level = None
    options.num_of_cards = None
    options.players = None
    options.range = None
    options.suits = None
    d = card_game.initialize_variables(options)
    assert d is not None

def test_initialize_variables_with_options():
    options = SimpleNamespace()
    options.debug = True
    options.logging_level = 'DEBUG'
    options.num_of_cards = '2'
    options.players = '2'
    options.range = '14'
    options.suits = 'diamonds:4,hearts:3,spades:2,clubs:1'

    d = card_game.initialize_variables(options)
    assert d is not None
    assert d.players == 2
    assert d.num_of_cards_per_hand == 2
    assert d.card_range == 14
    assert d.suits == {'diamonds':4,'hearts':3,'spades':2,'clubs':1}

def test_card_default():
    c = card_game.Card('Red',2,10)
    assert c is not None
    assert c.suit_name() == 'Red'
    assert c.suit_value() == 2
    assert c.value() == 10

def test_deck_default():
    d = card_game.Deck(2, 2, 14, {'diamonds':4,'hearts':3,'spades':2,'clubs':1})
    assert d is not None
    assert d.players() == 2
    assert d.num_of_cards_per_hand() == 2
    assert d.card_range() == 14
    assert d.suits() == {'diamonds':4,'hearts':3,'spades':2,'clubs':1}
    assert d.deck() is not None

def test_deck_shuffle():
    d = card_game.Deck(2, 2, 14, {'diamonds':4,'hearts':3,'spades':2,'clubs':1})
    deck = d.deck()
    first_card = deck[0]
    last_card = deck[len(deck)-1]
    d.shuffle()
    first_after_shuffle = deck[0]
    last_after_shuffle = deck[len(deck)-1]
    assert d is not None
    assert first_card != first_after_shuffle
    assert last_card != last_after_shuffle

def test_get_top_card():
    d = card_game.Deck(2, 2, 14, {'diamonds':4,'hearts':3,'spades':2,'clubs':1})
    deck = d.deck()
    first_card = deck[0]
    other = d.get_top_card()
    assert d is not None
    assert first_card == other
