from django.shortcuts import render,redirect,HttpResponse
import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.db import IntegrityError
from hotelapp.models import Rooms,Roombooking
import razorpay
# Create your views here.
def index(request):
    r=Rooms.objects.all()
    context={}
    context['room']=r
    return render(request,'index.html',context)

def mybooking(request):
    if request.user.is_authenticated:
        b=Roombooking.objects.filter(uid=request.user)
        context={}
        context['booking']=b
        context['today']=datetime.datetime.today()
        if len(b)==0:
            context['errmsg1']="You haven't proceeded with any booking yet!!"
        return render(request,'mybooking.html',context)
    else:
        return redirect('/login')

def contact(request):
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        mail=request.POST['email']
        msg=request.POST['msg']
        context={}
        if fname=="" or mail=="" or msg=="":
            context['errmsg']="Note: '*' marks fileds are mandatory"
        elif fname.isdigit() or lname.isdigit():
            context['errmsg']="Please enter valid first and last name"
        else:
            context['succmsg']='We have received your mail/Query.'
        return render(request,'contact.html',context)
    else:
        return render(request,'contact.html')

def rdetails(request,rid):
    if request.method=='GET':
        r=Rooms.objects.filter(id=rid)
        print(r)
        print(r[0].rname)
        context={}
        context['room']=r
        return render(request,'seedetails.html',context)

def custdetail(request,rid,cin,cout):
    if request.user.is_authenticated:
        r=Rooms.objects.filter(id=rid)
        context={}
        context['room']=r
        context['checkin']=cin
        context['checkout']=cout
        cin=datetime.datetime.strptime(cin, "%Y-%m-%dT%H:%M")
        cout=datetime.datetime.strptime(cout, "%Y-%m-%dT%H:%M")
        diff=cout-cin
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        print(hours,minutes)
        if minutes!=0:
            hours+=1
        context['hour']=hours
        price=hours*r[0].Price
        gst=round(price*0.18/100)
        net=price+gst+500
        adv= round(net * 10 /100)
        rest=net-adv
        print(price,gst,net,adv,rest)
        context['price'],context['net'],context['gst'],context['adv'],context['rest']=price,net,gst,adv,rest
        return render(request,'custdetail.html',context)
    else:
        return redirect('/login')

def ulogin(request):
    if request.method=="POST":
        uname=request.POST['username']
        upass=request.POST['userpass']
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Fields cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/index')
            else:
                context['errmsg']="Enter Valid Username and Password"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')

def ulogout(request):
    logout(request)
    return redirect('/login')

def register(request):
    if request.method=='POST':
        fname=request.POST['firstname']
        lname=request.POST['lastname']
        mail=request.POST['mail']
        upass=request.POST['upass']
        cpass=request.POST['cpass']
        context={}
        if fname=="" or lname=="" or mail=="" or upass=="" or cpass=="":
            context['errmsg']="Please enter values in all fields"
        elif upass!=cpass:
            context['errmsg']="Password and Confirm password does not match"
        elif fname.isdigit() or lname.isdigit():
            context['errmsg']="Please enter valid First and Last name"
        else:
            try:
                u=User.objects.create(username=mail,first_name=fname,last_name=lname,password=upass,email=mail)
                u.set_password(upass)
                u.save()
                context['success']="Registered successfully"
            except IntegrityError:
                context['errmsg']="Email id already exists. Use another Email ID."
            except Exception as e:
                context['errmsg']="Something went wrong. Please try again"
        return render(request,'register.html',context)
    else:
        return render(request,'register.html')

def aboutus(request):
    return render(request,'aboutus.html')

def bedtype(request,bid):
    r=Rooms.objects.filter(bedtypecat=bid)
    context={}
    if len(r)==0:
        context['errmsg']="Oops! Seems room not available with us at the moment"
    else:
        context['room']=r
    return render(request,'index.html',context)

def sort(request):
    minp=request.GET['minprice']
    maxp=request.GET['maxprice']
    print(minp,maxp)
    context={}
    if minp=="" and maxp=="":
        r=Rooms.objects.all()
        context['room']=r
        context['errmsg']="Enter the Minimum or Maximum Ammount"
        return render(request,'index.html',context)
    elif maxp=="":
        r=Rooms.objects.filter(Price__gte=minp)
    elif minp=="":
        r=Rooms.objects.filter(Price__lte=maxp)
    else:
        q1=Q(Price__gte=minp)
        q2=Q(Price__lte=maxp)
        r=Rooms.objects.filter(q1 & q2)
    print(r)
    context['room']=r
    return render(request,'index.html',context)

