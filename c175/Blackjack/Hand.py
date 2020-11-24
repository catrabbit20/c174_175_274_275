from Card import Card


class Hand:
    '''A BlackJack hand is an ordered list of cards.
    New cards can be added to the hand. The hand can 
    tell its total value and whether it is "busted".
    '''
    def __init__(self):
        '''Initializes the hand by creating 
        an empty list for the cards.'''
        self.__cards = []
        
    def dealCards(self, cards):
        '''Add cards to the hand.
        cards must be an iterable
        object containing Card objects.'''
        for i in range(len(cards)):
            self.__cards.append(cards[i])

    def clear(self):
        '''Removes all the cards from the hand'''
        self.__cards = []
    
    def getTotal(self):
        '''Returns the total value of the hand, 
        according to Blackjack rules. Remeber to make correct
	use of any Aces in the hand.'''
        total = 0
        aces_present = 0
        for i in range(len(self.__cards)):
            current_card = self.__cards[i].getValue()
            if current_card == 1:
                aces_present += 1
                total += 11
            else:
                total += current_card 
                
            if total > 21 and aces_present > 0:
                aces_present -=1
                total -= 10
        return total
    
    def isBusted(self):
        '''Returns true when the total value 
        of the hand is over 21'''               
        if self.getTotal() > 21:
            return True
        else:
            return False

    def __str__(self):
        '''Returns a nicely formatted string representation
        of the hand.'''
        output_string = ""
        for i in range(len(self.__cards)):
            output_string += str(self.__cards[i])
        return output_string