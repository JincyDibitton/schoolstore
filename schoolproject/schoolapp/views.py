from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.mail import message
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from.forms import StudentForm
from .models import Department,Courses,Student
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request,'index.html')
def register(request):
    if request.method =='POST':
        username=request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['password1']
        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username  already exists')
                return redirect('register')

            else:
                user=User.objects.create_user(username=username,password=password)
                user.save();
                return redirect('login')
        else:
            messages.info(request,'password not matching')
            return redirect('register')
        return redirect('/')
    return render(request,'register.html')

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('student_add')
        else:
            messages.info(request,'Invalid Credential')
            return redirect('login')
    return render(request,'login.html')
def logout(request):
    auth.logout(request)
    return redirect('/')

def student_create_view(request):
    form = StudentForm()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            message.info(request,"your form is saved")
            return redirect('student_add')
    return render(request, 'requirements.html', {'form': form})


def student_update_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(instance=student)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_change', pk=pk)
    return render(request, 'requirements.html', {'form': form})

def load_courses(request):
    department_id = request.GET.get('department_id')
    courses = Courses.objects.filter(department_id=department_id).all()
    return render(request,'student/courses_dropdown_list_options.html', {'courses':courses})
    # return JsonResponse(list(courses.values('id', 'name')), safe=False)
def order(request):
    return render(request,'order.html')