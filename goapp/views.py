from audioop import reverse
from email import message
import email
from fileinput import filename
from random import random
from stat import FILE_ATTRIBUTE_SYSTEM
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import  CreateView
from goapp.models import *
from . import models
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import json
import hashlib
from django.http import HttpResponse,JsonResponse
import random
from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

 #authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def index(request):
    return render(request, 'index.html', {})

def home(request):
    return render(request, 'index.html', {})   

def login(request):
    return render(request, 'login.html', {})

def Register(request):
    return render(request, 'Register.html', {})

def mod(request):
    if request.session.is_empty():
        return redirect(login)
    return render(request, 'moderator/index.html', {})

def usere(request):
    if request.session.is_empty():
        return render(request,'login.html')
    us=request.session['id']
    er=user.objects.get(login_id=us)
    return render(request, 'user/index.html', {"rt":er})

def addeval(request):
    if request.session.is_empty():
        return render(request,'login.html')
    return render(request, 'moderator/addeval.html')

def drope(request):
    if request.session.is_empty():
        return render(request,'login.html')
    return render(request, 'moderator/drop.html', {})

def add_prod(request):
    if request.session.is_empty():
        return render(request,'login.html')
    return render(request, 'moderator/add_prod.html', {})

def add_slot(request):
    if request.session.is_empty():
        return render(request,'login.html')
    return render(request, 'user/add_slot.html')

def up_pass(request):
    if request.session.is_empty():
        return render(request,'login.html')
    return render(request, 'user/up_pass.html', {})

def eval(request):
    if request.session.is_empty():
        return render(request,'login.html')
    return render(request, 'Evaluator/index.html', {})

def evalstatus(request):
    if request.session.is_empty():
        return render(request,'login.html')
    return render(request,'Evaluator/evalstatus.html',{})



#User Registeration
def register(request):
    if request.method=="POST":
        name = request.POST['name'] #to get values by POST method frm form
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        image= request.FILES['image']
        ls = FileSystemStorage(location='./static/build_image')
        filename=ls.save(image.name,image)
        file_url=ls.url(filename)
        build_image='build_image'+file_url+''
        password =request.POST['password']
        hashpassword=hashlib.md5(password.encode('utf-8')).hexdigest()
        #import models from app (line 3)
        data = models.login.objects.filter(email=email).count() #to get all rows of data use filter
        if data == 0:
            login = models.login.objects.create(email=email,password=hashpassword,status=1,utype=2) #a=b,a->coloumn name of corresponding table,b->variable name
            login.save()#saving detals
            user_id = models.login.objects.get(email=email) #to get id and store to foreignkey values
            user = models.user.objects.create(Name=name,email=email,mobile=mobile,address=address,image=build_image,status=1,login_id=user_id.login_id)#user_id is variable name and . operator concatinate with login_id
            user.save()
            subject = 'welcome to GoGreen'
            message = f'Hi,{user.Name},\r\n {login.email}, \r\n Password:{login.password} \r\n thank you for registering in GoGreen.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [settings.EMAIL_HOST_USER]
            send_mail( subject, message, email_from, recipient_list )
            messages.success(request,"Registeration Success and Check Mail")
            return redirect('/login')
        else:
            messages.error(request,"Email already registered")
            return redirect(Register)
        return render(request, 'login.html',{"message":message2})

#Checklogin
def checklogin(request):
        if request.method=="POST":
            email = request.POST['email']
            password = request.POST['password']
            hashpassword=hashlib.md5(password.encode('utf-8')).hexdigest()
            data = models.login.objects.filter(email=email,status=1)
            count = data.count()
            if count == 1:
                data2 = data.filter(password=hashpassword)
                if data2.count() == 1:
                
                    for c in data:
                        if c.utype == 2:
                            request.session['id']=c.login_id
                            uid=models.user.objects.get(login_id=c.login_id)
                            if uid.status==0:
                                messages.error(request,"call admin")
                                return redirect(login)
                            request.session['email']=uid.email
                            request.session['Name']=uid.Name
                            return redirect(usere)
                        elif c.utype == 3:
                            request.session['id']=c.login_id
                            return redirect(mod)
                        elif c.utype == 4:
                            request.session['id']=c.login_id
                            eid=models.evaluator.objects.get(login_id=c.login_id)
                            request.session['evname']=eid.evname
                            return redirect(eval)
                else:   
                        subject = 'Login Failed'
                        message = f'Hi, \r\n Password Incorrect Please recheck before type.'
                        email_from = settings.EMAIL_HOST_USER
                        recipient_list = [settings.EMAIL_HOST_USER]
                        send_mail( subject, message, email_from, recipient_list )
                        messages.error(request,"Invalid password")                                  
                        return redirect(login)
            else:
                messages.error(request,"Invalid Credinals or Contact Adminstrator")                                  
                return redirect(login)      


