from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def auth_login_view(request):
    return render(request, 'login.html')

def auth_loginCredentials(request):
    if request.method == 'POST':
        try:
            user = authenticate(request, username=request.POST.get('email'), password=request.POST.get('pass'))
            if user is not None:
                login(request, user)
                return redirect('/shop')  
            else:
                return render(request, 'login.html', {'error': "Credenciales incorrectas"})
        except:
            return render(request, 'login.html', {'error': "Error de autenticación"})  
    else:
        return render(request, 'login.html')

@login_required
def auth_logoutCredentials(request):
    logout(request)
    return redirect('/shop')

def auth_signup(request):
    return render(request, 'signup.html')

def auth_signupCredentials(request):
    if request.method == 'POST':
       try:
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 != pass2:
            return render(request, 'signup.html', {'error': "Las contraseñas no coinciden"})
        else:
            user = User.objects.create_user(
                username=request.POST.get('email'),
                password=pass1,
                email=request.POST.get('email'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name')
            )
            user.save()
            login(request, user)
            return redirect('/shop')
       except:
            return render(request, 'signup.html', {'error': "El usuario ya existe"})
