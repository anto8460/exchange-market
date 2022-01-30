
from django.forms import forms
from django.shortcuts import redirect, render
from django.contrib import messages
from exchange_market_app.utils.get_items import get_all_items
from exchange_market_app import forms
from exchange_market_app import User

# Create your views here.

def index(request):
    items = get_all_items()
    user_id = request.session["user_id"]
    return render(request, 'index.html', {"items": items, "user_id": user_id})

def login(request):

    user = User.User()

    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        
        if login_form.is_valid():
            result = user.authenticate(login_form.data["email"], login_form.data["password"])    
            
            if result == User.UserStates.EXCEED_TRIES:
                messages.add_message(request, messages.ERROR, "Too many attempt to log-in with wrong credentials")
                User.User.reload_counter()
                return redirect("/")
            
            if result == User.UserStates.WRONG_CREDENTIALS:
                messages.add_message(request, messages.ERROR, f"Wrong Credentials. Left tries: {User.User.counter}")
                return render(request, 'login.html', {"form": login_form})

            if result == User.UserStates.AUTHENTICATED:
                messages.add_message(request, messages.SUCCESS, "Logged-in!")
                request.session["user_id"] = user.get_primary_key()
                return redirect("/")
        else:
             return render(request, 'login.html', {"form": login_form})  
    else:
        login_form = forms.LoginForm()

    return render(request, 'login.html', {"form": login_form})

def log_out(request):
    request.session["user_id"] = None
    messages.add_message(request, messages.SUCCESS, "Logged-out!")
    return redirect("/login/")
