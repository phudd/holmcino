import math
from games.exceptions import *

pointRange = [4, 5, 6, 8, 9, 10]
naturalRange = [7, 11]
crapsRange = [2, 3, 12]

class InvalidPointError(GameError):
    code = 1201
    message = "Point must be one of 4, 5, 6, 8, 9, 10"

class LineOnPointError(BetNotYetError):
    code = 1202
    message = "You can not place a line bet when there is a point."

class RequiresNewBet(GameError):
    code = 1203
    message = "Requires a new bet instead of adding to an old one."    

def validateAmount(amount):
    """Ensures the point is a float greater than 0, and not NaN.
    
    Returns the validated float amount.
    """
    try:
        amount = float(amount)
        if amount <= 0 or math.isnan(amount):
            raise BetInvalidAmount
    except ValueError:
        raise BetInvalidAmount
    return amount

def validatePoint(point):
    """Ensures the point is 0 (no point) or is a valid integer in [4,5,6,8,9,10].
    
    Returns the validated integer point.
    """
    try:
        point = int(point)
        if point and point not in pointRange:
            raise InvalidPointError
    except ValueError:
        raise InvalidPointError
    return point
        

class CrapsBetFactory(object):
    wagers = {}
    def register(self, name, theClass):
        assert callable(theClass)
        name = name.lower()
        if not self.wagers.has_key(name):
            self.wagers[name] = theClass
    def create(self, name, *args, **kwargs):
        name = name.lower()
        func = self.wagers[name]
        return apply(func, args, kwargs)

betFactory = CrapsBetFactory()
"""Use betFactory to create bets based on the registered names of the wager classes.

eg: bet = betFactory.create('pass', 20, 0)
"""

class CrapsWager(object):
    amount = 0.0
    """How much is currently bet on this wager."""
    
    point = 0
    """Subclasses are not required to track this value, but many use it."""
    
    def __init__(self, amount, point):
        """Sets the amount of the bet.
        
        The amount and points are assumed to be valid, and no validation is done at the
        Wager level.  The hosting Game must filter the values before calling the constructor.
        
        If the bet is invalid (usually because of timing) then throw a GameError or one of
        its subclasses.
        
        *float* **amount** The amount to bet.  A positive float value
        *int* **point** The current point.  Must be 0 or in pointRange.  Set to 0 by the constructor
        """
        self.amount = amount
        self.point = 0
    
    def add(self, amount, point):
        """Add more to the current bet.  Subclasses may override this.
        
        On success, returns the new bet total for this wager.  The subclass may round down
        the new bet amount, but not below zero.
        
        On failure, throw a GameError exception.
        
        Some bets can't be added to, but you can make a new bet that is the same.  Raise
        RequiresNewBet to indicate such a condition."""
        self.amount += amount
        return self.amount
        
    def eval(self, point, d1, d2):
        """Evaluate the bet in light of the given roll.
        
        *int* **point** This is the point before the dice were rolled.
        *int* **d1** An integer in the range 1-6
        *int* **d2** An integer in the range 1-6
        
        Must return a float:
            0 - The bet is pushed to the next roll
            f < 0 - The bet is lost, and must be removed from the table.  The return value 
                must be negative the amount of the bet.
                eg: For a 13.0 bet that is lost, the amount must be -13
            f > 0 - The bet is won, and must be removed from the table.  The dealer pays
                the given amount (which will be greater than the bet amount) to the player.
                eg: A line bet of 12 returns 24.
        """
        return self.amount
    
    def canRemove(self, point):
        """Returns true if the wager can be removed, false otherwise."""
        return False
    
class PassWager(CrapsWager):
    def __init__(self, amount, point):
        if point:
            raise LineOnPointError
        super(PassWager, self).__init__(amount, point)
    
    def add(self, amount, point):
        if point:
            raise LineOnPointError
        self.amount += amount
        return self.amount
    
    def eval(self, point, d1, d2):
        payout = 0.0
        total = d1 + d2;
        
        if not self.point:
            if total in naturalRange:
                payout = self.amount * 2
            elif total in crapsRange:
                payout = self.amount * -1
            else:
                self.point = total
        else:
            if total == 7:
                payout = self.amount * -1
            elif total == self.point:
                payout = self.amount * 2
        return payout
    
    def canRemove(self):
        return False if self.point else True
betFactory.register('pass', PassWager)

class DontPassWager(CrapsWager):
    def __init__(self, amount, point):
        if point:
            raise LineOnPointError
        super(DontPassWager, self).__init__(amount, point)
    
    def add(self, amount, point):
        if point:
            raise LineOnPointError
        self.amount += amount
        return self.amount
    
    def eval(self, point, d1, d2):
        payout = 0.0
        total = d1 + d2;
        
        if not self.point:
            if total in [2,3]:
                payout = self.amount * 2
            elif total in naturalRange:
                payout = self.amount * -1
            elif total == 12:
                payout = 0.0
            else:
                self.point = total
        else:
            if total == 7:
                payout = self.amount * 2
            elif total == self.point:
                payout = self.amount * -1
        return payout
    
    def canRemove(self):
        return False if self.point else True
betFactory.register('dontpass', DontPassWager)
