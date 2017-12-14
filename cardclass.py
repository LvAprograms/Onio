class Card(object):
    """This class should apply to each card. So you should have many instances of this class in your hand"""
    def __init__(self, value, colour):
        self.value = value
        self.colour = colour

    def __repr__(self):
        return '{} {}'.format(self.colour, self.value)  # CHANGED: removed 'card' in front of {}

    def __eq__(self, other):
        return self.value == other.value and self.colour == other.colour

    def __str__(self):
        return 'Dit is een {} {}'.format(self.colour, self.value)

    def check_play(self, card2):
        return card2 and (self.colour == card2.colour or self.value == card2.value)

    def check_reverse(self):
        return False


class BlueCard(Card):

    def __init__(self, value):
        super().__init__(value, (0, 0, 255))


class RedCard(Card):

    def __init__(self, value):
        super().__init__(value, (255, 0, 0))


class GreenCard(Card):

    def __init__(self, value):
        super().__init__(value, (0, 255, 0))


class YellowCard(Card):

    def __init__(self, value):
        super().__init__(value, (255, 255, 0))


class Reverse(Card):

    def __init__(self, colour):

        super().__init__('reverse', colour)

    def check_reverse(self):
        return True


# COLOURS = {
#     'RED': (255, 0, 0),
#     'GREEN': (0, 255, 0),
#     'BLUE': (0, 0, 255),
#     'YELLOW': (255, 255, 0),
# }
#
#
# class BlueCard(Card):
#     def __init__(self, value):
#         super().__init__(COLOURS['BLUE'], value)

# class Card(object):
#     """"# This class should apply to each card. So you should have many instances of this class in your hand."""
#     def __init__(self, value, colour, powers=None):
#         self.value = value
#         self.colour = colour
#         self.powers = powers
#
#     def __repr__(self):
#         return '{} {}'.format(self.colour, self.value) # CHANGED: removed 'card' in front of {}
#
#     def __eq__(self, other):
#         if self.value == None:
#             return self.powers == other.powers and self.colour == other.colour
#         else:
#             return (self.value == other.value or self.powers == other.powers) and self.colour == other.colour
#
#     def __str__(self):
#         return 'Dit is een {} {}'.format(self.colour, self.value)
