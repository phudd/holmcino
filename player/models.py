import os
import time
from hashlib import sha256
from django.db import models
from django.conf import settings
import base58

# Create your models here.

class Player(models.Model):
    player_id = models.CharField(max_length=16,primary_key=True)
    name = models.CharField(max_length=32,unique=True)
    payout_address = models.CharField(max_length=34,null=True,blank=True)
    deposit_address = models.CharField(max_length=34,null=True,blank=True)
    password = models.CharField(max_length=32)
    
    @staticmethod
    def createFromUsername(username):
        pid = generateRandomString()
        pw = generateRandomString()
        plyr = Player( player_id=pid, name=username, password=pw )
        return plyr
        
        
class Profile(models.Model):
    player = models.ForeignKey(Player,primary_key=True)
    name = models.CharField(max_length=32,null=True)

def generateRandomString(len=8):
    return base58.b58encode(sha256(os.urandom(512)).digest())[:len]

