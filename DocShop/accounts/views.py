from django.contrib.auth import get_user_model, login, logout, authenticate

from django.shortcuts import render, redirect
from stripe import Subscription

User = get_user_model()
# Create your views here.
def signup(request):
    if request.method == "POST":
        #traiter le formulaire
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        user = User.objects.create_user(username=username,
                                        password=password,
                                        email=email)
        login(request, user)
        return redirect('index')

    return render(request, 'signup.html')

def login_user(request):
    if request.method == "POST":
        #connecter l'utilisateur
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('index')
