from django.shortcuts import render
from django.http import JsonResponse , HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


# Create your views here.

def Main(request):
    template = loader.get_template('index.html')
    context ={}

    return HttpResponse(template.render(context,request))

def Signup(request):
    response_data ={}
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['new-password']

        forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root','email', 'user', 'join', 'sql', 'static', 'python', 'delete']
        if username.lower() in forbidden_users:
            response_data['username_error'] = "The username entered is prohibibited,choose another one"
            response_data['register'] = "Error"
            return HttpResponse(JsonResponse(response_data))

        if '@' in username or '+' in username or '-' in username:
            response_data['username_error'] = "This is an Invalid user, Do not user these chars: @ , - , +"
            response_data['register'] = "Error"
            return HttpResponse(JsonResponse(response_data))

        if User.objects.filter(username__iexact=username).exists():
            response_data['username_error'] = "User with this username already exists."
            response_data['register'] = "Error"
            return HttpResponse(JsonResponse(response_data))

        new_user = User.objects.create(username=username,email=email)
        new_user.set_password(password)
        new_user.save()
        new_user.is_active=False
        log_user =authenticate(username=username,email=email)
        if log_user is not None:
            login(request,log_user)
        response_data['register']='Success'
        return HttpResponse(JsonResponse(response_data))
    return HttpResponse(JsonResponse(response_data))

def Login(request):
    username =password = ""
    response_data = {}
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        username = request.POST['current-username']
        password = request.POST['current-password']

        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                response_data = {'login': "Success"}
            else:
                response_data = {'user' : "not active"}
        else:
            response_data ={'user': "nouser"}
    else:
        username =password=''
        response_data = { 'login': "Failed"}
    return HttpResponse(JsonResponse(response_data))


















