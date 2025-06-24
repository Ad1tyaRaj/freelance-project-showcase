from django.shortcuts import render
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import AndroidApp, UserTask, User
from .forms import EditProfileForm,AddTaskForm
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from rest_framework import viewsets
from .serializers import UserSerializer, AndroidAppSerializer, UserTaskSerializer
from rest_framework.permissions import IsAdminUser

# Create your views here.

#Api
    
class AndroidAppViewSet(viewsets.ModelViewSet):
    queryset = AndroidApp.objects.all()
    serializer_class = AndroidAppSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class UserTaskViewSet(viewsets.ModelViewSet):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    
    
def api_view(request):
    return redirect('/get/token')
    
#End Api

#Home
def Home(request):
    context = {
        'apps': AndroidApp.objects.all()
    }
    return render(request, 'Home/index.html', context)


#Signup
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2'] 
        if password1 == password2:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "You have successfully signed up!")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match")
            return render(request, 'Home/signup.html')
    else:
        return render(request, 'Home/signup.html')

#Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)    
            return redirect('home')
        else:
            messages.warning(request, "Your Username and Password is Incorrect !!!")
            return render(request, 'Home/login.html')
    return render(request, 'Home/login.html')

#profile
@login_required
def profile_view(request):
    context = {
        'total_posts': 0,  # You can replace with actual count
        'total_views': 0,  # You can replace with actual count
        'join_date': request.user.date_joined.strftime('%B %Y')
    }
    return render(request, 'Home/profile.html', context)



#Dashboard
@login_required
def dashboard_view(request):
    return render(request, 'Home/Dashboard.html')

#Admin Dashboard
@login_required
def admin_dash_view(request):
    return render(request, 'Home/Admin-dash.html')

#Task
# @login_required
def task_view(request):
    context = {
        'apps': AndroidApp.objects.all()
    }
    return render(request, 'Home/Task.html', context)

#Screenshot
# Submit Task
@login_required
def submit_view(request):
    if request.method == 'POST' and 'screenshot' in request.FILES:
        screenshot = request.FILES['screenshot']
        UserTask.objects.create(user=request.user, screenshot=screenshot)
        messages.success(request, "Screenshot submitted successfully!")
        return redirect('task')

    context = {'apps': AndroidApp.objects.all()}
    return render(request, 'Home/Task.html', context)


#Points
@login_required
def points_view(request):
    context = {
        'total_points': UserTask.objects.filter(user=request.user).count()
    }
    return render(request, 'Home/Task.html', context)

#Edit Profile
@login_required
def admin_setting(request):
    users = User.objects.all()
    return render(request,'Home/Admin-settings.html',{'users':users})


#Edit User
@login_required
def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if user.is_active == False:
                messages.success(request, "User profile deleted successfully!")
                return redirect('login')
            if request.user.is_superuser:
                return redirect('admin_settings')
            else:
                messages.success(request, "User profile updated successfully!")
                return redirect('profile')
        elif 'username' in form.errors:
            messages.error(request, "Username already exists. Please choose a different username.")
        elif 'email' in form.errors:
            messages.error(request, "Email already exists. Please choose a different email.")  
        else:
            messages.error(request, "Failed to update profile. Please try again.")
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'Home/Edit.html', {'form': form})

#Add Task
@login_required
def add_task(request):
    context = {
        'form': AddTaskForm(),
        'apps': AndroidApp.objects.all()
    }
    if request.method == 'POST':
        form = AddTaskForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Task added successfully!")
            return redirect('task')
        else:
            messages.error(request, "Failed to add task. Please try again.")
    return render(request, 'Home/Add-Task.html', context)


#Edit Task
@login_required
def edit_task(request, task_id):
    task = AndroidApp.objects.get(id=task_id)
    context = {
        'task': task,
        'apps': AndroidApp.objects.all()
    }
    if request.method == 'POST':
        form = AddTaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('task')
        else:
            messages.error(request, "Failed to update task. Please try again.")
    else:
        form = AddTaskForm(instance=task)
    return render(request, 'Home/Edit-Task.html', context)

#Delete Task
@login_required
def delete_task(request, task_id):
    task = AndroidApp.objects.get(id=task_id)
    task.delete()
    messages.success(request, "Task deleted successfully!")
    return redirect('task')


#Delete User
@login_required
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('admin_settings')



#Logout
@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Successfully logged out!")
    return redirect('home')
