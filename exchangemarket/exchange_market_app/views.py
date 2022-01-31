
from django.forms import forms
from django.shortcuts import redirect, render
from django.contrib import messages
from exchange_market_app.utils.Items import Items
from exchange_market_app import forms
from exchange_market_app import User

# Create your views here.

def index(request):
    items = Items.get_all_items()

    request.session["log_in_counter"] = 3

    try:
        user_id = request.session["user_id"]
    except KeyError:
        request.session["user_id"] = None
        user_id = request.session["user_id"]
    
    return render(request, 'index.html', {"items": items, "user_id": user_id})

def login(request):

    if request.method == "POST":
        if request.session["log_in_counter"] != 1:
            login_form = forms.LoginForm(request.POST)
            
            if login_form.is_valid():
                result = User.User.authenticate(login_form.data["email"], login_form.data["password"])    
                
                if result == User.UserStates.WRONG_CREDENTIALS:
                    request.session["log_in_counter"] -= 1
                    attempts = request.session["log_in_counter"]
                    messages.add_message(request, messages.ERROR, f"Wrong Credentials. Left attempts {attempts}")
                    return render(request, 'login.html', {"form": login_form})

                if result == User.UserStates.AUTHENTICATED:
                    request.session["log_in_counter"] = 3
                    messages.add_message(request, messages.SUCCESS, "Logged-in!")
                    request.session["user_id"] = User.User.get_primary_key()
                    return redirect("/")
            else:
                return render(request, 'login.html', {"form": login_form}) 
        else:
            request.session["log_in_counter"] = 3
            messages.add_message(request, messages.ERROR, "Too many attempt to log-in with wrong credentials")

            return redirect("/") 
    else:
        login_form = forms.LoginForm()

    return render(request, 'login.html', {"form": login_form})

def log_out(request):
    request.session["user_id"] = None
    messages.add_message(request, messages.SUCCESS, "Logged-out!")

    return redirect("/login/")

def inventory(request):
    items = None
    user_id = request.session["user_id"]
    items = User.User.get_inventory_items(user_id)
    return render(request, 'inventory.html',  {"items": items, "user_id": user_id})

def register(request):
    
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            if register_form.data["password"] != register_form.data["repeat_password"]:
                messages.add_message(request, messages.ERROR, f"Passwords don't match!")
                return render(request, 'register.html', {"form": register_form})
            else:
                name = register_form.data["name"]
                country = register_form.data["country"]
                username = register_form.data["username"]
                email = register_form.data["email"]
                password = register_form.data["password"]

                result = User.User.add_user(name, country, username, email, password)
            
            if result == User.UserStates.USER_EXISTS:
                messages.add_message(request, messages.ERROR, f"User already exists! Try to log in instead")
                return render(request, 'register.html', {"form": register_form})
            
            if result == User.UserStates.USERNAME_EXISTS:
                messages.add_message(request, messages.ERROR, f"Username already taken.")
                return render(request, 'register.html', {"form": register_form}) 

            if result == User.UserStates.USER_CREATED:
                messages.add_message(request, messages.SUCCESS, f"Registered successfully, try to sign in.")
                return redirect("/login/")

    return render(request, 'register.html')