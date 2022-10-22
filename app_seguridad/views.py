from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse


# Verificar si el usuario esta autenticado en nuestra app web
def page_login(request):
    
    if request.user.is_authenticated:
        return redirect(reverse('Reportes:accounts_upload'))
    
        
    return render(request, 'security/login.html')

# Iniciar sesion 
def log_in(request):
    if (request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect(reverse('Reportes:accounts_upload'))   
        else:
            mensaje = 'Usuario o Contraseña Incorrecto'
            ctx = {
                "mensaje" : mensaje
            }
            return render(request, 'security/login.html', ctx)

    else:
        return redirect('/')


def log_out(request):
    logout(request)
    return redirect('/')