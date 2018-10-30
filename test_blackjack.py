import pytest

from blackjack import Card, Deck, Player, Blackjack


class TestCard:
    @pytest.mark.parametrize('id', [10.4, -1, -100])
    def test_value_error(self, id):
        with pytest.raises(ValueError):
            Card(id)

    @pytest.mark.parametrize('id, name', [
                             (0, 'Spade A'),
                             (4, 'Spade 5'),
                             (9, 'Spade 10'),
                             (10, 'Spade J'),
                             (11, 'Spade Q'),
                             (12, 'Spade K'),
                             (13, 'Club A'),
                             (26, 'Heart A'),
                             (39, 'Diamond A'),
                             (52, 'Spade A'),
                             (65, 'Club A'),
                             (78, 'Heart A'),
                             (91, 'Diamond A'),
                             ])
    def test_card_name(self, id, name):
        card = Card(id)
        assert card.id == id
        assert card.name == name

    @pytest.mark.parametrize('id, point', [
                             (0, [1, 11]),  # Spade A
                             (4, [5, 5]),  # Spade 5
                             (9, [10, 10]),  # Spade 10
                             (10, [10, 10]),  # Spade J
                             (11, [10, 10]),  # Spade Q
                             (12, [10, 10]),  # Spade K
                             (13, [1, 11]),  # Club A
                             (26, [1, 11]),  # Heart A
                             (39, [1, 11]),  # Diamond A
                             ])
    def test_card_point(self, id, point):
        card = Card(id)
        assert card.id == id
        assert set(card.point) == set(point)


class TestDeck:
    def test_get_id(self):
        deck = Deck(1)
        assert deck.num_cards == 52
        id = deck.get_id()
        assert type(id) == int
        assert 0 <= id < 52
        assert deck.num_cards == 51

    def test_refresh(self):
        deck = Deck(1)
        for i in range(10):
            deck.get_id()
        assert deck.num_cards < 51
        deck.refresh()
        assert deck.num_cards == 52


class TestPlayer:
    def test_name(self):
        name = 'abcdefghijklmn'
        player = Player(name)
        assert name.startswith(player.name, 0, 7)

    def test_draw(self):
        player = Player('You')
        assert len(player.hold_cards) == 0
        player.draw_card(0)
        assert player.hold_cards == ['Spade A', ]
        player.draw_card(4)
        assert player.hold_cards == ['Spade A', 'Spade 5']

    def test_get_point(self):
        player = Player('You')
        player.draw_card(0)
        assert player.get_point() == [1, 11]
        player.draw_card(13)
        assert player.get_point() == [2, ]
        player.draw_card(10)
        player.draw_card(11)
        assert player.get_point() == [22, ]

    def test_refresh(self):
        player = Player('You')
        for i in range(3):
            player.draw_card(i)
        assert len(player.hold_cards) == 3
        assert player.get_point() != [0, ]
        player.refresh()
        assert len(player.hold_cards) == 0
        assert player.get_point() == [0, ]


class TestBlackjack:
    def test_first_draw(self):
        play = Blackjack('You')
        play.first_draw()
        assert 1 <= max(play._player.get_point()) <= 21
        assert 1 <= max(play._dealer.get_point()) <= 21

    def test_state(self):
        play = Blackjack('You')
        assert play.player_stat is None
        play._player.draw_card(0)
        play._player.draw_card(10)
        play._check_points()
        assert play.player_stat == 'blackjack'
        play._player.draw_card(11)
        play._player.draw_card(12)
        play._check_points()
        assert play.player_stat == 'bust'

    def test_dealer_draw(self):
        play = Blackjack('You')
        play.first_draw()
        play.dealer_draw()
        assert max(play._dealer.get_point()) >= 17