#ADD products..
def prod(request):
    if request.session.is_empty():
        return render(request,'login.html')
    if request.method=="POST":
        pname = request.POST['pname'] #to get values by POST method frm form
        dis = request.POST['dis']
        image= request.FILES['image']
        fs = FileSystemStorage(location='./static/product_image')
        filename=fs.save(image.name,image)
        file_url=fs.url(filename)
        product_image='product_image'+file_url+''
        quantity = request.POST['quantity']
        price = request.POST['price']
        #import models from app (line 3)
        data=models.product.objects.filter(pname=pname)
        count = data.count()
        if count==0:
            prod = models.product.objects.create(pname=pname,dis=dis,image=product_image,quantity=quantity,price=price)
            prod.save()
            messages.success(request,"Product Added")
            return redirect(add_prod)
        else:
            messages.error(request,"Product already exist")    #image=product_image
            return redirect(add_prod)

# #add evaluator
def ev_reg(request):
    if request.session.is_empty():
        return render(request,'login.html')
    if request.method=="POST":
        evname = request.POST['evname'] #to get values by POST method frm form
        email = request.POST['email']
        phone = request.POST['phone']
        password=request.POST['password']
        hashpassword=hashlib.md5(password.encode('utf-8')).hexdigest()
        address=request.POST['address']
        district = request.POST.get('district')
       
        district = int(district)
        print(type(district))
        city = request.POST.get('city')
        print(city)
        #import models from app (line 3)
        data = models.login.objects.filter(email=email).count()#to get all rows of data use filter
        login=()
        if data == 0:
            login = models.login.objects.create(email=email,password=hashpassword,status=1,utype=4) #a=b,a->coloumn name of corresponding table,b->variable name
            login.save()#saving detals
            evaluator = models.evaluator.objects.create(evname=evname,email=email,phone=phone,address=address,district_id=district,city=city,login=login,password=password)#user_id is variable name and . operator concatinate with login_id
            evaluator.save()
            subject = 'welcome to GoGreen'
            message = f'Hi {login.email}, \r\n Password:{login.password} \r\n thank you for registering in GoGreen.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [evaluator.email,]
            send_mail( subject, message, email_from, recipient_list )
            messages.success(request,"Evaluators Added & Mail Send Successfully")
            return redirect(display)
        else:
            messages.error(request,"Already added Email")
            return redirect(display)

def logout(request):
    if request.session.is_empty():
        return HttpResponseRedirect('usere')
    request.session.flush()
    return HttpResponseRedirect('usere')

def table(request):
    if request.session.is_empty():
        return render(request,'login.html')
    eval=evaluator.objects.all()
    dis=district.objects.all()
    cis=city.objects.all()
    use=user.objects.all()
    pr=product.objects.all()
    return render(request,"moderator/table.html",{'ev':eval,'dd':dis,'cc':cis,'ur':use,'pt':pr})

#Add slot
def ad_slot(request):
    if request.session.is_empty():
        return render(request,'login.html')
    if request.method=="POST":
        district=int(request.POST['district'])
        city=request.POST['city']
        evname=request.POST['evname']
        date=request.POST['date']
        time=request.POST['time']
        evobject=models.evaluator.objects.filter(evname=evname)
        for ev in evobject:
            eid = ev.e_id
        #import models from app (line 3)
        
        s_id = request.session['id']
        slot = models.adslot.objects.create(district_id=district,city=city,evname=evname,date=date,time=time,login_id=s_id,e_id=eid)
        slot.save()
        subject = 'welcome to GoGreen'
        message = f'Hi Evaluator:{slot.evname},\r\n Date:{slot.date} \r\n Time:{slot.time} \r\n thank you for Booking slot  in GoGreen.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]
        send_mail( subject, message, email_from, recipient_list )
        messages.success(request,"Slot Booked Success! and Email Send ")
        return redirect(add_slot)
        
