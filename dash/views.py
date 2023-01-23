from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from core.models import Profile, MFILoan, UploadedDocument
from .models import LoanProcess
from django.contrib import messages

# Create your views here.

@staff_member_required(login_url='/manage/login')
def home_page(request):
    return 

def login_user(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user and user.is_staff:
            # User is authenticated
            login(request, user)
            messages.success(request, "Login successful")
            return redirect(f'/manage/?login=true')
        messages.error(request, "Invalid credentials")        
        return redirect("/manage/login?msg=invalid credentials")    
    return render(request, 'manage/auth/login.html') 


def logout_user(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('/manage/?logout=True') 

@staff_member_required(login_url='/manage/login')
def mfi_applications(request):
    return render(request, )

@staff_member_required(login_url='/manage/login')
def processes(request):
    return 

@staff_member_required(login_url='/manage/login')
def mfi_application_info(request, loan_id):
    return 

@staff_member_required(login_url='/manage/login')
def process_info(request, loan_id):
    return 

@staff_member_required(login_url='/manage/login')
def mfi_doc(request, loan_id):
    return 

@staff_member_required(login_url='/manage/login')
def process_doc(request, loan_id):
    return     

