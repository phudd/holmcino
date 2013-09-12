import sys
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
    
    def __str__(self):
        return "{} {}:1".format(self.position, self.win)
        
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
        
        if self.amount != 0.0:
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

def europeanLayout():
    """Returns an array of wager positions for a European game.  
    
    Single zero, partage, no imprison."""
    retval = []
    red = [1, 3, 5, 7, 9, 12, 14, 18, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
    
    # All those even-payout partage bets
    retval.append( Partage("Red", red, 1) )
    retval.append( Partage("Black", [p for p in range(1,37) if p not in red], 1) )
    retval.append( Partage("Odd", [p for p in range(1,37,2)], 1) )
    retval.append( Partage("Even", [p for p in range(2,37,2)], 1) )
    retval.append( Partage("First 18", range(1,19), 1) )
    retval.append( Partage("Second 18", range(19,37), 1) )
    
    # thirds
    retval.append( Wager("First 12", range(1, 13), 2) )
    retval.append( Wager("Second 12", range(13,25), 2) )
    retval.append( Wager("Third 12", range(25,37), 2) )
    
    # six-line
    for streetEnd in range(6,37,3):
        streetStart = streetEnd-5
        w = Wager("Line {}-{}".format(streetStart, streetEnd), range(streetStart,streetEnd+1), 5)
        retval.append(w)
    
    # All the corners
    # Look at a layout picture, and this will make more sense
    for ctr in [p for p in range(5,37) if p%3 != 1]: # 5 6 8 9 ...
        corner = [ctr-4, ctr-3, ctr-1, ctr]
        name = "Corner {0} {1} {2} {3}".format(*corner)
        retval.append( Wager(name, corner, 8) )
    
    # three-numbered streets
    for streetEnd in range(3,37,3):
        streetStart = streetEnd-2
        w = Wager("Street {}-{}".format(streetStart, streetEnd), range(streetStart,streetEnd+1), 11)
        retval.append(w)

    # Horizontal Splits
    for pos in [p for p in range(1,36) if p%3]:
        pair = [pos, pos+1]
        name = "Split {0} {1}".format(*pair)
        retval.append( Wager(name, pair, 17) )
    
    # Vertical Splits
    for pos in range(1,34):
        pair = [pos, pos+3]
        name = "Split {0} {1}".format(*pair)
        retval.append( Wager(name, pair, 17) )
    
    # All of the single-number bets
    redWagers = [ Wager("Red {}".format(p), [p], 35) for p in red ]
    blackWagers = [ Wager("Black {}".format(p), [p], 35) for p in range(1,37) if p not in red ]
    retval += redWagers + blackWagers
    
    # And the number that, all by itself, imparts profit
    retval.append( Wager("0", ["0"], 35) )
    
    return retval
    
class Seat(object):
    """The seat manages one player's place in the game.
    
    The seat is not in charge of policy -- that is the Game object's job.  But it does have
    to keep the necessary data on tap.  It is mostly a composite of all possible positions,
    plus some aggregate amounts.
    """
    
    def __init__(self, factory=europeanLayout):
        self.positions = factory()
        self.amount = 0.0 # the current total the player has on the board
        self.won = 0 # cumulative win/loss during this session
        
    def bet(self, position, chips):
        """Creates a new position, or adds to an existing one."""
        pos = None
        for oneWager in self.positions:
            if oneWager.position == position:
                pos = oneWager
                break;
        if not pos:
            raise BetInvalidError("{} is not a valid position".format(position))
        
        (changeAmount, currentAmount) = pos.add(chips)
        self.amount += changeAmount
        
        return (changeAmount, currentAmount, pos.position)
        
    def resolve(self, point):
        changes = []
        newWinnings = 0.0
        newAmount = 0.0
        
        for pos in self.positions:
            oneChange = pos.resolve(point)
            if oneChange[0] != 0:
                newWinnings += oneChange[0]
                newAmount += oneChange[1]
                changes.append(oneChange)
        
        self.amount = newAmount
        self.won += newWinnings
        
        return { 'amount':self.amount, 'won':newWinnings, 'changes':changes }
