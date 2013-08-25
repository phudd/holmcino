import datetime
from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from json import dumps
from player.models import Player

# Create your views here.

class BitcoinAddressField(forms.CharField):
    """ Form field and validator for Bitcoin addresses. """
    def validate(self, value):
        addressInfo = settings.BITCOIN_SERVICE.validateaddress( str(value) )
        if not addressInfo.get(u'isvalid'):
            raise forms.ValidationError( "Not a valid bitcoin address", code="bad_bitcoin_address")
        
def login(request):
    """ Log in as a player, using a payout address.
    
    The view takes a LoginForm, and produces the following context variables:
        form: the login form
            payout_address: the customer's payout address
            password: the customer's password
            destination_url: the destination url, if login is successful.  
                Defaults to "player_home"
    """
    err = None
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            clean = loginForm.cleaned_data
            try:
                player = Player.objects.get(payout_address=clean['payout_address'])
                if player.password == clean['password']:
                    redirect('player_home')
                else:
                    err = 'You need to provide your password'
            except Player.DoesNotExist as ex:
                player = Player.createFromPayoutAddress(clean['payout_address'])
                player.save()
                redirect('player_home')
    else:
        loginForm = LoginForm()
    
    return render(  request, 
                    'player/login.html', 
                    {   'form':loginForm, 
                        'error':err
                    }
                )
    
def home(request):
    return HttpResponse('<html><body>home is where the crazy be</body></html>')

class LoginForm(forms.Form):
    """Defines the standard user login form.
    
    We have to put this AFTER the view functions because we use the reverse() method.  Turns
    out there is some circular-declaration problem otherwise.
    """
    payout_address = BitcoinAddressField(max_length=37,min_length=32,required=True,label="Payout Address")
    password = forms.CharField(max_length=32, required=False, label="Password")
    destination_url = forms.CharField(widget=forms.HiddenInput, required=False,initial=reverse('player_home'))
