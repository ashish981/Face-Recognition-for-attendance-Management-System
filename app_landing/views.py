from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

from tkinter import *
from tkinter import messagebox

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('home')
            else:
                #messages.info(request, 'Invalid username or password')
                window = Tk()
                window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
                window.withdraw()

                messagebox.showerror('Invalid', 'Invalid username or password')

                window.deiconify()
                window.destroy()
                window.quit()

                return redirect('/')


        else:
            return render(request, 'login.html')

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
