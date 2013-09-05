import unittest
from games import craps
from games.exceptions import *

class TestCrapsWagers(unittest.TestCase):

	def test_pass(self):
		# You can't create a line bet when there is a point
		with self.assertRaises(craps.LineOnPointError):
			pb = craps.PassWager(1, 8)
		
		# Check that the factory works, and create a valid line bet
		pb = craps.betFactory.create('pass', 1, 0)
		self.assertEqual(1, pb.amount)
		self.assertEqual(0, pb.point)
		
		pb.add(2, 0)
		self.assertEqual(3, pb.amount)
		self.assertEqual(0, pb.point)
		
		# Crap out
		self.assertEqual(-3, pb.eval(0, 1, 1))
		self.assertEqual(-3, pb.eval(0, 1, 2))
		self.assertEqual(-3, pb.eval(0, 6, 6))
		
		# Natural
		self.assertEqual(6, pb.eval(0, 3, 4))
		self.assertEqual(6, pb.eval(0, 6, 5))
		
		# We should still be able to add to our bet, since there is no point
		pb.add(1, 0)
		self.assertEqual(4, pb.amount)
		self.assertEqual(0, pb.point)
		
		# establish a point of 5
		self.assertEqual(0, pb.eval(0, 2, 3))
		self.assertEqual(5, pb.point)
		
		# We should raise an error if we try to raise the bet now
		with self.assertRaises(craps.LineOnPointError):
			pb.add(2, 5)
		
		# our bet is 4 and the point is 5
		self.assertEqual(-4, pb.eval(5, 2, 5))
		self.assertEqual(-4, pb.eval(5, 5, 2))
		self.assertEqual(0, pb.eval(5, 1, 2))
		self.assertEqual(0, pb.eval(5, 6, 5))
		self.assertEqual(0, pb.eval(5, 4, 4))
		self.assertEqual(8, pb.eval(5, 3, 2))
		
		# Pass bets keep their own point internally, once set.  The game can send any point
		# it wants and it won't matter.
		self.assertEqual(8, pb.eval(8, 3, 2))
		
	def test_dontpass(self):
		# You can't create a line bet when there is a point
		with self.assertRaises(craps.LineOnPointError):
			pb = craps.DontPassWager(1, 8)
		
		# Check that the factory works, and create a valid line bet
		pb = craps.betFactory.create('dontpass', 1, 0)
		self.assertEqual(1, pb.amount)
		self.assertEqual(0, pb.point)
		
		pb.add(2, 0)
		self.assertEqual(3, pb.amount)
		self.assertEqual(0, pb.point)
		
		# Crap out wins or pushes
		self.assertEqual(6, pb.eval(0, 1, 1))
		self.assertEqual(6, pb.eval(0, 1, 2))
		self.assertEqual(0, pb.eval(0, 6, 6))
		self.assertEqual(0, pb.point) # 12 is a push, with no point established
		
		# Natural
		self.assertEqual(-3, pb.eval(0, 3, 4))
		self.assertEqual(-3, pb.eval(0, 6, 5))
		self.assertEqual(0, pb.point)
		
		# We should still be able to add to our bet, since there is no point
		pb.add(1, 0)
		self.assertEqual(4, pb.amount)
		self.assertEqual(0, pb.point)
		
		# establish a point of 10
		self.assertEqual(0, pb.eval(0, 5, 5))
		self.assertEqual(10, pb.point)
		
		# We should raise an error if we try to raise the bet now
		with self.assertRaises(craps.LineOnPointError):
			pb.add(2, 10)
		
		# our bet is 4 and the point is 10
		self.assertEqual( 8, pb.eval(10, 2, 5))
		self.assertEqual( 8, pb.eval(10, 5, 2))
		self.assertEqual( 0, pb.eval(10, 1, 2))
		self.assertEqual( 0, pb.eval(10, 6, 5))
		self.assertEqual( 0, pb.eval(10, 4, 4))
		self.assertEqual(-4, pb.eval(10, 6, 4))
		
		# Pass bets keep their own point internally, once set.  The game can send any point
		# it wants and it won't matter.
		self.assertEqual(-4, pb.eval(8, 4, 6))

