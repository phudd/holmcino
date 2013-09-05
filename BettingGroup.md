Everyone who is part of the same game must be on the same server/ioLoop.

Rules
=====

Connections come and go, but players stay at their tables.

Every wager is final, at least until the game server crashes.


Implementation Discoveries
==========================

- Don't try to do a lot of stuff from open().  You get zero reporting.
- Look/Change ops have to occur in uninterrupted code blocks.  We get a strong assist from our architecture, which means we don't need locking, but we still can't yield during a multi-step change

Trash 
=====

When do we write game state? (Every bet might be too much.  Every roll might be sensible.)
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
