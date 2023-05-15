from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages
from blog.models import CustomUser
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')


    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist!!')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentails!!")


    return render(request, 'account/login.html')


def logoutUser(request):
    logout(request)
    return redirect('account:login')


def register_page(request):
    auth_form = CustomUserCreationForm()
    if request.method == 'POST':
        auth_form = CustomUserCreationForm(request.POST)
        if auth_form.is_valid():
            auth_form.save()
            messages.success(request, 'Account has been created successfully')
            return redirect('account:login')
        else:
            messages.error(request, "Oops!, An error ocurred ")
    else:
        auth_form = CustomUserCreationForm()
    
    return render(request, 'account/register.html', {'auth_form': auth_form})