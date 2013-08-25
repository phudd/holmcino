import os
import time
from hashlib import sha256
from django.db import models
from django.conf import settings
import base58

# Create your models here.

class Player(models.Model):
    player_id = models.CharField(max_length=16,primary_key=True)
    payout_address = models.CharField(max_length=34,unique=True)
    deposit_address = models.CharField(max_length=34,unique=True)
    password = models.CharField(max_length=32)
    
    @staticmethod
    def createFromPayoutAddress(address):
        """Create a player for the given payout address.
        
        Does not save the new player ... simply returns it.  You must still call save().
        
        It generates a random id, and password, and creates a new deposit address too.
        """
        pid = generateRandomString(8)
        pw = generateRandomString(8)
        
        plyr = Player( player_id=pid, payout_address=address, password=pw)
        return plyr
        
class Profile(models.Model):
    player = models.ForeignKey(Player,primary_key=True)
    name = models.CharField(max_length=32,null=True)

def generateRandomString(len=8):
    return base58.b58encode(sha256(os.urandom(512)).digest())[:len]

