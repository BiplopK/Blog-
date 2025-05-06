from django.shortcuts import render,redirect
from django.views.generic import View
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

class UserRegistrationView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"registration/register.html",{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            first_name=form.cleaned_data.get('first_name')
            last_name=form.cleaned_data.get('last_name')
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            
            user=User.objects.filter(username=username)
            
            if user.exists():
                messages.info(request, "Username already taken")
                print("username already")
                return redirect('register')
            
            user=User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
                
            )
            user.set_password(password)
            user.save()
            messages.info(request, "User created succesfully!!!!")
            return redirect('login')
        return render(request,"registration/register.html",{'form':form})
    

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"registration/login.html",{'form':form})
    
    def post(self,request,*args,**kwargs):
        form= LoginForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            
            if not User.objects.filter(username=username).exists():
                form.add_error('username','Invalid Username')
                print("Invlaid username")
                return redirect('login')
            user=authenticate(request, username=username,password=password)
            
            if user is None:
                form.add_error('password','Invalid Password')
                print("Invalid password")
                return redirect('login')
            else:
                login(request,user)
                print(f"User {user.username} logged in successfully.")
                return redirect('blog-list')
        else:
            print("Form is not valid:", form.errors)
        return render(request, "registration/login.html",{'form':form})

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('blog-list')
