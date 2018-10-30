#!/usr/bin/env python3
"""Blackjack game."""

import random
from time import sleep


class Card:
    def __init__(self, id):
        if id < 0 or type(id) != int:
            raise ValueError('Card id should be non-negative integer.')

        self.id = id
        self._set_info(id)

    def _set_info(self, id):
        suit, rank = divmod(id, 13)

        if suit % 4 == 0:
            card_name = 'Spade '
        elif suit % 4 == 1:
            card_name = 'Club '
        elif suit % 4 == 2:
            card_name = 'Heart '
        elif suit % 4 == 3:
            card_name = 'Diamond '

        rank += 1
        if rank == 1:
            card_name += 'A'
            card_point = [1, 11]
        elif rank == 11:
            card_name += 'J'
            card_point = [10, 10]
        elif rank == 12:
            card_name += 'Q'
            card_point = [10, 10]
        elif rank == 13:
            card_name += 'K'
            card_point = [10, 10]
        else:
            card_name += str(rank)
            card_point = [rank, rank]

        self.name = card_name
        self.point = card_point


class Deck:
    def __init__(self, num_deck):
        self._num_deck = num_deck
        self._initialize()

    def _initialize(self):
        self._cards = list(range(52*self._num_deck))
        self.num_cards = 52*self._num_deck

    def get_id(self):
        id = random.choice(self._cards)
        self._cards.remove(id)
        self.num_cards -= 1
        return id

    def refresh(self):
        self._cards.clear()
        self._initialize()


class Player:
    def __init__(self, name):
        self.name = name[:7]
        self._initialize()

    def _initialize(self):
        self._hold_ids = []
        self.hold_cards = []
        self._point = [0, 0]
        self.stat = None

    def draw_card(self, id):
        self._hold_ids.append(id)
        card = Card(id)
        self.hold_cards.append(card.name)
        self._point = [x + y for (x, y) in zip(self._point, card.point)]

    def get_point(self):
        points = list(set(self._point))
        if max(points) > 21:
            points = [min(points)]
        return sorted(points)

    def refresh(self):
        self._hold_ids.clear()
        self.hold_cards.clear()
        self._point.clear()
        self._initialize()


