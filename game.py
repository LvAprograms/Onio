# This will be the class for the card. It must have a colour and a number (for the first version)
# I need a class for the deck of cards. This starts at 80
import logging
import random
from cardclass import Card, Reverse

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
# colours = [BLUE, RED, GREEN, YELLOW]
# for card in deck:
#     print(card.value, card.colour)
# logging.debug('Checking if shuffling worked)')


# for card in deck:
#     print(card.value, card.colour)  # I tested this and it works :D

logging.basicConfig(filename='Onio.log', level=logging.DEBUG)


class PlayStack(object):
    """Represents the playstack of all cards, where only the top card is visible to the players. Starts at 1"""

    def __init__(self, deck, decksize, stacksize=0):
        self.stacksize = stacksize
        self.decksize = decksize
        self.deck = deck
        self.stack = []
        self.topcard = []
        self.startcard = deck[0]

    def startingcard(self):
        self.stacksize += 1
        del self.deck[0]
        self.decksize -= 1
        self.stack.append(self.startcard)
        self.topcard = self.stack[-1]

    def show_top_card(self):
        """Should return the top card of the deck"""
        return 'Er ligt een {}'.format(repr(self.topcard))


class Player(object):

    def __init__(self, name, game):
        self.game = game
        self.handsize = game.handsize
        self.hand = []
        self.name = name
        self.deck = game.deck
        self.decksize = game.decksize

    def look_at_hand(self):
        """Shows all cards in the hand of handsize handsize"""
        for eachCard in self.hand:
            print(eachCard)

    def sort_hand(self):
        return sorted(self.hand, key=lambda card: (card.colour, str(card.value)))

    def drawcard(self, startphase=False):
        """Draws one card from the deck and adds it to the player's hand"""
        draw = self.deck[0]
        # print(deck)
        self.hand.append(draw)
        del self.deck[0]
        self.decksize -= 1
        self.hand = self.sort_hand()
        if not startphase:
            self.handsize += 1
        return 'Je hebt een {} {} getrokken.'.format(draw.colour, draw.value)

    def drawcards(self, n, startphase=False):
        for i in range(n):
            self.drawcard(startphase)

    def update(self, card_to_play):
        logging.debug('Found the card! appending to stack and removing from hand now')
        self.handsize -= 1
        self.game.playstack.stacksize += 1
        self.game.playstack.stack.append(card_to_play)  # append card to stack
        self.hand.remove(card_to_play)  # remove card from hand
        self.game.playstack.topcard = card_to_play  # change top card to the played card!

    def playcard(self, card_to_play):  # I want to get a card away from the hand onto the playstack
        if card_to_play and card_to_play.check_play(self.game.playstack.topcard):
            if card_to_play.check_reverse():
                logging.info('Played card was a reverse')
                self.update(card_to_play)
                self.game.reverse(self.game.players, self.game.current_player)
                return
            else:
                logging.info('Played card was no reverse')

            logging.debug('attempted play is valid!')
            self.update(card_to_play)
            logging.debug('Je bent een geit')
        else:
            logging.error('Attempted play is not allowed. colour on colour or value on value!')
            print(card_to_play.check_play(self.game.playstack.topcard))
            new_card_to_play = input('Deze kaart mag niet! Probeer een andere:').split(' ')
            new_card_to_play = Card(new_card_to_play[1], new_card_to_play[0])
            new_card_to_play.value = int(new_card_to_play.value)
            return self.playcard(new_card_to_play)

    def __str__(self):
        return 'Speler {} heeft {} kaarten in handen.'.format(self.name, self.handsize)


