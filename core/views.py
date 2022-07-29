from django.shortcuts import render, redirect
from .models import NewUser
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.db.models import F
from django.contrib import messages



# Create your views here.

def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['user_name']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('wallet')

    return render(request, 'core/register.html', {'page': page})


def wallet(request): 
    if request.method == 'POST':

        username = request.POST['name']
        money = request.POST['money']
        login_model = NewUser
   
        
        check_existing = login_model.objects.filter(email=username).exists()
        if check_existing:

            finduser = NewUser.objects.get(email=username)
            currentuser = NewUser.objects.get(email=request.user.email)

            
            if int(money) >= 10000 and int(money) <= 100000:
                if int(money) > int(currentuser.money):
                    print("you dont have enough money")
                else:
                    currentuser.money = F('money') - (int(money) + 200)
                    finduser.money = F('money') + money
                    messages.success(request, f"transaction fee of Rwf 200")

                
            elif int(money) > 100000:
                  if int(money) > int(currentuser.money):
                    print("you dont have enough money")
                  else:

                    currentuser.money = F('money') - (int(money) + 1000)
                    finduser.money = F('money') + money
                    messages.success(request, f"transaction fee of Rwf 1,000")
         
            else:
                currentuser.money = F('money') - (money)
                finduser.money = F('money') + money
           
                messages.success(request, f"no transaction fee")

            giveit = finduser.save()
            removeit = currentuser.save()
            if(giveit):
                print("save")
                return redirect('wallet')


        else:
            messages.warning(request, f"User does not Exists")

    return render(request, 'core/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')




def registerUser(request):
    page = 'register'

    login_model = NewUser()

    if request.method == 'POST':
        
        
        regusername = request.POST['user_name']
        regemail = request.POST['email']
        regpassword1 = request.POST['password1']
        regpassword2 = request.POST['password2']

        if regpassword1 == regpassword2:

            check_user = NewUser.objects.filter(email=regemail).exists()
            if check_user:
                messages.warning(request, f"user exists")
                return redirect('register')

            else:
                 saveuser = NewUser.objects.create_user(user_name=regusername, email=regemail, first_name='',  password=regpassword1)
            return redirect('login')
        else:
            messages.warning(request, f"Password Don't match")
            return redirect('register')
       
    return render(request, 'core/register.html')




