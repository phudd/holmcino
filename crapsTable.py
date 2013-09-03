import os
import sys
from hashlib import sha256
import traceback
import datetime
import json
from tornado import websocket
from tornado import gen
from tornado.ioloop import IOLoop
import base58

"""Notes for consideration

We might need the idea of a Player, a Game, and a PlayerSeat.
    There needs to be a player handler object
    There also needs to be a player session object, because players may repeatedly connect and disconnect
        (page reloads, network errors, and a whole host of other shit we can't control)
        The session can have a lot of activity on it while the player is out, like craps table rolls.
        The same player might have multiple connections.
        The same player might play multiple games. (Should we allow that?)
        If the same player has multiple sessions/games across multiple servers, does that matter?
        
        If a player loses their connection then they are "gray" until they either (1) reconnect
        or (2) all their outstanding bets are paid/taken
    Players might want to do things not directly related to the game, like search for new games,
    check their balance, and who-knows-what-else?
    PlayerSeats are the player's "spot" on the game.  Might not need this...but maybe will
    Games can come and go, and players can be added and removed from them.
"""

theTable = None
    
class CrapsTable(object):    
    def __init__(self, loop=None):
        self.loop = loop or IOLoop.current()
        self.delegate = GameDelegate()
        self.state = "setting up"
        self.players = {}
        self.nonce = None
        self.loop.add_timeout(datetime.timedelta(seconds=2), self.setup)
    
    def setup(self):
        self.chat('server', 'setting up')
        self.nonce = self.generateRandomString()
        self.chat('server', self.nonce)
        self.state = "coming out"
        
    def addPlayer(self, player):
        self.players[player.userInfo['id']] = player
        player.write_message("You have joined a craps game!")        
    
    def removePlayer(self, player):
        pid = player.userInfo['id']
        if self.players.get(pid):
            del self.players[pid]
    
    def chat(self, name, text):
        notification = "chat {0} {1}".format(name, text)
        for pname, player in self.players.iteritems():
            player.write_message(notification)
    
    def generateRandomString(self, len=8):
        rand = os.urandom(512)
        return base58.b58encode(sha256(rand).digest())[:len]

class CrapsPlayer(websocket.WebSocketHandler):
    userInfo = {}
    
    @gen.coroutine
    def open(self, userToken, **kwargs):
        global theTable
        if not theTable:
            theTable = CrapsTable()
        self.delegate = GameDelegate()
        self.userInfo = yield self.delegate.getUserInformation(userToken)
        self.write_message("craps 0.1")
        self.write_message("player {0}".format(json.dumps(self.userInfo)))
        theTable.addPlayer(self)

    def close(self):
        global theTable
        theTable.removePlayer(self)
        
    def on_message(self, message):
        global theTable
        try:
            (command, params) = message.split(' ', 1)
            if command == 'say':
                theTable.chat(self.userInfo['id'], params)
        except Exception as ex:
            self.write_message("error: {}\n{}".format(str(ex), traceback.format_exc()))

class GameDelegate(object):
    """Integration hooks between the host system and the game server.
    
    The hooks fall generally into a few categories:
    - Game registration and discovery
    - User identification
    - Bet approval and registration
    - Random number generation
    
    The hooks provided in the default delegate allow anybody to connect with any username
    and approves any amount.
    
    All of the functions you implement here must be generators.  They will be called within
    the context of the main IO loop, so you may need to do more awesome stuff.
    """
    
    @gen.coroutine
    def getUserInformation(self, token):
        """For a given token, retrieve the user information as a dictionary.
        
        The minimum required members is:
            "id":
            "name":
        Optional values
            "bet_limit": 
        
        The game server will pass in whatever token it received on connection.  The delegate
        may throw an exception to indicate that the user is not allowed to play the game.
        """
        return {"id":token, "name":token}
        
    
    @gen.coroutine
    def registerGame(game_id, game_desc, players):
        yield True
    
    @gen.coroutine
    def approveWager(self, user, amount):
        """Asks for approval for a specific wager amount.
        
        The delegate may return an amount less than what was requested, or simply True.
        
        Returning False indicates the player may not make the wager.
        """
        yield True
    
    @gen.coroutine
    def getNonce(self):
        """Returns a string that the game should display to users.  It is part of the
        provably secure system of PRGN.
        
        Returns a string.
        """
        return self.generateRandomString()
        
    def generateRandomString(self, len=8):
        return base58.b58encode(sha256(os.urandom(512)).digest())[:len]
