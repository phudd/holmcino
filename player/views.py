from django import forms
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import datetime
from bitcoin import Bitcoin
from jsonrpc.proxy import ServiceProxy
from json import dumps
from bitcoin import Bitcoin

# Create your views here.

class LoginForm(forms.Form):
    payout_address = forms.CharField(max_length=37,min_length=32,required=True,label="Payout Address")
	
def login(request):
    quote = 'Ergggg!'
    err = None
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            clean = loginForm.cleaned_data
            btc = Bitcoin(settings.BITCOIN_URL)
            addressInfo = btc.validateaddress(clean['payout_address'])
            quote = dumps(addressInfo)
            # do some things here
    else:
        loginForm = LoginForm()
    
    return render(request, 'player/login.html', {'form':loginForm,'quote':quote, 'error':err})
    
def home(request):
    return HttpResponse('<html><body>home is where the crazy be</body></html>')