#eval info  
# def evalinfi(request):
#     es=models.evaluator.objects.all()
#     return render(request,"user/add_slot.html",{'eer':es})

#slot information
# def status(request):
#     if request.session.is_empty():
#         return render(request,'login.html')
#     id = request.session['id']
#     sl=models.adslot.objects.filter(login_id=id)
#     s=models.district.objects.all()
#     return render(request,"user/status.html",{'em':sl,'se':s})

#Eval dis
# def evalstatus(request):
#     sm=models.adslot.objects.all()
#     return render(request,"Evaluator/evalstatus.html",{'em':sm})



def display(request):
    if request.session.is_empty():
        return render(request,'login.html')
    districtobj=district.objects.all()
    cityobj=city.objects.all()
    return render(request,"moderator/addeval.html",{"di":districtobj,"ci":cityobj})

def display1(request):
    if request.session.is_empty():
        return render(request,'login.html')
    districtobj=district.objects.all()
    cityobj=city.objects.all()
    evalobj=evaluator.objects.all()
    return render(request,"user/add_slot.html",{"di":districtobj,"ci":cityobj,"ev":evalobj})

def userinfoy(request):
    if request.session.is_empty():
        return render(request,'login.html')
    us=user.objects.all()
    return render(request,"Evaluator/users_list1.html",{'usr':us})

#evalstatus

# def evalstatus(request):
#     if request.session.is_empty():
#         return render(request,'login.html')
#     id = request.session['id']
#     print(id)
#     data = models.evaluator.objects.filter(login_id=id)
#     for d in data:
#         dname=d.evname
#         print(dname)
#     es=user.objects.all()
#     si=adslot.objects.filter(evname=dname)
#     s=district.objects.all()
#     return render(request,"Evaluator/evalstatus.html",{"rs":es,"is":si,"sr":s})

def responsepage(request,id):
    if request.session.is_empty():
        return render(request,'login.html')
    context={'slotid':id}
    return render(request,"Evaluator/response.html",context)

def res(request):
    if request.session.is_empty():
        return render(request,'login.html')
    if request.method == "POST":
        res=request.POST['res']
        slotid=request.POST['slotid']
        resp = models.adslot.objects.get(s_id=slotid)
        resp.res = res
        resp.save()
        messages.success(request,"Response Added")
        return redirect(tableeval)
    
#user block


#view products
def viewpr(request):
    if request.session.is_empty():
        return render(request,'login.html')
    rs=product.objects.all()
    return render(request,"moderator/viewproducts.html",{"di":rs})

def advise(request):
    if request.session.is_empty():
        return render(request,'login.html')
    if request.method == "POST":
       advise=request.POST['adv']
       slotid=request.POST['slotid']
       advi=models.adslot.objects.get(s_id=slotid)
       advi.advise=advise
       advi.save()
       messages.success(request,"Advise Added")
       return redirect(tableeval)

def advisepage(request,id):
    if request.session.is_empty():
        return render(request,'login.html')
    context={'slotid':id}
    return render(request,"Evaluator/advise.html",context)

def update(request):
    if request.session.is_empty():
        return render(request,'login.html')
    if request.method=="POST":
        npassword=request.POST['npassword']
        id = request.session['id']
        s1=models.login.objects.get(login_id=id)
        s1.password=npassword
        s1.save()
        subject = 'Data updated'
        message = f'Hi User:{s1.email},\r\n Password:{s1.password}  \r\n Password Updated.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]
        send_mail( subject, message, email_from, recipient_list )
        messages.success(request,"Password Changed and Check Mail")
        return redirect(usere)

# def updatepassword(request,id):
#     context={'lid':id}
#     return render(request,"user/up_pass.html",context)

def updatel(request):
    if request.session.is_empty():
        return render(request,'login.html')
    if request.method=="POST":
        npassword=request.POST['npassword']
        id = request.session['id']
        se=models.login.objects.get(login_id=id)
        se.password=npassword
        se.save()
        subject = 'Data updated'
        message = f'Hi User:{se.email},\r\n Password:{se.password}  \r\n Password Updated.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]
        send_mail( subject, message, email_from, recipient_list )
        messages.success(request,"Password Changed and Check ur mail")
        return redirect(eval)
    
    
