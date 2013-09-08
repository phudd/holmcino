import math
from games.exceptions import *

class Wager(object):
    """Represents a possible wager on the roulette layout, its payout, and the points for
    which it pays.
    
    Most of this API does minimal error checking.  The upstream objects are responsible
    for making sure obviously bad data doesn't get sent to these functions."""
    
    points = []
    """The points on which this bet will win."""
    
    position = None
    """The name of the position.  This name is the hook to the UI commands"""
    
    win = 1.0
    """The payout percentage when winning.  1 pays 100% (double your money).
    We phrase it this way because winning bets typically remain on the board, so this is
    the amount (not including the original wager) to give back to the player."""
    
    amount = 0.0
    """The current amount the player has bet on this wager."""
    
    def __init__(self, position, points, win):
        """The initializer gives us all of the required information to handle the given wager.
        
        params:
            points - an array of Strings (not ints!) That indicates the winning points for this number
            position - The name of the position on the board.  This name will be used by the 
                UI to address bets to the right position of the layout.  ("Red 32", "Street 1 2 3", etc.)
            win - A float that says how much to pay the player on a win
        """
        self.points = [str(p) for p in points]
        self.position = position
        self.win = float(win)        
        if self.win < 0.0 or math.isnan(self.win):
            raise ValueError
    
    def add(self, amount):
        """Add the given amount to the bet.  You can use a negative number to remove part
        of a bet.
        
        Returns a tuple of (amountAddedOrRemoved, amountCurrentlyBet)"""
        amount = float(amount)
        if amount < 0.0 and abs(amount) > self.amount:
            amount = self.amount * -1
        
        self.amount += amount
        return (amount, self.amount)
    
    def resolve(self, point):
        """Returns a tuple of two floats and a string (won/lost, ride, position).
        
        The first is either a positive number (a win) or a negative number (a loss) and indicates
        how much to add/subtract from the user's account.
        
        The second is the amount remaining on the number in play.  This is usually zero."""
        
        retval = 0.0
        riding = 0.0
        
        if point in self.points:
            retval = self.amount * self.win
            riding = self.amount
        else:
            retval = self.amount * -1
            riding = 0.0
        
        self.amount = riding
        
        return (retval, riding, self.position)

class Partage(Wager):
    """The partage wager returns half on 0, 00, or 000."""
    def resolve(self, point):
        if str(point) in ["0", "00", "000"]:
            retval = (self.amount / 2) * -1
            riding = self.amount / 2
            self.amount = riding
            return (retval, riding, self.position)
        else:
            return super(Partage, self).resolve(point)

class RouletteSeat(object):
    """The entire layout, as seen by a single person."""
    pass


