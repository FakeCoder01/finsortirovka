from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Profile, MFILoan, UploadedDocument
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from dash.models import LoanProcess
# Create your views here.


def login_user(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            # User is authenticated
            login(request, user)
            messages.success(request, "Login successful")
            if Profile.objects.filter(user=request.user, profile_active=True).exists():
                return redirect('/')
            return redirect(f'/profile?perform=new')
        messages.error(request, "Invalid credentials")        
        return redirect("/login?msg=invalid credentials")    
    return render(request, 'app/auth/login.html', {"page_title" : "Login"})


def signup_user(request):
    try:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']

            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if confirm_password != password:
                messages.error(request, "Password did not match")
                return redirect("/signup?res=Password did not match")

            full_name = first_name+' '+last_name
            username = email

            # create a user account for the student
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                new_profile = Profile.objects.create(
                    user = user,
                    full_name = full_name
                )
                messages.success(request, 'Account has been created')
                return redirect(f'/profile?res=account created successfully&perform=new')

            messages.error(request, 'User not logged in')
            return redirect("/signup?res=User not activated")

        return render(request, "app/auth/signup.html", {"page_title" : "Sign up"})
    except Exception as err:
        print(err)
        messages.error(request, 'Account creation Failed')
        return redirect("/signup?res=Something went wrong")

@login_required(login_url="/login")
def manage_profile(request):
    try:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            gender = request.POST['gender']
            phone = request.POST['phone']
            address = request.POST['address']
            full_name = first_name+' '+last_name

            # create/update a user profile for the user
            profile = request.user.userprofile
            profile.full_name = full_name
            profile.gender = gender
            profile.phone = phone
            profile.address = address
            profile.profile_active = True

            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            
            user.save()
            profile.save()
            messages.success(request, 'Profile has been saved')

            try:
                if request.GET['perform'] == 'new':
                    return redirect(f'/?perform=done')
            except:
                return redirect(f'/profile?res=Profile saved successfully')
        context = {
            "page_title" : "Profile",
        }
        return render(request, "app/auth/profile.html", context)
    except Exception as err:
        ###
        print(err)
        messages.error(request, 'Profile creation Failed')
        return redirect("/?l=")

def logout_user(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('/')

@login_required(login_url="/login")
def mfi_form(request):
    try:
        if request.method == 'POST':
            legal_status_of_user = request.POST['legal_status_of_user']
            confirm_income_source = request.POST.getlist('confirm_income_source')
            age_of_user = request.POST['age_of_user']
            loan_amount = request.POST['loan_amount']
            loan_tenure_in_days = request.POST['loan_tenure_in_days']
            loan_type = request.POST['loan_type']
            documents = request.POST.getlist('documents')
            method_of_receiving_money = request.POST.getlist('method_of_receiving_money')
            region = request.POST['region']
            message = request.POST['message']

            new_mfi_loan = MFILoan.objects.create(
                user = request.user.userprofile,
                legal_status_of_user = legal_status_of_user,
                confirm_income_source = confirm_income_source,
                age_of_user = int(age_of_user),
                loan_amount = loan_amount,
                loan_tenure_in_days = int(loan_tenure_in_days),
                loan_type = loan_type,
                method_of_receiving_money = method_of_receiving_money,
                region = region,
                message = message,
            )

            for file in documents:
                temp_x = UploadedDocument.objects.create(
                    profile = request.user.userprofile,
                    document_name = str(file),
                    doc_id=get_random_string(6)
                )
                new_mfi_loan.documents.add(temp_x)
            new_mfi_loan.save()  

            LoanProcess.objects.create(
                user = new_mfi_loan.user,
                loan = new_mfi_loan
            )

            return redirect('/dash?from=new')  
        return render(request, 'app/form/mfi.html')    
    except Exception as err:
        print(err)  
        return redirect('/?error')  

@login_required(login_url="/login")
def dashboard(request):
    loans = MFILoan.objects.filter(user=request.user.userprofile)
    context = {
        'applications' : loans,
    }
    return render(request, 'app/form/dash.html', context)

@login_required(login_url="/login")
def loan_details(request, loan_id):
    if not MFILoan.objects.filter(loan_id=loan_id, user=request.user.userprofile).exists():
        return redirect('/dash?error=mismatch')
    loan = MFILoan.objects.get(loan_id=loan_id, user=request.user.userprofile)   
    v = loan.confirm_income_source.replace('[', '') 
    v = v.replace("'", "")
    v = v.replace("]", "")

    w = loan.method_of_receiving_money.replace('[', '') 
    w = w.replace("'", "")
    w = w.replace("]", "")
    context  = {
        'application' : loan,
        'confirm_income_source' : v,
        'method_of_receiving_money' : w
    }    
    return render(request, 'app/form/form-detail.html', context)

@login_required(login_url="/login")
def upload_doc(request, loan_id):
    if not MFILoan.objects.filter(loan_id=loan_id, user=request.user.userprofile).exists():
        return redirect('/dash?error=mismatch')
    loan = MFILoan.objects.get(loan_id=loan_id, user=request.user.userprofile)    
    if request.method == 'POST':
        for x in loan.documents.all():
            try:
                file = request.FILES[str(x.doc_id)]
                x.media = file
                x.save()
            except:
                pass
        
        messages.success(request, "Documents uploaded successfully")       
    context = {
        'loan' : loan
    }    
    return render(request, 'app/form/upload.html', context)


def home_page(request):
    return render(request, 'app/index.html')