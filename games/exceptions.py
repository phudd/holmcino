
class GameError(Exception):
    """The base class for all game errors.
    
    GameError includes two attributes:
        code: a positive numeric code that indicates the specific error type to the client 
        (usually a web browser)
        
        data: Defaults to None, but can be any native python data (usually an array or dict)
    """
    
    code = 700
    """The numerical error code that bubbles up to the client software."""
    
    message = "General game eror"
    """The human-readable error message."""
    
    data = None
    """Arbitrary data.  Must consist entirely of Python built-in types, with no circular references."""
    
    def __init__(self, code=None, data=None):
        if code:
            self.code = code
        if data:
            self.data = data
    
    def __str__(self):
        return "GameError({}) {}".format(self.code, self.message)
    
    def json(self):
        return { "code":self.code, "message":self.message, "data":self.data }

class BetTooBigError(GameError):
    code = 701
    message = "Your bet exceeds the maximum allowed"

class BetNotYetError(GameError):
    code = 702
    message = "You can not place that bet now"

class BetIsFinalError(GameError):
    code = 703
    message = "You can not remove that bet"

class BetInvalidAmountError(GameError):
    code = 704
    message = "Bets must be positive floating point numbers"

class BetInvalidError(GameError):
    code = 705
    message = "That bet is invalid"
    
class InsufficientFundsError(GameError):
    code = 706
    message = "Insufficient funds"

