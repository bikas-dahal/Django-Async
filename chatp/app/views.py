from django.shortcuts import render, redirect

from django.views import View

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Message, UserChannel

from django.db.models import Q



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
        
        return redirect('main')
    
    

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
                return redirect('home')
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
            print(user)
            if user is not None:
                login(request, user)
                return redirect('home')
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
        
        messages = Message.objects.filter(
            Q(sender=me, receiver=user) | Q(sender=user, receiver=me)
        ).order_by('date', 'time')
        
        data = {
            'type': 'receiver_function',
            'type_of_data': 'messages',
        }
        
        receiver_channel = UserChannel.objects.get(user=user)
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(receiver_channel.channel, data)
        
        unseen_message = Message.objects.filter(sender = me, receiver = user)
        print(unseen_message)
        unseen_message.update(has_been_seen = True)
            
        context = {
            'user': user,
            'me': me,
            'messages': messages
        }
        
        return render(request, 'app/chat_person.html', context)
    

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('main')