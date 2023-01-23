from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.core.mail import send_mail
from virya.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
import uuid
from django.contrib import messages
from django.contrib.auth import authenticate
import os

# Create your views here.



def regis(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        #checking
        if User.objects.filter(username=username).first():
            messages.success(request,'username already taken')
            return redirect(regis)
        if User.objects.filter(email=email).first():
            messages.success(request,'email already exist')
            return redirect(regis)
        user_obj=User(username=username,email=email)
        user_obj.set_password(password)
        user_obj.save()
        #import uuid
        auth_token=str(uuid.uuid4())
        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        send_mail_regis(email,auth_token)
        return render(request, 'success.html')
    return render(request,'ureg.html')

def send_mail_regis(email,token):
    subject="your account has been verified"
    message=f'paste the link to verigy your account   http://127.0.0.1:8000/viryaapp/verify/{token}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)

def verify(request,auth_token):
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,'your account is already verified')
            return redirect(login)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'your account has been verified')
        return redirect(login)
    else:
        return redirect(error)

def login(request):
    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        a=User.objects.all()
        for i in a:
            email=i.email
        user_obj= User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'user not found')
            return HttpResponse("user not ound") #login
        profile_obj = profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request,'profile not verified check your mail')
            return HttpResponse("not verified password")
        user = authenticate(username=username,password=password,email=email)
        if user is None:
            messages.success(request,'wrong pasword or username')
            return HttpResponse("worng password")
        return render(request,'userindex.html',{'name':username,'email':email})
    return render(request,'ulog.html')



def off(request):
    user=User.objects.all
    return render(request, 'show.html',{'user':user})

def dregister(request):
    if request.method=="POST":
        a=dform(request.POST)#form
        if a.is_valid():
            nm=a.cleaned_data['username']
            em=a.cleaned_data['email']
            ps=a.cleaned_data['password']
            cp=a.cleaned_data['confirm']
            if ps==cp:
                b=dmodel(username=nm,email=em,password=ps)
                b.save()
                return redirect(dlog)
            else:
                return HttpResponse("password doesn't match")
        else:
            return HttpResponse("registration failed")

    return render(request,'dreg.html')

def dlog(request):
    if request.method=="POST":
        a=dlogform(request.POST)
        if a.is_valid():
            n=a.cleaned_data['username']
            p=a.cleaned_data['password']
            b=dmodel.objects.all()
            for i in b:
                if n==i.username and p==i.password:
                    e=i.email
                    return render(request,'dindex.html',{'name':n,'email':e})
            else:
                return HttpResponse("login failed")
    else:
        return render(request,'dlogin.html')


def orthofileup(request):
    if request.method=="POST":
        a=orthoform(request.POST,request.FILES)
        if a.is_valid():
            im = a.cleaned_data['image']
            nm=a.cleaned_data['name']
            co=a.cleaned_data['country']
            st=a.cleaned_data['state']
            ci=a.cleaned_data['city']
            qu=a.cleaned_data['qualification']
            spe=a.cleaned_data['specialisation']
            b=orthomodel(image=im,name=nm,country=co,state=st,city=ci,qualification=qu,specialisation=spe)
            b.save()
            return HttpResponse("success")
        else:
            return HttpResponse("failed....")
    else:
        return render(request,'ortho.html')
def ofupd(request):
    x=orthomodel.objects.all()
    li=[]
    name=[]
    country=[]
    state=[]
    city=[]
    qua=[]
    spe=[]
    id=[]
    for i in x:
        id1=i.id
        id.append(id1)
        path=i.image
        li.append(str(path).split("/")[-1])
        nm=i.name
        name.append(nm)
        co=i.country
        country.append(co)
        st = i.state
        state.append(st)
        ci = i.city
        city.append(ci)
        qo = i.qualification
        qua.append(qo)
        sp = i.specialisation
        spe.append(sp)
    mylist=zip(li,name,country,state,city,qua,spe,id)
    return render(request,'oview.html',{'mylist':mylist})

def uroom(request,id):
    prod=orthomodel.objects.get(id=id)
    li = str(prod.image).split('/')[-1]
    if request.method=="POST":
        if len(request.FILES)!=0:
            if len(prod.image)>0:
                os.remove(prod.image.path)
            prod.image=request.FILES['image']
        prod.name=request.POST.get('name')
        prod.des=request.POST.get('country')
        prod.price=request.POST.get('stste')
        prod.price = request.POST.get('city')
        prod.price = request.POST.get('qualification')
        prod.price = request.POST.get('specialisation')

    context = {'prod':prod,'li':li}
    return render(request,'home.html',context)


def home(request):
    return render(request,'home.html')

def room(request,room):
    username=request.GET.get('rusername')
    room_details=Room.objects.get(name=room)
    return render(request,'room.html',{
        'username':username,
        'room':room,
        'room_details':room_details
    })

def checkview(request):
    room=request.POST['roomname']
    username=request.POST['rusername']
    if Room.objects.filter(name=room).exists():
        return redirect('http://127.0.0.1:8000/viryaapp'+'/'+room+'/?rusername='+username)
    else:
        new_room=Room.objects.create(name=room)
        new_room.save()
        return redirect('http://127.0.0.1:8000/viryaapp'+'/'+room+'/?rusername='+username)



def send(request):
        rusername=request.POST['rusername']
        room_id=request.POST['room_id']
        message=request.POST['message']
        new_message=Messages.objects.create(value=message,user=rusername,room=room_id)
        new_message.save()
        return redirect(getmsg)



def getmsg(request):
    x = Messages.objects.all()
    value = []
    date = []
    room = []
    user = []
    for i in x:
        va=i.value
        value.append(va)
        da=i.date
        date.append(da)
        ro=i.room
        room.append(ro)
        us=i.user
        user.append(us)
    mylist=zip(value,date,room,user)
    return render(request,'room.html',{'mylist': mylist})

# def main(request):
#     return redirect(send)







