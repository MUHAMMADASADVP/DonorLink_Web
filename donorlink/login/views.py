from django.contrib.auth import authenticate, login, logout,get_user
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.cache import cache_control
import json

from .models import User,Donor,Hospital,Bloodbank,Patient,Bankstock

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_view(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user= User.objects.get(username=username)
            if user.is_active == False:
                return render(request, "login.html", {
                    "message": "User Waiting For approval"
                })
        except:
            user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return render(request,"home.html")
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        Phoneno = request.POST["phoneno"]
        Age  = request.POST["age"]
        City = request.POST["city"]
        Document = request.FILES["doc"]
        Bg = request.POST["bloodgroup"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "dsignup.html",{
                "message": "missmatch passwords....."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.role='donor'
            user.save()

            donor  = Donor.objects.create(uuser = user,phoneno = Phoneno ,age = Age,bg = Bg,city = City,document = Document)
            donor.save()
        except IntegrityError:
            return render(request, "dsignup.html",{
                "message":"User Already Exists"
            })
        login(request, user)
        return render(request, "home.html",{
            "user":user
        })
    else:
        return render(request, "dsignup.html")

def hsignup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        Phoneno = request.POST["phoneno"]
        City = request.POST["city"]
        Document = request.FILES["doc"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "signup.html",{
                "message": "missmatch passwords....."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.role='hospital'
            user.is_active=False
            user.save()

            hospital  = Hospital.objects.create(uuser = user,phoneno = Phoneno ,city = City,document = Document)
            hospital.save()
        except IntegrityError:
            return render(request, "hsignup.html",{
                "message":"User Already Exists"
            })

        return render(request, "hsignup.html",{
            "message":"Registration Successfull Wait for Approval"
        })
    else:
        return render(request, "hsignup.html")
    
def bsignup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        Phoneno = request.POST["phoneno"]
        City = request.POST["city"]
        Document = request.FILES["doc"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "bsignup.html",{
                "message": "missmatch passwords....."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.role='bloodbank'
            user.is_active=False
            user.save()

            bloodbank  = Bloodbank.objects.create(uuser = user,phoneno = Phoneno ,city = City,document = Document)
            bloodbank.save()

            bstock = Bankstock.objects.create(bank = bloodbank)
            bstock.save()

        except IntegrityError:
            return render(request, "bsignup.html",{
                "message":"User Already Exists"
            })

        return render(request, "bsignup.html",{
            "message":"Registration Successfull Wait for Approval"
        })
    else:
        return render(request, "bsignup.html")

@login_required(login_url='login')
def update(request):
    rusr = get_user(request)
    user = User.objects.get(username = rusr.username)
    if request.method == 'POST':
        Email = request.POST["email"]
        Phoneno = request.POST["phoneno"]
        City = request.POST["city"]
        Age = request.POST["age"]
        Dist = request.POST['district']
        bld = request.POST["bloodgroup"]
        Dnr = user.donor
        Dnr.bg = bld
        Dnr.age = Age
        Dnr.city = City
        Dnr.district = Dist
        Dnr.phoneno = Phoneno
        user.email = Email
        Dnr.save()
        user.save()

        return render(request, "update.html", {
            "user":User.objects.get(username = get_user(request)),
            "message": "Updated Successfully"
        })

    else:
        return render(request, "update.html", {
            "user":user,
        })
    
@login_required(login_url='login')
def bstock(request):
    if request.method == 'POST':

        bg = request.POST["bloodgroup"]
        value = request.POST["bvalue"]

        user = get_user(request)
        Bankstockobj =  user.bloodbank.bankstock
        setattr(Bankstockobj,bg , value)
        Bankstockobj.save()

        messages.success(request,"updated successfully")

        return redirect(bstock)
    else:
        return render(request,'bstock.html')
    
@login_required(login_url='login')
def addpatient(request):
    if request.method == "POST":
        Pname = request.POST["name"]
        Pur = request.POST["purpose"]
        Dname = request.POST["doctor"]
        Email = request.POST["email"]
        Phoneno = request.POST["phoneno"]
        City = request.POST["city"]
        Age = request.POST["age"]
        Dist = request.POST['district']
        bld = request.POST["bloodgroup"]
        Document = request.FILES["doc"]

        user = get_user(request)
        hos = user.hospital

        patient = Patient.objects.create(hosp = hos, name=Pname, purpose= Pur, doctor= Dname,phoneno= Phoneno,email= Email,age= Age,bg= bld,district= Dist,city= City,document= Document)
        patient.save()



        return render(request, "addpatient.html" ,{
            "message": "Patient registered successfully"
        })
    else:
        return render(request,"addpatient.html")
    

def get_attr_value(request,attr):
    bankstock = Bankstock.objects.get(bank = get_user(request).bloodbank)
    attrvalue = getattr(bankstock,attr)
    return  JsonResponse({"attrvalue":attrvalue})

def patients(request, argument=None):
    if argument is None :
        return render(request,"patients.html",{
            'patients': get_user(request).hospital.patients.all()
        })
    else:
        obj = get_user(request).hospital.patients.all().get(name=argument)
        obj_data = {
                "Name" : obj.name,
                "Purpose" : obj.purpose,
                "Doctor"  : obj.doctor,
                "Phoneno" : obj.phoneno,
                "Email" : obj.email,
                "Age" : obj.age,
                "Bloodgroup" : (obj.bg).upper(),
                "District" : obj.district,
                "City" : obj.city,
                "ID" : obj.pid
        }

        return JsonResponse(obj_data)
    

def completerequest(request,id):

        user = get_user(request)
        hospital = user.hospital
        hcity = hospital.city
        patient = hospital.patients.all().get(pid = id)
        pcity = patient.city
        banks = User.objects.filter(role='bloodbank')
        for bank in banks:
            print(bank.bloodbank.city)
        print(hcity)
        print(pcity)

        return HttpResponse("SEoe")
