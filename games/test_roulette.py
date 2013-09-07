import unittest
from games import roulette
from games.exceptions import *

class TestRouletteWagers(unittest.TestCase):
	
	def test_wagerBasics(self):
		w = roulette.Wager("Red 1", [1], 35)
		self.assertEqual("Red 1", w.position)
		self.assertEqual(["1"], w.points)
		self.assertEqual(35.0, w.win)
		self.assertEqual(1.0, w.lose)
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
		self.assertEqual(1.0, x.lose)
		self.assertEqual(0.0, x.amount)
		
	def test_wagerPayouts(self):
		w = roulette.Wager("Street 1 2 3", [1, "2", 3], 11)
		self.assertEqual( (0,0), w.resolve("0") )
		self.assertEqual( (5,5), w.add(5.0) )
		self.assertEqual( (-5, 0), w.resolve("7") )
		self.assertEqual( (9,9), w.add(9.0) )
		self.assertEqual( (99, 9), w.resolve("2") )
		self.assertEqual( (1, 10), w.add(1.0) )
		self.assertEqual( (110, 10), w.resolve("3") )
		