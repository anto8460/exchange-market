
from django.forms import forms
from django.shortcuts import redirect, render
from django.contrib import messages
from exchange_market_app.utils.Items import Items, ItemsState
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

def create_item(request):

    if request.method == "POST":
        create_item_form = forms.CreateItemForm(request.POST)
        print(request.POST)
        print(create_item_form.is_valid())
        if create_item_form.is_valid():
            user_id = request.session["user_id"]
            name =  create_item_form.data["name"]
            description = create_item_form.data["description"]

            free = True if "check" in create_item_form.data else False

            result = Items.create_item(user_id, name, description, free)
            if (result == ItemsState.ITEM_CREATED):
                messages.add_message(request, messages.SUCCESS, f"Item Succesfully added")
                return redirect("/inventory")


    return render(request, "create_item.html")

def view_item(request, id):
    user_id = request.session["user_id"]
    item, state = Items.get_item(id)
    item_is_from_inventory = Items.is_item_from_inventory(id, user_id)

    if state == ItemsState.ITEM_NOT_FOUND:
        messages.add_message(request, messages.ERROR, f"Item not found")
        return render(request, "item.html", {"item": item})

    if request.method == 'POST':
        if "delete_item" in request.POST:
            status = Items.delete_item(id)
            if status == ItemsState.ITEM_DELETED:
                return redirect("/inventory")
            else:
                messages.add_message(request, messages.ERROR, f"System Error")

    return render(request, "item.html", {"item": item[0], "user_id": user_id, "item_is_from_inventory": item_is_from_inventory})

def edit_item(request, id):
    form = dict()
    item, status = Items.get_item(id)
    
    form["name"] = item[0].name
    form["description"] = item[0].description
    form["free"] = item[0].is_free

    if request.method == "POST":
        edit_item_form = forms.CreateItemForm(request.POST)

        if edit_item_form.is_valid():
            user_id = request.session["user_id"]
            name =  edit_item_form.data["name"]
            description = edit_item_form.data["description"]

            free = True if "check" in edit_item_form.data else False

            print(edit_item_form)
            result = Items.edit_item(id, name, description, free)
            
            if (result == ItemsState.ITEM_EDITED):
                messages.add_message(request, messages.SUCCESS, f"Item Succesfully edited!")
                return redirect("/inventory")

    return render(request, "edit_item.html", {"name": form["name"], "description": form["description"], "free": form["free"]})

def create_offer(request):

    return render(request, "create_offer.html")