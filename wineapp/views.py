from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect
from wineapp.models import Msg
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from wineapp.models import Product,Cart,Order
from django.db.models import Q
import random
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
#import razorpay
# Create your views here.
   
def home(request):
    # userid=request.user.id
    # print(userid)
    #print('result:',request.user.is_authenticated)
    #return render(request,'index.html')
    context={}
    p=Product.objects.filter(is_active=True)
    print(p)
    context['Products']=p
    return render(request,'index.html',context)


def product_details(request,pid):
    context={}
    context['Products']=Product.objects.filter(id=pid)
    return render(request,'productdetails.html',context)


def about(request):
    return render(request,'about.html')
def contact(request):
    return render(request,'contact.html')
def register(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        cpass=request.POST['upsc']
        if uname=="" or upass=="" or cpass=="":
            context['errormsg']="field can not be empty"
            return render(request,'register.html',context)
        elif upass!=cpass:
            context['errormsg']="password and confirmpassword did not match"
            return render(request,'register.html',context)
        else:
            try: 
                u=User.objects.create(username=uname,password=upass,email=uname)
                u.set_password(cpass)
                u.save()
                context['success']="user created successfully plz login"
                return render(request,'register.html',context)
            except Exception:
                context['errormsg']="user name already exist"
            return render(request,'register.html',context)

    else:
        return render(request,'register.html')
def user_login(request):
    context={}
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        if uname=="" or upass=="":
            context['errormsg']="data is fetched"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errormsg']='invalid username and password'
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')
            
   

def user_logout(request):
    logout(request)
    return redirect('/home')
    
def range(request):
    min=request.GET['umin']
    max=request.GET['umax']
    q1=Q(price__gte = min)
    q2=Q(price__lte = max)
    q3=Q(is_active=True)
    x=Product.objects.filter(q1 & q2 & q3)
    print('final products are', x)
    context={}
    context['Products']=x
    return render(request,'index.html',context)

    print(min)
    print(max)
                                                       

def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    x=Product.objects.filter(q1 & q2)
    print(x)
    context={}
    context['Products']=x
    return render(request,'index.html',context)




def sort(request,sv):
    if sv == '0':
        col='price'
    else:
        col='-price'
    r=Product.objects.filter(is_active=True).order_by(col)
    print(r)
    context={}
    context['Products']=r
    return render(request,'index.html',context)





def addtocart(request,pid):
    if request.user.is_authenticated:
       userid=request.user.id
       u=User.objects.filter(id=userid)
       print(u[0])
       p=Product.objects.filter(id=pid)
       print(p[0])
       c=Cart.objects.create(uid=u[0],pid=p[0])
       c.save()
    # print(userid)
    # print(pid)
       return redirect('/home')
    else:
        return redirect('/login')
    
    
def cart(request):
    return render(request,'cart.html')


def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')
 


def viewcart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    s=0
    np=len(c)
    for x in c:
        # print(x)
        # print(x.pid.price)
        s=s+x.pid.price * x.qty
    context={}

    context['n']=np
    context['Products']=c
    context['total']=s
    return render(request,'cart.html',context)

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)

            # print(c)
    # print(c[0])
    # print(c[0].qty)
    return redirect('/viewcart')


def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    oid=random.randrange(1000,9999)
    print('orderid',oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    np=len(c)
    for x in c:
        # print(x)
        # print(x.pid.price)
        s=s+x.pid.price * x.qty
    context={}

    context['n']=np
    context['Products']=c
    context['total']=s
    return render(request,'placeorder.html',context)

#def makepayment(request):
   # orders=Order.objects.filter(uid=request.user.id)
    #s=0
    #for x in orders:
    # print(x)
    #print(x.pid.price)
            
       # s=s+x.pid.price *x.qty
       # oid=x.order_id
        #client = razorpay.Client(auth=("rzp_test_gHlznvzclnDxMR", "EUmD4ch8itx3EyiAkORv0970"))
        #data = { "amount": s, "currency": "INR", "receipt": "oid" }
        #payment = client.order.create(data=data)
        #print(payment)
        #context={}
        #context['data']=payment
        #return render(request,"pay.html",context)


def forget_password(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        new_password = request.POST.get('upass')
        confirm_password = request.POST.get('upsc')

        user = User.objects.filter(username=username).first()

        if user:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()

                # Update the session to avoid automatic logout
                update_session_auth_hash(request, user)

                messages.success(request, 'Password reset successfully!')
                return redirect('/login')  # Redirect to login page after successful password reset
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'User not found.')

    return render(request, 'forget.html')