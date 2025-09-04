from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User

def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Já existe uma conta com este e-mail.")
            return redirect("register")

        hashed_password = make_password(password)
        user = User.objects.create(email=email, password=hashed_password)
        user.save()

        messages.success(request, "Conta criada com sucesso! Faça login.")
        return redirect("login")

    return render(request, "register.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                request.session["user_id"] = str(user.id)
                request.session["user_email"] = user.email
                return redirect("home")
            else:
                messages.error(request, "Senha inválida.")
        except User.DoesNotExist:
            messages.error(request, "E-mail não encontrado.")

        return redirect("login")

    return render(request, "login.html")

def logout(request):
    request.session.flush()
    return redirect("login")
