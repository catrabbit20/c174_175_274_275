import random
# custom random generator to avoid 
# cross-platform incompatability issues
import sgenrand
from Card import Card
from Hand import Hand


class Deck:
    '''The deck contains an ordered list of cards.
    One can shuffle a deck, repopulate it (to contain
    all cards of all different suits and ranks),
    a draw cards from its "top".
    '''
    def __init__(self):
        '''Initializes the deck, by populating it.'''
        self.populate()
        self.shuffle()
        
    def populate(self):
        '''Make the deck empty first (contain no cards). Then
	populates the deck of cards to make sure that it contains
        all the 52 cards in a common deck (a French deck).
        The order should be by suit, h d c s, and then value, 
        A 2 3 4 5 6 7 8 9 10 J Q K
        '''
        self.__cards = []
        
        val = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        suit = ["h", "d", "c", "s"]
        
        for i in suit:
            for j in val:
                self.__cards.append(Card(j,i))
        
        
        
        
                        
    def shuffle(self):
        '''Shuffles the deck of cards.'''
        random.shuffle(self.__cards,sgenrand.genrand)    
        
    def drawCards(self, number):
        '''Draws <number> cards from the "top" of
        the deck and return them as a list.
	The function should also remove the cards drawn from the deck.
        For consistency, we define the top card of the deck to be
        the last card in the list.
        When the number of cards requested is greater than the 
        number of cards in the deck, all cards
        of the deck are removed and returned --
        no error will be raised.'''
        for i in range(number):
            cards_drawn = []
            cards_drawn.append(self.__cards.pop())
        return cards_drawn