def checkavailbility(request,cid):
    r=Rooms.objects.filter(id=cid)
    context={}
    context['room']=r
    if request.method=='POST':
        cin=request.POST['checkin']
        cout=request.POST['checkout']
        context['checkin']=cin
        context['checkout']=cout
        c=datetime.datetime.today()
        try:
            cin=datetime.datetime.strptime(cin, "%Y-%m-%dT%H:%M")
            cout=datetime.datetime.strptime(cout, "%Y-%m-%dT%H:%M")
        except Exception:
            cin=""
            cout=""
        if cin=="" or cout=="":
            context['errmsg']="Please enter the details"
        else:
            if cin<c or cout<c:
                context['errmsg']="Enter valid check-in and check-out date"
            elif cin>cout:
                context['errmsg']="Please enter valid check-out date"
            elif cin==cout:
                context['errmsg']="Rooms Cannot be booked for same day"
            else:
                q1=Q(rid=r[0].id)
                q2=Q(status=2)
                #q3=Q(checkin>datetime.date.today())
                b=Roombooking.objects.filter(q1 & q2)
                if len(b)==0:
                    context['succmsg']='Room available. Click on Next to proceed or check more dates for availabilty.'
                    return render(request,'seedetails.html',context)
                for x in b:
                    if cin.date()<=x.checkin.date()<=cout.date():
                        avail=False
                        context['errmsg']='Room already booked. Try another room or another dates.'
                        break
                    elif cin.date()<=x.checkout.date()<=cout.date():
                        avail=False
                        context['errmsg']='Room already booked. Try another room or another dates.'
                        break
                    elif x.checkin.date()<=cin.date()<=x.checkout.date():
                        avail=False
                        context['errmsg']='Room already booked. Try another room or another dates.'
                        break
                    # elif x.checkin.date()<=cout.date()<=x.checkout.date():
                    #     print("out between")
                    #     avail=False
                    #     context['errmsg']='Room already booked. Try another room or another dates.'
                    #     break
                    else:
                        avail=True
                if avail:
                        context['succmsg']='Room available. Click on Next to proceed or check more dates for availabilty.'
        return render(request,'seedetails.html',context)
    else:
        return render(request,'seedetails.html',context)
    

def cancel(request,rid):
    r=Rooms.objects.filter(id=rid)
    context={}
    context['room']=r
    return render(request,'seedetails.html',context)

def confirm(request,rid,cin,cout):
    r=Rooms.objects.filter(id=rid)
    context={}
    context['room']=r
    context['checkin']=cin
    context['checkout']=cout
    cin=datetime.datetime.strptime(cin, "%Y-%m-%dT%H:%M")
    cout=datetime.datetime.strptime(cout, "%Y-%m-%dT%H:%M")
    diff=cout-cin
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    print(hours,minutes)
    if minutes!=0:
        hours+=1
    context['hour']=hours
    context['price']=hours*r[0].Price
    if request.method=='POST':
        cname=request.POST['cname']
        mob=request.POST['mob']
        mail=request.POST['email']
        adults=request.POST['adults']
        child=request.POST['child']
        if child=="":
            child='0'
        if adults=='':
            adults='0'
        count=int(adults)+int(child)
        if cname=="" or mob=="" or mail=="" or adults=="":
            context['errmsg']="Note: '*' marks fileds cannot be empty"
            return render(request,'custdetail.html',context)
        elif int(mob)<6000000000 or int(mob)>9999999999:
            context['errmsg']="Enter valid mobile number"
            return render(request,'custdetail.html',context)
        elif int(adults)<1:
            context['errmsg']="Need atleast 1 adults in the group"
            return render(request,'custdetail.html',context)
        elif count>4:
            context['errmsg']="Maximum capacity of room is 4 members"
            return render(request,'custdetail.html',context)
        elif cname.isdigit():
            context['errmsg']="Enter valid Customer name"
            return render(request,'custdetail.html',context)
        else:
            u=User.objects.filter(id=request.user.id)
            try:
                b=Roombooking.objects.create(uid=u[0],rid=r[0],checkin=cin,checkout=cout,cname=cname,mob=mob,email=mail,adults=adults,child=child,status=4)
                b.save()
                return redirect("/finalbooking")
            except Exception as e:
                return HttpResponse(e)    
    else:
        return render(request,'custdetail.html',context)
    
def finalbooking(request):
    print(request.user)
    q1=Q(uid=request.user)
    q2=Q(status=4)
    b=Roombooking.objects.filter(q1 & q2)
    print(len(b))
    for x in b:
        print(x.rid,x.uid)
    context={}
    if len(b)>1:
        context['errmsg']="Seems you have previous pending booking. Please clear the unwanted drafts."
    else:
        context['details']=b
        # cin=datetime.datetime.strptime(b[0].checkin, "%Y-%m-%dT%H:%M")
        # cout=datetime.datetime.strptime(b[0].checkout, "%Y-%m-%dT%H:%M")
        diff=b[0].checkout-b[0].checkin
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        if minutes!=0:
            hours+=1
        context['hour']=hours
        price=hours*b[0].rid.Price
        gst=round(price*0.18/100)
        net=price+gst+1
        adv= round(net * 10 /100)
        rest=net-adv
        context['price'],context['net'],context['gst'],context['adv'],context['rest']=price,net,gst,adv,rest
    return render(request,"finalbooking.html",context)

