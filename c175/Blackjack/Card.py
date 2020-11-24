class Card:
        
    def __init__(self, rank, suit):
        '''Initialize the card's suit and rank.'''
        self.rank = rank
        self.suit = suit
                
    def __str__(self):
        '''Return a string composed of the rank and suit. The rank comes first.
	For example, the 3 of Clubs would be 3c.
        '''
        return str(self.rank) + str(self.suit)
        
    def getValue(self):
        '''Returns the Blackjack value for the card. Face cards return
        a value of 10, Ace is valued at 1, and the numeric cards use their numeric values
        (i.e. 8h would return 8).
        '''
        if self.rank.isdigit():
            return int(self.rank)
        elif self.rank == "A":
            return 1
        else:
            return 10
    
red = Card("c", 10)
print(red)