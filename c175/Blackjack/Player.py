from Deck import Deck
from Hand import Hand
from Card import Card

class Player():
    '''
    Assigns instance variables for name and isDealer, and creates an empty Hand
    object. isDealer will be 'True' if the Player is the dealer, and 'False'
    otherwise. Returns the instance variable for the player's name.'''

    def __init__(self, name, isDealer):
        self.name = name
        self.isDealer = isDealer
        self.hand = Hand()
    
    def getName(self):
        return self.name
    
    def dealCards(self, cards):
        self.hand.dealCards(cards)
        
    def clearHand(self):
        self.hand.clear()
        
    def getTotal(self):
        return self.hand.getTotal()
        
    def isBusted(self):
        return self.hand.isBusted()
    
    def isHitting(self):
        if self.isDealer:
            value = self.getTotal()
            if value < 17:
                return True
            else:
                return False
            
        else:
            end = False
            while not end:
                decision = input("Do you want to hit? (Y/N) ")
                if decision.upper() == "Y":
                    end = True
                    return True
                elif decision.upper() == "N":
                    end = True
                    return False
                else:
                    print("invalid input.")
            
    def showHand(self):
        print(self.name, "'s cards:", self.hand, "Value:", self.getTotal())
            
            
        '''
        dealCards(self, cards): Takes the cards and adds them to the player's hand.
        clearHand(self): Clears the player's hand.
        getTotal(self): Returns the total value of the Player's hand.
        isBusted(self): Checks if the player has busted. Returns True if the player has busted.
        isHitting(self): Return True if the player wants to continue. The behaviour will depend on whether or not the player is the Dealer:
        isDealer is False: The player is no the Dealer. Query the player if they would like to hit or hold. Return True if the player wants to hit and return False  the player wants to hold. Query the player even if the player's hand totals 21. Use the sample output below as a guide for the expected output.
        isDealer is True: The player is the Dealer. The Dealer must hit if the hand is less than 17. The dealer must hold if their hand is larger than or equal to 17.
        showHand(self): Shows (outputs) the hand of the player. Use the sample output below as a guide for the expected output.        '''