def moredate(request,mid):
    r=Rooms.objects.filter(id=mid)
    print(r)
    print(r[0].rname)
    context={}
    context['room']=r
    return render(request,'seedetails.html',context)

def remove(request,bid):
    context={}
    try:
        b=Roombooking.objects.filter(id=bid)
        b.delete()
        context['succmsg']="Booking successfully removed"
    except Exception:
        context['errmsg']="Something went wrong try refreshing the page"
    finally:
        b=Roombooking.objects.filter(uid=request.user)    
        context['booking']=b
        context['today']=datetime.datetime.today()
    return render(request,'mybooking.html',context)

def cancelbooking(request,bid):
    context={}
    try:
        b=Roombooking.objects.filter(id=bid).update(status=3)
        context['succmsg']="Booking Cancelled Successfully"
    except Exception:
        context['errmsg']="Something went wrong try refreshing the page"
    finally:
        b=Roombooking.objects.filter(uid=request.user)    
        context['booking']=b
        context['today']=datetime.datetime.today()
    return render(request,'mybooking.html',context)
    

def booknow(request,bid):
    #code to show the booking
    b=Roombooking.objects.filter(uid=request.user)
    context={}
    context['booking']=b
    context['today']=datetime.datetime.today()
    #Actual booking starts here
    b1=Roombooking.objects.filter(id=bid)
    q1=Q(rid=b1[0].rid)
    q2=Q(status=2)
                #q3=Q(checkin>datetime.date.today())
    b=Roombooking.objects.filter(q1 & q2)
    print(b,len(b))
    for x in b:
        print(x.rid)
    if len(b)==0:
        return redirect('/finalbooking')
    for x in b:
        if b1[0].checkin.date()<=x.checkin.date()<=b1[0].checkout.date():
            print("checkin between")
            avail=False
            context['errmsg']='Oh!.. Room is not available.'
            return render(request,'mybooking.html',context)
        elif b1[0].checkin.date()<=x.checkout.date()<=b1[0].checkout.date():
            print("checkout between")
            avail=False
            context['errmsg']='Oh!.. Room is not available.'
            return render(request,'mybooking.html',context)
        elif x.checkin.date()<=b1[0].checkin.date()<=x.checkout.date():
            print("in between")
            avail=False
            context['errmsg']='Oh!.. Room is not available.'
            return render(request,'mybooking.html',context)
                    # elif x.checkin.date()<=cout.date()<=x.checkout.date():
                    #     print("out between")
                    #     avail=False
                    #     context['errmsg']='Room already booked. Try another room or another dates.'
                    #     break
        else:
            avail=True
        if avail:
            #context['succmsg']='Room available. Click on Next to proceed or check more dates for availabilty.'
            return redirect('/finalbooking')

def location(request):
    context={}
    loca=request.GET['loc']
    if loca=="":
        r=Rooms.objects.all()
        context['room']=r
        context['errmsg']="Enter City or State in which you are searching"
        return render(request,'index.html',context)
    q1=Q(City=loca)
    q2=Q(Location=loca)
    try:
        r=Rooms.objects.filter(q1 | q2)
        print(r)
        if len(r)==0:
            context['errmsg']='OOPS!! Seems we don\'t have avaiable rooms in this region OR Check the spelling'
    except Exception as e:
        context['errmsg']="Something went Wrong"
        r=Rooms.objects.all()
    finally:
        context['room']=r
        return render(request,'index.html',context)
    
def bookconfirm(request,bid):
    context={}
    try:
        b=Roombooking.objects.filter(id=bid)
        diff=b[0].checkout-b[0].checkin
        days, seconds = diff.days, diff.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        if minutes!=0:
            hours+=1
        price=hours*b[0].rid.Price
        gst=round(price*0.18/100)
        net=price+gst+1
        adv= round(net * 10 /100)
        print(adv)
        client = razorpay.Client(auth=("rzp_test_wIRW5UcLnuojt3", "TAWQaJo7pF8PxWMwC5MwnOQg"))
        DATA = {
        "amount": adv*100,
        "currency": "INR",
        "receipt": bid
        }
        payment=client.order.create(data=DATA)
        print(payment)
        #context['DATA']=DATA
        return render(request,"pay.html")
        #return redirect('/mybooking')
    except Exception:
        context['errmsg']="Something went wrong"
        return render(request,'finalbooking.html',context)
    
    '''
    context={}
    try:
        b=Roombooking.objects.filter(id=bid).update(status=2)
        return redirect('/mybooking')
    except Exception:
        context['errmsg']="Something went wrong"
        return render(request,'finalbooking.html',context)'''
    