class Blackjack:
    def __init__(self, player_name):
        self.deck = Deck(1)
        self.player = Player(player_name)
        self.dealer = Player('Dealer')
        self.num_win = 0
        self.num_loose = 0
        self.num_draw = 0

    def _refresh(self):
        self.deck.refresh()
        self.dealer.refresh()
        self.player.refresh()

    def _draw(self, player, num_card):
        for i in range(num_card):
            player.draw_card(self.deck.get_id())

    def _check_points(self, player):
        player_points = player.get_point()
        if min(player_points) > 21:
            player.stat = 'bust'
        elif 21 in player_points:
            player.stat = 'blackjack'

    def _show_hold_cards(self, player, card_open):
        if card_open:
            cards_list = ['[' + '{:^10}'.format(x) + ']'
                          for x in player.hold_cards]
            if len(cards_list) <= 4:
                cards = ' '.join(cards_list)
                print('{:>7}: {}'.format(player.name, cards))
            else:
                cards = ' '.join(cards_list[:4])
                print('{:>7}: {}'.format(player.name, cards))
                for i in range(len(cards_list) // 4):
                    i += 1
                    cards = ' '.join(cards_list[4*i:4*(i+1)])
                    print(' '*9 + '{}'.format(cards))
            points_list = [str(x) for x in player.get_point()]
            points = ' or '.join(points_list)
            print(' '*9 + '<{} points>'.format(points))
            if player.stat == 'blackjack':
                print(' '*9 + '--> Blackjack!')
            elif player.stat == 'bust':
                print(' '*9 + '--> Bust!')
        else:
            cards = '[{:^10}] [{:^10}]'.format(player.hold_cards[0], '')
            print('{:>7}: {}'.format(player.name, cards))

    def _player_win(self, first):
        if type(first) != bool:
            raise TypeError

        print('You win!')
        self.num_win += 1

    def _player_loose(self):
        print('You loose.')
        self.num_loose += 1

    def _player_draw(self):
        print('Draw')
        self.num_draw += 1

    def first_draw(self):
        self._refresh()
        self._draw(self.dealer, 2)
        self._draw(self.player, 2)

        self._check_points(self.dealer)
        self._check_points(self.player)
        self._show_hold_cards(self.dealer, False)
        self._show_hold_cards(self.player, True)
        print()

    def dealer_draw(self):
        points = self.dealer.get_point()
        while max(points) < 17:
            self._draw(self.dealer, 1)
            points = self.dealer.get_point()

    def hit(self):
        self._draw(self.player, 1)
        self._check_points(self.player)
        self._show_hold_cards(self.player, True)
        print()

    def show_results(self):
        self._check_points(self.dealer)
        self._show_hold_cards(self.dealer, True)
        print()
        sleep(0.5)

        pstat = self.player.stat
        ppoint = max(self.player.get_point())
        dstat = self.dealer.stat
        dpoint = max(self.dealer.get_point())
        if ppoint == dpoint:
            self._player_draw()
        elif pstat == 'blackjack' and dstat != 'blackjack':
            self._player_win(False)
        elif pstat != 'blackjack' and dstat == 'blackjack':
            self._player_loose()
        elif pstat == 'bust' and dstat != 'bust':
            self._player_loose()
        elif pstat != 'bust' and dstat == 'bust':
            self._player_win(False)
        elif ppoint > dpoint:
            self._player_win(False)
        elif ppoint < dpoint:
            self._player_loose()
        print()


def ask_action():
    ans = input('Hit or Stand? (h/s [s]) ')
    print()
    ans = ans.lower()
    if len(ans) == 0:
        return False
    elif ans.startswith('h'):
        return True
    elif ans.startswith('s'):
        return False
    else:
        raise ValueError()


def main():
    print('-------------------------------------------------------------')
    print('     ____  _        _    ____ _  __   _   _    ____ _  __')
    print('    | __ )| |      / \\  / ___| |/ /  | | / \\  / ___| |/ /')
    print("    |  _ \\| |     / _ \\| |   | ' /_  | |/ _ \\| |   | ' /")
    print('    | |_) | |___ / ___ \\ |___| . \\ |_| / ___ \\ |___| . \\')
    print('    |____/|_____/_/   \\_\\____|_|\\_\\___/_/   \\_\\____|_|\\_\\')
    print('-------------------------------------------------------------')
    sleep(0.5)

    game_continue = True
    yesl = ['y', 'yes', '']
    nol = ['n', 'no', 'q', 'quit']
    play = Blackjack('You')
    while game_continue:
        play.first_draw()
        if (play.player.stat != 'blackjack'):
            hit = ask_action()
        if (play.player.stat != 'blackjack'
           and play.dealer.stat != 'blackjack'):
            while hit:
                play.hit()
                if play.player.stat is not None:
                    break
                hit = ask_action()
            if play.player.stat != 'bust':
                play.dealer_draw()
        sleep(0.5)
        play.show_results()
        ans = input('Continue? (y/n [y]) ').lower()
        if ans in yesl:
            game_continue = True
        elif ans in nol:
            game_continue = False
        else:
            raise ValueError()
        print('-'*61)
    num_match = play.num_win + play.num_loose + play.num_draw
    win_ratio = 100 * play.num_win / num_match
    loose_ratio = 100 * play.num_loose / num_match
    draw_ratio = 100 * play.num_draw / num_match
    print('  win: {:4d}  [{:5.1f} %]'.format(play.num_win, win_ratio))
    print('loose: {:4d}  [{:5.1f} %]'.format(play.num_loose, loose_ratio))
    print(' draw: {:4d}  [{:5.1f} %]'.format(play.num_draw, draw_ratio))


if __name__ == '__main__':
    main()
