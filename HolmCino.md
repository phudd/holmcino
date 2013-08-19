Random notes from the fringe
============================


Know your accounting use cases, even the Bad Ones.

Engaging Play
-------------

Use good feedback and science to get people to keep hitting the buttons.

I've noticed that I enjoy the cleaner presentations better.

What about multi-player table play?  If you put the dice-roll/roulette-ball on a timer, and give a 5-sec countdown after bets are off, then you can have a good time.  

A multi-player table game would be awesome ... with gravatar images of the players around the table and a chat interface.

User Account Management
-----------------------

Absolute easiest signup possible.  Less friction is better than more friction.  The primedice model is really nice, and they've done a good job  of thinking though the security implications.

#### New User Signup

> Bob enters his payout address.  If that address does not have an existing account, then create one.

#### Old User Returns

> Bob enters his payout address.  We find his password and userid in the cookies, which match his login.  Then we re-establish his session.

#### Old User Returns With New Session

> Someone logs in, claiming to be Bob. One of two things happens.

> If he knows his password, then we let him play as-is.  We can safely re-establish his session.

> If he doesn't know his password, then he can still play.  But first we pay out his entire account.  He'll have to re-deposit funds to play, and his password will be reset.

> If he doesn't know his password and can't be payed out, then he can't play.

Profiles
--------

Set user name.  Set Avatar.

Expose user name to others.  If you don't, when you go to multiplayer tables you'll receive an alias.  (Jayne Penny, Bob Roller, John Whale).

Tables
------

Session Table - user, session id, IP?

Customer

- customer_id
- other_id

### Multiplayer

Player always sees himself in the same position.  Other player's positions are determined randomly.  Up to N per table (4, 6?).

Players have some amount of time to place their wagers.  They get a three-second warning, during which bets are closed.  Then the roll!

#### Gamestate

- player 

Test Data
---------

### Customer Accounts ("Customers")

- mvdemVHg5z2FJpA88gLzfxbNJmZFYRhDde

### Payout Addresses ("Payouts")

- murVPyqbVrQiGom1Pyd66zD1srxxNEHbHx

Test Cases
----------

Attempt to use an existing deposit address as a payout address
Attempt to log in without a password to an account that can't be paid out because of pending confirmations.
