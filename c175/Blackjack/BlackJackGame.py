from Player import Player
from Deck import Deck
import sys
import sgenrand

class BlackjackGame:
    RESULT_DEALER_WON = 0
    RESULT_PLAYER_WON = 1
    RESULT_DRAW       = 2
    
    def __init__(self):
        self.__player = Player("Player", False)
        self.__dealer = Player("Dealer", True)
        self.__deck = Deck() # creates a standard 52 card deck

        self.__draws = 0
        self.__playerWins = 0
        self.__dealerWins = 0
      
    def dealCardsTo(self, player):
        while not player.isBusted() and player.isHitting():
            player.dealCards( self.__deck.drawCards(1) )
            player.showHand()
     
    def gameEnd(self,result):
        if result==BlackjackGame.RESULT_DEALER_WON:
            print(self.__dealer.getName()+" wins!")
            self.__dealerWins += 1
        elif result==BlackjackGame.RESULT_PLAYER_WON:
            print("Congratulations! You win!")
            self.__playerWins += 1
        else:
            print("It's a draw! Unbelievable!")
            self.__draws += 1

    @staticmethod
    def __gamePercentStr(gameNum,total):
        return "("+str(int(gameNum/total*100))+"%)"

    @staticmethod
    def __showStanding(intro,gameNum,total):
        print(intro,gameNum,BlackjackGame.__gamePercentStr(gameNum,total))
        
    def showStandings(self):
        print("Standings:")
        total = self.__playerWins + self.__dealerWins + self.__draws
        if total>0:
            BlackjackGame.__showStanding(self.__player.getName(),self.__playerWins,total)
            BlackjackGame.__showStanding(self.__dealer.getName(),self.__dealerWins,total)
            BlackjackGame.__showStanding("Draws:",self.__draws,total)
        else:
            print("No games so far!")
            
    def play(self):
        # initialize game
        self.__player.clearHand() 
        self.__dealer.clearHand() 
        self.__deck.populate()          
        self.__deck.shuffle()    
        
        # Give the initial 2 cards
        self.__player.dealCards( self.__deck.drawCards(1) )
        # Intercept dealer's first card because we need to show it
        dealersFirstCard = self.__deck.drawCards(1)[0]
        self.__dealer.dealCards( [dealersFirstCard] ) 
        self.__player.dealCards( self.__deck.drawCards(1) )
        self.__dealer.dealCards( self.__deck.drawCards(1) )

        # show the dealer's first card
        print(self.__dealer.getName()+"'s first card:\t",str(dealersFirstCard))
        # show the player's first card
        self.__player.showHand()
        
        # Give additional cards to player
        self.dealCardsTo(self.__player)
        # Once the player is finished if he busted
        # give cards to the dealer
        if self.__player.isBusted():
            print("You bust! :-<\n")
            self.__dealer.showHand()
            print()
            self.gameEnd(BlackjackGame.RESULT_DEALER_WON)
        else:  
            print("\n"+self.__dealer.getName()+"'s turn!")
            self.__dealer.showHand()      
            # Give additional cards to dealer
            self.dealCardsTo(self.__dealer)
            # Determine and announce winner
            print()
            if self.__dealer.isBusted():
                print(self.__dealer.getName()+" busts!")
                self.gameEnd(BlackjackGame.RESULT_PLAYER_WON)
            elif self.__player.getTotal() > self.__dealer.getTotal():
                self.gameEnd(BlackjackGame.RESULT_PLAYER_WON)
            elif self.__player.getTotal() < self.__dealer.getTotal():
                self.gameEnd(BlackjackGame.RESULT_DEALER_WON)
            elif self.__player.getTotal() ==self.__dealer.getTotal():
                self.gameEnd(BlackjackGame.RESULT_DRAW)                    

         
                      
def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--seed':
            print("seeding the random numbers.")
            sgenrand.sgenrand(int(sys.argv[2]))

    game=BlackjackGame()
    again = 'y'
    while again != "n":
        game.play()
        again = input("\nDo you want to play again (y/n)? ").lower()
        print("\n")

    game.showStandings()
    print("Bye!")
    
if __name__=="__main__":
        main()
