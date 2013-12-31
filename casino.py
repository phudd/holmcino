import tornado.gen

class Delegate(object):
	"""Integrate the game system with the back-end data store.
	
	The delegate is in charge of:
	- Registering and unregistering games
	- Authorizing and identifying logins
	- Authorizing game joins
	- Authorizing bets
	- Recording wins and losses
	- Generating and recording random events (game keys, die rolls, deck shuffles)

	In short, we have tried to put all of the player, money, and tracking hooks into this
	one class.
	
	All Delegates must use the @tornado.gen.coroutine annotation, and properly use yield/return.
	
	The default delegate accepts any players not already playing, sets aside 1000 in chips per
	player, and doesn't really log anything.
	"""
	
	reserveMethod = False;
	
	@tornado.gen.coroutine
	def autorizeUser(self, token):
		"""Returns information about the authorized user, or throws an InvalidAuth exception.
		
		When users are passed form the main web site to the casino's WebSocket connection,
		the web site should provide some kind of token that:
		- identifies the user
		- indicates that user is allowed to play in the casino
		
		This method's job is to validate the token, and return information about the user.
		The user information must be a dictionary whose minimum entries are:
		- player_id: a system-unique player identifier
		- player_name: the name by which the player is known
		- public_fields: a list of field names that can be made available to other players
		
		When the player joins a table, his public information will be transmitted to all of
		the other players.  Generally, the only field should be player_name.  If player_name
		is not in public_fields, then "Anonymous" is used instead.
		"""
		return { 'player_id':token, 'player_name':token, 'public_fields':['player_name'] }
	
	@tornado.gen.coroutine
	def getBalances(self, players):
		"""Return the current amount available for betting for all of the players.
		
		Inputs:
		- players: a list of player IDs
		"""
		return []
	
	
	
	