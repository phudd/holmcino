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
        genstr = settings.SECRET_KEY + str(time.time()) # float down to 10-usec
        genstr = sha256(genstr).digest()
        genstr = base58.b58encode(genstr)
        depAddr = settings.BITCOIN_SERVICE.getaccountaddress(settings.DEPOSIT_ACCOUNT)
        
        plyr = Player(player_id=genstr[:5],payout_address=address,deposit_address=depAddr,password=genstr[-5:])
        plyr.save()
        return plyr

class Profile(models.Model):
    player = models.ForeignKey(Player,primary_key=True)
    name = models.CharField(max_length=32,null=True)
    