def updatee(request):
    if request.session.is_empty():
        return render(request,'login.html')
    return render(request,"Evaluator/up_password.html",{})

def profile(request):
    if request.session.is_empty():
        return render(request,'login.html')
    return render(request,"user/profile.html",{})

def add_culti(request):
    if request.session.is_empty():
        return render(request,'login.html')
    er=request.session['id']
    ur=models.adslot.objects.filter(login_id=er)
    return render(request, 'user/add_cult.html',{"rt":ur})


def viewprofile(request):
    if request.session.is_empty():
        return render(request,'login.html')
    if request.method=="POST":
        mobile=request.POST['mobile']        
        address=request.POST['address']
        id = request.session['id']
        up=models.user.objects.get(login_id=id)
        up.mobile=mobile
        up.address=address
        up.save()
        subject = 'Profile updated'
        message = f'Hi User:{up.email},\r\n Profile Updated.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]
        send_mail( subject, message, email_from, recipient_list )
        messages.success(request,"Profile Updated")
        return redirect(usere)

def shop(request):
    if request.session.is_empty():
        return render(request,'login.html')
    return render(request,"user/indexs.html",{})

# def payment(request):
#     if request.session.is_empty():
#         return render(request,'login.html')
#     return render(request,"user/shop/payment.html",{})

def type_select(request):
    if request.session.is_empty():
        return render(request,'login.html')
    if request.method == 'POST':
        search_str=json.loads(request.body).get('type')
            
        result=city.objects.filter(dis=search_str) 
        data=result.values()
        return JsonResponse(list(data), safe=False)
    
def cartupdate(request):
    if request.session.is_empty():
        return render(request,'login.html')
    if request.method == 'POST':
        cid=json.loads(request.body).get('type')
        no=json.loads(request.body).get('number')
        c=models.cart.objects.get(cartid=cid)
        print(c.p_id)
        
        p=models.product.objects.get(p_id=c.p_id)
        print(type(p.quantity))
        

         
        pr=p.price
        uprice=p.price*float(no)
        data=uprice
        update=models.cart.objects.get(cartid=cid)
        update.quantity=no
        update.uprice=pr
        update.tprice=data
        
  
        update.save()
        return JsonResponse(data, safe=False)
def updatequantity(request,pid,q):
    print(pid)
    print(q)
    product=models.product.objects.get(p_id=pid)
    product.quantity = product.quantity + q
    product.save()
    return redirect(table) 

def type_select1(request):
    if request.session.is_empty():
        return render(request,'login.html')
    if request.method == 'POST':
        search_str=json.loads(request.body).get('type1')  
        result=evaluator.objects.filter(city=search_str) 
        data=result.values()
        return JsonResponse(list(data), safe=False)
    

def dash(request):
    if request.session.is_empty():
        return render(request,'login.html')
    cd=user.objects.count()
    return render(request,"user/dash.html",{"ui":cd})

#shoping site page

def shop(request):
    pf=product.objects.all()
    for p in pf:
        print(p.pname)
    id=request.session['id']
    user=models.user.objects.get(login_id=id)
    cart=models.cart.objects.filter(user_id=user.user_id).count()
    return render(request,"user/indexs.html",{"pd":pf,"cart":cart})


def promote(request,id):
    context={'user_id':id}
    us=user.objects.get(user_id=id)
    us.promote=1
    us.save()
    return redirect(eval)

def tab(request):
    return render(request, 'user/table.html', {})

def block(request,id):
    context={'user_id':id}
    us=user.objects.get(user_id=id)
    us.status=0
    us.save()
    return redirect(table)

def unblock(request,id):
    context={'user_id':id}
    es=user.objects.get(user_id=id)
    es.status=1
    es.save()
    return redirect(table)

def cart(request):
    return render(request,"user/cart.html",{})

def check(request):
    return render(request,"user/checkout.html",{})

def tableuser(request):
    if request.session.is_empty():
        return render(request,'login.html')
    id = request.session['id']
    et=adslot.objects.select_related('district').filter(login_id=id)
    ev=evaluator.objects.all()
    return render(request,"user/tableuser.html",{'ed':et,'ey':ev})

