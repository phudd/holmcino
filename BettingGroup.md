Everyone who is part of the same game must be on the same server/ioLoop.

Game Discovery
Game Creation
Game Change Notification (recent player list)
Bet Limit Approval:
	approve(playerid, amt) ==> approved amount
Bet Return
Logging
Disconnect/Reconnect
Transfer of control to game system
Player authentication
Die/Restart
Random number recreation
Multi-player games continue even when people disconnect.  Yer OOL dude.
Start a table with just your friends


	__init__.py
		games = {
			'xxydffyxaksdk': <some big object>
		}
	


connection arrives with a single parameter.  Eg:

	ws://casinoserver.org:8801/craps/_any_/_playerid_
	

Game Delegate
