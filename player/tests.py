"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.

Test cases I can think of
	new payout address
	new invalid payout address
	try to use a deposit address as a payout address
	log in with an existing payout address and password
	log in with an existing payout address and no password
	log in with an existing payout address, no password, and the payout can't be made because there are pending transactions.
"""

from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