def tableeval(request):
    if request.session.is_empty():
        return render(request,'login.html')
    id = request.session['id']
    print(id)
    data = models.evaluator.objects.get(login_id=id)
   
    es=user.objects.all()
    si=adslot.objects.select_related('district').filter(e_id=data.e_id)
    
    for s in si:
        print(s.district.dname)
    
    return render(request,"Evaluator/tableeval.html",{"rs":es,"is":si})

def addtocart(request,cid):
    id=request.session['id']
    user=models.user.objects.get(login_id=id)
    prod = models.cart.objects.filter(p_id=cid,user_id=user.user_id).count()
    if prod > 0:
         messages.error(request,"Already in cart")
         return redirect(shop)
    prod = models.cart.objects.create(p_id=cid,user_id=user.user_id)
    prod.save()
    return redirect(shop)

def cart(request):
    id=request.session['id']
    print(id)
    user=models.user.objects.get(login_id=id)
    cart=models.cart.objects.select_related('p','user').filter(user_id=user.user_id)
    context={'cart':cart}
    return render(request,"user/cart.html",context)

def remove(request,id):
    context={'cartid':id}
    rd=models.cart.objects.get(cartid=id)
    rd.delete()
    return redirect(cart)

def checkout(request):
    rt=request.session['id']
    ur=models.user.objects.get(login_id=rt)
    car=models.cart.objects.select_related('p','user').filter(user_id=ur.user_id)
    amount=0
    for cat in car:
         amount=amount+cat.tprice
    cd=models.tbl_bank.objects.filter(user_id=ur.user_id)
    for ce  in cd:
        et=ce
    print(et)
    
    currency = 'INR'
    ar = amount
    amount = amount*100  # Rs. 200
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler'
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context["us"]=ur
    context["cr"]=car
    context["ar"]=ar
    
    return render(request,"user/checkin.html",context=context)

def placeorder(request):
    order = ()
    rt=request.session['id']
    ur=models.user.objects.get(login_id=rt)
    cr=models.cart.objects.filter(user_id=ur.user_id)
    amount=0
    for cat in cr:
        amount=amount+cat.tprice
    print(amount)
    for gh in cr:
        pi=models.product.objects.get(p_id=gh.p_id)
        pi.quantity = pi.quantity-gh.quantity
        pi.save()
    generate_random=random.randint(111111111111,999999999999)
    generate_random=str(generate_random)    
    order=models.order.objects.create(amount=amount,user_id=ur.user_id,track=generate_random)
    order.save()
    for ord in cr:
        od=models.orderdetails.objects.create(quantity=ord.quantity,price=ord.tprice,order=order,p_id=ord.p_id)
        od.save()
    dr=models.cart.objects.filter(user_id=ur.user_id)
    for der in dr:
        der.delete()
    gen=random.randint(11111,99999)
    gene=str(gen)
    ty=models.tbl_bank.objects.get(user_id=ur.user_id)
    yu=models.order.objects.filter(user_id=ur.user_id)
    for ye in yu:
        ye.transid=gene
        ye.b_id=ty.b_id
        ye.save()
    subject = 'Thank you For Your Order!|GoGreen'
    message = f'Hi User:{ur.Name},\r\n Orderid:{generate_random}\r\n Products Name: /r/n  Order Confirmed and Your Transication ID:{ye.transid}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_HOST_USER]
    send_mail( subject, message, email_from, recipient_list )
    messages.success(request,"Order Confirmed Please check ur Mail !")
    return render(request,"user/order.html",{"ar":amount,"orderid":generate_random}) 

@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return redirect(placeorder)
                except:
 
                    # if there is an error while capturing payment.
                    return redirect(placeorder)
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return redirect(placeorder)
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()




def ordersi(request):
    rt=request.session['id']
    ur=models.user.objects.get(login_id=rt)
    print(ur)
    ot=models.order.objects.select_related('user').filter(user_id=ur.user_id)
    return render(request,"user/orderh.html",{"ui":ot})

def orderd(request,id):
    ty=models.orderdetails.objects.select_related('p').filter(order_id=id)
    context={'order_id':id,'po':ty}
    return render(request,"user/orderd.html",context)

def carte(request):
    return render(request,"user/cart.html")

def buyagain(request,cid):
    id=request.session['id']
    user=models.user.objects.get(login_id=id)
    # prod = models.cart.objects.filter(p_id=cid,user_id=user.user_id)
    # if prod > 0:
    #      messages.error(request,"Already in cart")
    #      return redirect(shop)
    prod = models.cart.objects.create(p_id=cid,user_id=user.user_id)
    prod.save()
    return redirect(cart)

