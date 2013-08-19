from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import datetime
from json import dumps

# Create your views here.

class BitcoinAddressField(forms.CharField):
    """ Form field and validator for Bitcoin addresses. """
    
    def validate(self, value):
        addressInfo = settings.BITCOIN_SERVICE.validateaddress( str(value) )
        if not addressInfo.get(u'isvalid'):
            raise forms.ValidationError( "Not a valid bitcoin address", code="bad_bitcoin_address")
        
class LoginForm(forms.Form):
    payout_address = BitcoinAddressField(max_length=37,min_length=32,required=True,label="Payout Address")
    password = forms.CharField(max_length=32, required=False, label="Password")
    
    
def login(request):
    """ Log in as a player, using a payout address.
    
    The view takes a LoginForm, and produces the following context variables:
        form: the login form
        
            payout_address: the customer's payout address
            
            password: the customer's password
            
            destination_url: the destination url, if login is successful.  
            Defaults to "player_login_successful"
            
        
            
    """
    err = None
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            clean = loginForm.cleaned_data
                
            # do some things here
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
