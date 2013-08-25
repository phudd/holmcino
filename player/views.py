import datetime
import json
from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.db import IntegrityError
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
                player = Player.objects.get(name=clean['username'])
                if player.password == clean['password']:
                    request.session['player'] = player
                    return redirect(clean['destination_url'])
                else:
                    err = 'Username and password do not match.'
            except Player.DoesNotExist as ex:
                err = 'Username and password do not match.'
    else:
        loginForm = LoginForm()
    
    return render(request, 'player/login.html', {'form':loginForm,'error':err})

def create(request):
    err = None
    if request.method == 'POST':
        createForm = CreateForm(request.POST)
        if createForm.is_valid():
            clean = createForm.cleaned_data
            explayer = Player.objects.filter(name=clean['username'])
            if len(explayer):
                err = "Username is not available."
            else:
                player = Player.createFromUsername(clean['username'])
                player.save()
                return redirect(clean['destination_url'])
    else:
        createForm = CreateForm()
        
    return render( request, 'player/create.html', 
                   {    'form':createForm,
                        'error':err,
                   })

def logout(request):
    del(request.session['player'])
    return render( request, 'player/logout.html' )

# @require_player_login(reverse('player_login'))
def home(request):
    if request.session.get('player') == None:
        return redirect(reverse('player_login'))
    return HttpResponse('<html><body>home is where the crazy be</body></html>')

class CreateForm(forms.Form):
    username = forms.CharField(max_length=32, required=True, label="New User Name")
    destination_url = forms.CharField(widget=forms.HiddenInput, required=False,initial=reverse('player_home'))
    
class LoginForm(forms.Form):
    """Defines the standard user login form.
    
    We have to put this AFTER the view functions because we use the reverse() method.  Turns
    out there is some circular-declaration problem otherwise.
    """
    username = forms.CharField(max_length=32, required=False, label="Username")
    password = forms.CharField(max_length=32, required=False, label="Password")
    destination_url = forms.CharField(widget=forms.HiddenInput, required=False,initial=reverse('player_home'))