def returne(request,mid):
    us=models.orderdetails.objects.get(ord_id=mid)
    us.status="returned"
    us.save()
    orderid = us.order_id
    check=models.orderdetails.objects.filter(order_id=orderid)
    flag=0
    for c in check:
        if c.status == 'returned':
         flag=1
    print(flag)     
    if flag == 1:
        oo=models.order.objects.get(order_id=orderid)
        oo.status="returned"
        print(oo.status)
        oo.save()
    return redirect(usere)


#admin orders view\

def orders(request):
    ord=models.order.objects.select_related('user').all()
    return render(request,"moderator/orders.html",{"ore":ord})
   
def ordersd(request,vid):
    ordi=models.orderdetails.objects.select_related('p').filter(order_id=vid)
    context={'order_id':vid,'po':ordi}
    return render(request,"moderator/ordersd.html",context)

def cultiv(request):
    if request.session.is_empty():
        return render(request,'login.html')
    if request.method=="POST":
        vname=request.POST['vname']
        dise=request.POST['dise']
        sdate=request.POST['sdate']
        ldate=request.POST['ldate']
        slot_id=request.POST['slot_id']
        status=request.POST['status']
        gt=models.adslot.objects.get(s_id=slot_id)
        #import models from app (line 3)
        ct_id = request.session['id']
        cult = models.culti.objects.create(vname=vname,dise=dise,sdate=sdate,ldate=ldate,status=status,e_id=gt.e_id,login_id=ct_id,slot_id=slot_id)
        cult.save()
        messages.success(request,"Details Added")
        return redirect(add_culti)
    
def upcult(request):
    rt=request.session['id']
    print(rt)
    ut=models.culti.objects.filter(login_id=rt)
    return render(request,"user/update_clt.html",{"uy":ut})

def cultistatus(request,ctid,status):
    print(ctid)
    print(status)
    stat=models.culti.objects.get(ct_id=ctid)
    stat.status = status
    stat.save()
    return redirect(upcult) 

def evalculti(request):
    id = request.session['id']
    data = models.evaluator.objects.get(login_id=id)
    ry=models.culti.objects.select_related('login').filter(e_id=data.e_id)
    list=[]
    for r in ry:
        user = models.user.objects.get(login_id=r.login.login_id)
        r.username=user.Name
        list.append(r)
    return render(request,"Evaluator/cultstatus.html",{"li":list})  

def dash(request):
    return render(request,"user/dash.html")

def track(request):
    return render(request,"user/track.html")

def tracky(request):
    if request.method=="POST":
        track=request.POST['track']
    print(track)
    ody=models.order.objects.select_related('user').get(track=track)
    return render(request,"user/track.html",{"od":ody})

def adm(request):
    return render(request,"moderator/statusdev.html")

def admstatus(request):
    if request.method=="POST":
        track=request.POST['track']
        status=request.POST['status']
        ody=models.order.objects.select_related('user').get(track=track)
        ody.status=status
        ody.save()
        return render(request,"moderator/statusdev.html",{"of":ody})

    
        
    
    
    
    
    
    
    







# def ordersad(request):
#     ot=models.order.objects.select_related('user').all()
#     return render(request,"user/ordersad.html",{"ui":ot})
    
    
    















# def payment(request):
#     rt=request.session['id']
#     ur=models.user.objects.get(login_id=rt)
#     if request.method == 'POST':
#         card=request.POST['card']
#         name=request.POST['name']      
#         expry=request.POST['expry']   
#         cvv=request.POST['cvv']
#         brd=models.tbl_bank.objects.create(name=name,card=card,expry=expry,cvv=cvv,user_id=ur.user_id)
#         brd.save()
#     return render(request,"user/shop/order.html")

  
    
    
    
    
    
    
    #subject = 'Thank you For Your Order!|GoGreen'
    # message = f'Hi User:{ur.Name},\r\n Orderid:{generate_random}  \r\n Order Confirmed.'
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = [settings.EMAIL_HOST_USER]
    # send_mail( subject, message, email_from, recipient_list )
    # messages.success(request,"Order Confirmed Please check ur Mail !")
    
   
#    generate_random=random.randint(111111111111,999999999999)
#    generate_random=str(generate_random)


































