import unittest
from games import roulette
from games.exceptions import *
from tornado.testing import AsyncTestCase, gen_test
from tornado.httpclient import AsyncHTTPClient

class TestRouletteWagers(unittest.TestCase):
	
	def test_wagerInvalid(self):
		with self.assertRaises(ValueError):
			w = roulette.Wager("Black 2", [2], "how much?")
		
	def test_wagerBasics(self):
		w = roulette.Wager("Red 1", [1], 35)
		self.assertEqual("Red 1", w.position)
		self.assertEqual(["1"], w.points)
		self.assertEqual(35.0, w.win)
		self.assertEqual(0.0, w.amount)
		
		# add some money to our bet
		self.assertEqual( (2,2), w.add(2) )
		self.assertEqual( (2.25,4.25), w.add(2.25) )
		self.assertEqual( 4.25, w.amount )
		
		# try removing some money
		self.assertEqual( (-0.25, 4), w.add(-0.25) )
		self.assertEqual( 4, w.amount )
		self.assertEqual( (-4, 0), w.add(-4) )
		self.assertEqual( 0, w.amount )
		
		# now adding some money and try taking more away
		self.assertEqual( (16, 16), w.add(16) )
		self.assertEqual( 16, w.amount )
		self.assertEqual( (-16, 0), w.add(-16.001) )
		self.assertEqual( 0.0, w.amount )
		
		# Look at a more complicated wager
		x = roulette.Wager("Street 1 2 3", [1, "2", 3], 11)
		self.assertEqual("Street 1 2 3", x.position)
		self.assertEqual(["1","2","3"], x.points)
		self.assertEqual(11.0, x.win)
		self.assertEqual(0.0, x.amount)
		
	def test_wagerPayouts(self):
		w = roulette.Wager("Street 1 2 3", [1, "2", 3], 11)
		# not bet on 1 2 3
		self.assertEqual( (0,0,"Street 1 2 3"), w.resolve("0") )
		# bet 5 and lose
		self.assertEqual( (5,5), w.add(5.0) )
		self.assertEqual( (-5, 0, "Street 1 2 3"), w.resolve("7") )
		# bet 9 and win
		self.assertEqual( (9,9), w.add(9.0) )
		self.assertEqual( (99, 9, "Street 1 2 3"), w.resolve("2") )
		# the 9 is still working on 1 2 3.  Add one more and win again
		self.assertEqual( (1, 10), w.add(1.0) )
		self.assertEqual( (110, 10, "Street 1 2 3"), w.resolve("3") )
		# now lose it!
		self.assertEqual( (-10, 0, "Street 1 2 3"), w.resolve("5") )
	
	def test_wagerPartage(self):
		w = roulette.Partage("Red", [1,3,5,7,9,12,15,16,18,19,21,23,35,27,30,32,34,36], 1)
		# losing numbers without bets
		self.assertEqual( (0,0,"Red"), w.resolve("0") )
		self.assertEqual( (0,0,"Red"), w.resolve("8") )
		# bet and win
		self.assertEqual( (5,5), w.add(5) )
		self.assertEqual( (5,5,"Red"), w.resolve("3") )
		# bet and lose
		self.assertEqual( (-5,0,"Red"), w.resolve("4") )
		# bet more and lose half
		self.assertEqual( (5,5), w.add("5") )
		self.assertEqual( (-2.5,2.5,"Red"), w.resolve("0") )
		# half again on 00
		self.assertEqual( (-1.25,1.25,"Red"), w.resolve("00") )
		# half again on 000
		self.assertEqual( (-.625,.625,"Red"), w.resolve("000") )
	
	def test_seat(self):
		s = roulette.Seat()
		
		with self.assertRaises(BetInvalidError):
			s.bet("Bad Wager", 20)
		
		self.assertEqual( (20, 20, "Red"), s.bet("Red", 20) )
		self.assertEqual( (5, 25, "Red"), s.bet("Red", 5) )
		
		# outcomes look like { won:float, amount:float, changes:[] }
		# changes are all (delta, working, position)
		outcome = s.resolve("1")
		self.assertEqual( 25, outcome['amount'] )
		self.assertEqual( 25, outcome['won'] )
		self.assertTrue( (25.0, 25.0, 'Red') in outcome['changes'] )
		self.assertEqual( 1, len(outcome['changes']) )
		self.assertEqual( 25, s.amount )
		self.assertEqual( 25, s.won )
		
		# We have 25 on Red
		# Let's put a little on a corner, and win with black
		self.assertEqual( (10, 10, "Corner 7 8 10 11"), s.bet("Corner 7 8 10 11", 10) )
		self.assertEqual( 35, s.amount )

		# Red will lose (-25), and the corner pays 8:1 (80)
		outcome = s.resolve("8")
		self.assertEqual( 55, outcome['won'] )
		self.assertEqual( 10, outcome['amount'] )
		self.assertTrue( (-25, 0, "Red") in outcome['changes'] )
		self.assertTrue( (80, 10, "Corner 7 8 10 11") in outcome['changes'] )
		self.assertEqual( 2, len(outcome['changes']) )
		self.assertEqual( 10, s.amount )
		self.assertEqual( 80, s.won ) # last spin's 25 plus this spin's 55
		
		# Take off the red, leave the corner working
		self.assertEqual( (0, 0, "Red"), s.bet("Red", -100000) )
		self.assertEqual( 10, s.amount )
		
		# And lose our corner
		outcome = s.resolve("0")
		self.assertEqual( -10, outcome['won'] )
		self.assertEqual( 0, outcome['amount'] )
		self.assertTrue( (-10, 0, 'Corner 7 8 10 11') in outcome['changes'] )
		self.assertEqual( 1, len(outcome['changes']) )
		self.assertEqual( 0, s.amount )
		self.assertEqual( 70, s.won )

		# Nothing ventured, nothing gained
		outcome = s.resolve("8")
		self.assertEqual( 0, outcome['won'] )
		self.assertEqual( 0, outcome['amount'] )
		self.assertEqual( 0, len(outcome['changes']) )
		self.assertEqual( 0, s.amount )
		self.assertEqual( 70, s.won )


class TestRouletteGame(AsyncTestCase):

	@gen_test
	def test_google(self):
		client = AsyncHTTPClient(self.io_loop)
		response = yield client.fetch("http://www.google.com")
		self.assertIn("Google", response.body)

