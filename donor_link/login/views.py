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
from geopy import distance
from PIL import Image,ImageFont,ImageDraw

from .models import User,Donor,Hospital,Bloodbank,Patient,Bankstock,Notification,History,Donationlist

def index(request):
    return render(request, "index.html")

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
        District = request.POST['district']
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

            donor  = Donor.objects.create(uuser = user,phoneno = Phoneno ,age = Age,bg = Bg,city = City,district = District,document = Document)
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
        District = request.POST['district']
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

            hospital  = Hospital.objects.create(uuser = user,district = District,phoneno = Phoneno ,city = City,document = Document)
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
        District = request.POST['district']
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

            bloodbank  = Bloodbank.objects.create(uuser = user,phoneno = Phoneno ,district=District , city = City,document = Document)
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
        if int(value) < 3 :
            checkandnotify(user.bloodbank)

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
                "ID" : obj.pid,
                "Name" : obj.name,
                "Purpose" : obj.purpose,
                "Doctor"  : obj.doctor,
                "Phoneno" : obj.phoneno,
                "Email" : obj.email,
                "Age" : obj.age,
                "Bloodgroup" : (obj.bg).replace('p','+').replace('n','-').upper(),
                "District" : obj.district,
                "City" : obj.city
        }

        return JsonResponse(obj_data)
    
def distances(c1,c2):
    location = {
        "Thalassery":(11.83565105, 75.64490544488862),
        "kannur":(11.8763836, 75.3737973),
        "Payyanur":(12.1059663, 75.2073158),
        "Kochi":(9.9674277, 76.2454436),
        "Kalamassery":(10.0547254, 76.3181545),
        "Aluva":(10.17039815, 76.38839448844891),
        "Neyyattinkara":(8.4100639, 77.0816275),
        "Attingal":(8.6985965, 76.8134401),
        "Nedumangad":(8.6052249, 77.0029782)
    }

    loc1 = location[c1]
    loc2 = location[c2]

    return distance.distance(loc1,loc2)

def completerequest(request,id):
        user = get_user(request)
        hospital = user.hospital
        patient = hospital.patients.all().get(pid = id)
        banks = User.objects.filter(role='bloodbank')
        Availbank = []
        for bank in banks:
            if (getattr(bank.bloodbank.bankstock,patient.bg) > 0 ):
                Availbank.append(bank.bloodbank)
        if Availbank == []:
            return render(request,"patients.html",{
                'patients': get_user(request).hospital.patients.all(),
                "error": "No Bloodbank has the required blood group in stock"
            })
        Availbank = sorted(Availbank,key = lambda obj : distances(obj.city,patient.city))
        nearest = Availbank[0]
        setattr(nearest.bankstock,patient.bg,getattr(nearest.bankstock,patient.bg)-1)
        nearest.bankstock.save()
        checkandnotify(nearest)
        hist = History.objects.create(npatient = patient , nbank = nearest)
        hist.save()

        return render(request,"patients.html",{
            'patients': get_user(request).hospital.patients.all(),
            "history": hist
        })


def history(request):
    user = get_user(request)
    if user.role == 'hospital':
        historys  = History.objects.filter( npatient__hosp = user.hospital).order_by('-time')
        return render(request , "hhistory.html", {
            "historys":historys
        })
    else:
        historys  = History.objects.filter( nbank = user.bloodbank ).order_by('-time')
        rhistorys = Donationlist.objects.filter(dbank = user.bloodbank)
        return render(request , "donationhistory.html", {
            "rhistorys":historys,
            "dhistorys":rhistorys

        })




def donorlist(request):
    bank = get_user(request).bloodbank
    dlist = Donor.objects.filter( district = bank.district,available = True )
    return render(request, "donorlist.html", {
        'dlist' : dlist
    })

def consentform(request):
    return render(request, "consentform.html")

def consent(request):
    user = get_user(request)
    Reason = request.GET.get('rsn')
    if user.donor.available == True:
        notif = Notification.objects.create(ndonor = user.donor,  reason = Reason , nbank = None, message = 'Consent form withdrawl completed')
        notif.save()
    else:
        notif = Notification.objects.create(ndonor = user.donor , reason = Reason, nbank = None, message = 'Consent form submission completed')
        notif.save()
    user.donor.available = not user.donor.available
    user.donor.save()

    return redirect('home')

def notifications(request):
    user = get_user(request)
    notification = Notification.objects.filter(ndonor = user.donor).order_by('-time')

    return render(request,"notifications.html",{
        "notifications":notification
    })

def checkandnotify(bank):
    bgs = ['ap','an','bp','bn','abp','abn','op','on']
    for bd in bgs:
        if int(getattr(bank.bankstock,bd)) < 3:
            bcity  = bank.city
            donors = Donor.objects.filter(available=True,bg = bd)
            nearestdonors = sorted(donors,key = lambda  obj : distances(obj.city,bcity))[0:3]
            print(nearestdonors)
            for dnr in nearestdonors:
                Message = f"{ bank.uuser.username } in { bank.city},{bank.district} requesting you donate blood due to shortage in { dnr.getbg() } bloodgroup in BloodBank" 
                notif = Notification.objects.create(ndonor = dnr,nbank = bank,reason='', message = Message,certificate = None)
                notif.save()

def getdonor(request,did = None):
    if did is None:
        return render(request,"getdonor.html")
    else:
        obj_data = None
        if Donor.objects.filter(id = did).exists():

            obj = Donor.objects.get(id = did)

            obj_data = {
                "Donor_id":obj.id,
                "Name":obj.uuser.username,
                "Phonenumber" : obj.phoneno,
                "Age" :obj.age,
                "Blood_group" : (obj.bg).replace('p','+').replace('n','-').upper(),
                "District" : obj.district,
                "City" : obj.city
            }

            return JsonResponse(obj_data)

        return JsonResponse(obj_data,safe=False)
                

def donationregister(request,did):    
    bank = get_user(request).bloodbank
    donor = Donor.objects.get(id= did)
    if donor.available == False:
        return render(request,'getdonor.html',{
            "error": "The donor either doesn't submitted the consent form or not eligible for donation"
        })
    else:
        donationlist = Donationlist.objects.create(ddonor = donor,dbank = bank)
        donationlist.save()
        bstck = getattr(bank.bankstock,donor.bg)
        setattr(bank.bankstock,donor.bg,bstck+1)
        cpath = createcertificate(donor.uuser.username,donationlist.getdate())
        notif = Notification.objects.create(ndonor = donor , reason = '' ,nbank = None, message = f'BloodDonation Succesfull on {bank.uuser.username}',certificate = cpath)
        notif.save()
        donor.available = False
        donor.save()
        return render(request,'getdonor.html',{
            "error": "Congratulations Your Blood Donation Registraion is Completed Succesfully"
        })
            
def createcertificate(name,date):

    certificate = Image.open("login/static/images/certificate.jpg")
    
    certificatewithname = certificate.copy()
    
    font_size = 75
    font_color = (0, 0, 0)  


    font = ImageFont.truetype("login/BRUSHSCI.ttf", size=font_size)

    width, height = certificate.size

    name_width, name_height = font.getsize(name)
    
    name_x = (width - name_width) // 2
    name_y = (height - name_height) // 2
    
    draw = ImageDraw.Draw(certificatewithname)
    
    draw.text((name_x, name_y), name, font=font, fill=font_color)

    font1 = ImageFont.truetype("arial.ttf", size=25)

    draw.text((555,570), date, font=font1, fill=font_color)

    certificatewithname.save(f"media/certificates/{name}{date}.png", 'PNG')

    return f"media/certificates/{name}{date}.png"