class Game(object):

    def __init__(self):
        self.players = list()  # create list of players
        self.handsize = self.ask_handsize()
        self.deck = self.shuffle_deck(self.make_deck())
        self.decksize = len(self.deck)
        self.playstack = PlayStack(self.deck, self.decksize)
        self.startgame()
        self.curplayer_index = 0
        self.current_player = self.players[self.curplayer_index]
        self.direction = True
        self.done = False

    def update_curplayer(self):
        self.curplayer_index = (self.curplayer_index + 1 if self.direction else -1) % len(self.players)
        self.current_player = self.players[self.curplayer_index]

    @staticmethod
    def make_deck():
        colours = ['rode', 'blauwe', 'groene', 'gele']  # create colour vector
        deck = [Card(value, colour) for value in range(10) for colour in colours]  # create deck of 1 copy of each card
        for colour in colours:
            deck.append(Reverse(colour))
        deck = deck + deck  # create another card for each card
        # print(deck)
        return deck

    def startgame(self):
        self.ask_players()
        startphase = True
        # initialise drawing the starting hand
        for eachPlayer in self.players:
            # For the starting draw, startphase is true. Afterwards it
            # uses the default value False (see Player.drawcard method)
            eachPlayer.drawcards(self.handsize, startphase)

        return self.players

    @staticmethod
    def shuffle_deck(pack_of_cards):
        """"Shuffles the whole deck"""
        random.shuffle(pack_of_cards)
        return pack_of_cards

    @staticmethod
    def ask_handsize():
        handgiven = False
        while handgiven is False:
            try:
                handsize = int(input('Met hoeveel kaarten wil je beginnen? '))
                if handsize < 7:
                    logging.critical('Je moet beginnen met minimaal 7 kaarten!')
                else:
                    handgiven = True
                    return handsize
            except (ValueError, TypeError):
                logging.critical('No handsize was given.')
                print('Vul een aantal kaarten in (minstens 7).')

    def ask_players(self):
        names = input('Wie spelen er? Scheid de namen met een komma\n').split(',')
        if len(names) < 2:
            logging.critical('Geef minstens 2 namen op')
            names = input('Je moet minstens 2 namen opgeven. Probeer opnieuw:\n')
        else:
            pass

        print('Welkom {}. Veel speelplezier met Onio!'.format(' en '.join(name for name in names)))
        self.playstack.startingcard()  # put a starting card on the table
        # create player instances
        num_of_players = len(names)
        for i in range(num_of_players):
            self.players.append(Player(names[i], self))

    def make_move(self, current_player):
        move = input('Wil je een kaart opleggen of trekken?\n')
        if move == 'opleggen' or move.startswith('o'):
            card_to_play = input('Welke kaart wil je opleggen?\n').split(' ')  # Asks which card to play
            # if card_to_play[1] == 'reverse':
            candidates = [c for c in current_player.hand if str(c.value) == card_to_play[1] and c.colour == card_to_play[0]]
            card_to_play = candidates[0] if len(candidates) > 0 else None
            #    card_to_play = Reverse(card_to_play[0])
            # else:
            #    card_to_play = Card(card_to_play[1], card_to_play[0])
            #    card_to_play.value = int(card_to_play.value)
            current_player.playcard(card_to_play)
            print(self.playstack.stack)
            print(current_player.handsize)

            if current_player.handsize <= 0:
                print('Gefeliciteerd! {} heeft gewonnen!'.format(current_player.name))  # the game ends
                self.done = True  # To shut down game
                # quit()
            print('Er zitten nog {} kaarten in de trekstapel.'.format(self.decksize))

        elif move == 'trekken' or move.startswith('t'):
            current_player.drawcard()
        else:
            logging.error('Typo made in answer for move')

    def play(self, current_player, heap_of_cards):
        """This is the actual game, taking turns with playing and drawing cards"""
        self.decksize = len(heap_of_cards)  # to prevent shadowing of deck
        print('{}: {}'.format(current_player.name, ', '.join(repr(card) for card in current_player.hand)))
        print(str(current_player))
        print(self.playstack.show_top_card())  # shows the top card of the deck to the player who's turn it is
        self.make_move(current_player)
        self.update_curplayer()

    def reverse(self, players, current_player):
        if len(players) == 2:
            self.make_move(current_player)  # take another turn
        elif len(players) > 2:
            self.direction = not self.direction
            print('\n'.join(str(p) for p in players))
            return players


def main():
    game = Game()
    while not game.done:
        game.play(game.current_player, game.deck)


if __name__ == '__main__':
    main()
