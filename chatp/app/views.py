from django.shortcuts import render, redirect

from django.views import View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages



class Main(View):
    def get(self, request):
        
        if request.user.is_authenticated:
            return redirect('home')
        
        return render(request, 'app/main.html')


class Home(View):
    def get(self, request):
        
        if request.user.is_authenticated:
            context = {
                'user': request.user,
                'users': User.objects.all()
            }
            return render(request, 'app/home.html', context=context) # redirect('home')
        
        return redirect(request, 'app/main.html', context=context)
    

class Login(View):
    def get(self, request):
        return render(request, 'app/login.html')
    
    def post(self, request):
        data = request.POST.dict()
        
        print(data)
        
        context = {}
        
        print(data)
        try:
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat')
            else:
                messages.info(request, 'Credentials are Invalid')
                return redirect('login')
            
        except Exception as e:
            context['error'] = str(e)
            
        return render(request, 'app/login.html', context)
    

class Register(View):
    def get(self, request):
        return render(request, 'app/register.html')
    
    def post(self, request):
        data = request.POST.dict()
        
        context = {}
        
        print(data)
        try:
            first_name= data.get('first_name')
            last_name = data.get('last_name')
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            
            user = User()
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
            
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                redirect('chat')
            else:
                messages.info(request, 'Credentials are Invalid')
                return redirect('register')
            
        except Exception as e:
            context['error'] = str(e)
        
        return render(request, 'app/register.html', context)
            
            
class Chat(View):
    
    
    def get(self, request, id):
        user = User.objects.get(id=id)
        me = request.user
        
        context = {
            'user': user,
            'me': me
        }
        
        return render(request, 'app/chat_person.html', context)
    

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('main')