from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import JsonResponse
from Admin.models import products
from Admin.models import product_category
from django.contrib import messages
from .models import Cart,Address,Order,myuser,coupon,Referal
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import random
from twilio.rest import Client
from django.core.files import File
from django.core.cache import cache
from django.http import HttpResponse,HttpRequest

# Create your views here.
def index(request):

    category=product_category.objects.all()
    product=products.objects.all()
    if request.user.is_authenticated and  request.user.is_active ==True:

         return render(request,"User/index.html",{'product':product,'category':category})
    else:
         if request.user.is_active ==False:
          return render(request,"User/index.html",{'product':product,'category':category})  

def login(request):  
     if request.user.is_authenticated:  
         return redirect(index)
     else:
          if request.method=='POST':
               username=request.POST['username']
               password=request.POST['password']
               if User.objects.filter(username=username).exists():
                    user=User.objects.get(username=username)
                    if user.is_active == True:
                         user = auth.authenticate(username=username,password=password)
                         if user is not None:
                              auth.login(request,user)
                              return JsonResponse('true',safe=False)
                         else:
                              return JsonResponse('false',safe=False)
                    else:
                         return JsonResponse('block',safe=False)  
               else:
                    return JsonResponse('false',safe=False)  
          else:
              return render(request,"User/register.html")
def register(request):

    if request.user.is_authenticated:
      return redirect(index)
    else:
          if request.method=='POST':
            username=request.POST['username']
            firstname=request.POST['first_name']
            lastname=request.POST['last_name']
            email= request.POST['email']
            password1= request.POST['password1']
            password2=request.POST['password2']
            mobile_number=request.POST['mobile_number']
            if User.objects.filter(email=email).exists():
                 return JsonResponse('false',safe=False)

            elif User.objects.filter(username=username).exists():
                 return JsonResponse('false1',safe=False) 
            elif myuser.objects.filter(mobile_number=mobile_number).exists():
                 return JsonResponse('false2',safe=False)   

            elif (password1==password2):
            
                  user= User.objects.create_user(username=username,password=password1,email=email,first_name=firstname,last_name=lastname)
                  myuser.objects.create(user=user,mobile_number=mobile_number)
                  welcome_coupon=random.randint(100000,999999)
                  print(welcome_coupon)
                  my=myuser.objects.get(mobile_number=mobile_number)
                  my.coupon_code=welcome_coupon
                  my.save()

                  return JsonResponse('true',safe=False)

def logout(request):
     auth.logout(request)    
     return redirect(index)  

def product_details(request,id):
     category=product_category.objects.all()
     product_details=products.objects.get(id=id)
     return render(request,"User/product_detail.html",{'details':product_details,'category':category})

def product_categ(request,id):
     category1=product_category.objects.all()
     category=product_category.objects.get(id=id)
     products_categorised=products.objects.filter(category=category)
     return render(request,"User/index.html",{'product':products_categorised,'category':category1})
def add_to_cart(request,id):
     if request.user.is_authenticated:

          details=products.objects.get(id=id)
          user=request.user
          if Cart.objects.filter(user=user,products=details).exists():
               Cart.objects.filter(user=user,products=details).update(count=F("count") + 1)
               cart_details= Cart.objects.all()
          else:
            cart= Cart.objects.create(user=user,products=details)
            cart.save()
            cart_details=Cart.objects.all()
     
          #return render(request,"User/cart.html",{'cart':cart_details})
          return redirect(index)

     else:
          return redirect(index)
def cart(request):
     if request.user.is_authenticated:

          carts=Cart.objects.filter(user=request.user)
          if not carts:
               message = "cart empty"
               context ={'cart':carts}
          else:
               sub_total=0
               grand_total=40
               total=0

               for cart in carts:
                    quantity = cart.count
                    if cart.products.category.discount==0:
                         price=cart.products.price
                    else:
                         price=cart.products.discountprice
                    total_price=quantity*price
                    cart.total=total_price
                    sub_total += total_price
                    grand_total = sub_total
                    request.session['total'] = float(grand_total)
               context = {'cart':carts,'sub_total':sub_total,'grand_total':grand_total}

          return render(request,"User/cart.html",context)
     
     else:

          return redirect(index)


@csrf_exempt
def cart_count(request):
     if request.user.is_authenticated:
          count=request.POST['qty']
          id = request.POST['pk']
          Cart.objects.filter(id=id).update(user=request.user,count=count)
          return redirect(cart)
     else:
         return redirect(index) 
@csrf_exempt
def cart_delete(request,id):
     if request.user.is_authenticated:
               cart=Cart.objects.get(id=id)
               cart.delete()
               return redirect('cart')
     else:
         return redirect(index) 
def checkout(request):
     if request.user.is_authenticated:
          user=request.user
          address=Address.objects.filter(user=user)
          # carts=Cart.objects.filter(user=user)
          # sub_total=0
          # grand_total=40
          # total=0

          # for cart in carts:
          #      quantity = cart.count
          #      if cart.products.category.discount !=0:
          #           price=cart.products.discountprice
          #           print(price)
          #           print(cart.products.category.discount)
          #           prin
                    
          #      else:
          #           price=cart.products.price
          #      total_price=quantity*price
          #      print(total_price)
          #      carts.total=total_price
          #      sub_total += total_price
          #      grand_total = grand_total + sub_total
          #      print('111111111111111111111111')
          #      print(quantity)

          #      print(grand_total)
          if request.method=='POST':
               coupon_typed=request.POST['coupon']
               print(coupon_typed)
               grand_total=request.session['total']

               if coupon.objects.filter(coupon_code=coupon_typed):
                    coup=coupon.objects.get(coupon_code=coupon_typed)
                    request.session['refercode']=coupon_typed 
                    grand_total1=(grand_total-(grand_total/100)*coup.coupon_percentage)
                    coup.active = False
                    coup.save()
               elif Referal.objects.filter(referal_code=coupon_typed):
                    # ref= Referal.objects.get(referal_code=coupon_typed)
                    # ref.delete()
                    request.session['refercode']=coupon_typed
                    grand_total1=(grand_total-((grand_total/100)*10))
               else:
                    grand_total1=grand_total
               
               return render(request,'User/checkout.html',{'address':address,'grand_total':grand_total1})
          else:
                    total=request.session['total']
                    return render(request,'User/checkout.html',{'address':address,'grand_total':total}) 
     else:
          return redirect(index)

def add_address(request):
     if request.user.is_authenticated:
          if request.method=='POST':
               name=request.POST['names']
               address=request.POST['address']
               mobile=request.POST['mobile_number']
               district=request.POST['district']
               city=request.POST['city']
               state=request.POST['state']
               pincode=request.POST['pincode']
               user=request.user
               address=Address.objects.create(user=user,name=name,address=address,mobile=mobile,district=district,state=state,pincode=pincode,city=city)
               return redirect(checkout)
     else:     
     
         return redirect(index)
@csrf_exempt     
def select_address(request,id):
     if request.user.is_authenticated:
          request.session['add']=id
          return JsonResponse('true',safe=False)
     else:
          return redirect(index)
def delete_address(request,id):
     if request.user.is_authenticated:
          address=Address.objects.filter(user=request.user,id=id)
          address.delete()
          return redirect(checkout)
          
     else:
          return redirect(index)
def payment_method(request):
     if request.user.is_authenticated:
          if request.method=='GET':
               value=request.GET['value']
               if value =='cod':
                    return JsonResponse('COD',safe=False)
               elif value =='razorpay':
                    return JsonResponse('RAZORPAY',safe=False)
               elif value=='paypal':
                    return JsonResponse('PAYPAL',safe=False )
     else:
          return redirect(index)
def cod(request):
     if request.user.is_authenticated:
          user=request.user
          address_id=request.session['add']
          address=Address.objects.get(id=address_id)
          cart=Cart.objects.filter(user=user)
          for i in cart:
               if i.products.category.discount==0:
                    price=i.count*i.products.price
               else:
                    price=i.count*i.products.discountprice
               Order.objects.create(user=i.user,products=i.products,address=address,status='Ordered',payment_method='COD',count=i.count,price=price)
               i.delete()
          if request.session.has_key('refercode'):
               coup=request.session['refercode']
               if coupon.objects.filter(coupon_code=coup):
                    coup=coupon.objects.get(coupon_code=coup)
                    
                    del request.session['refercode']
               elif Referal.objects.filter(referal_code=coup):
                    refer=Referal.objects.get(referal_code=coup)
                    refer.delete()
                    del request.session['refercode']
          return render(request,'User/confirmationpage.html')
     else:
          return redirect(index)            
def paypal(request):
     if request.user.is_authenticated:
          user=request.user
          cart=Cart.objects.filter(user=user)
          grand_total=0 
          for i in cart:
               if i.products.category.discount==0:
                    price=i.count*i.products.price
               else:
                    price=i.count*i.products.discountprice
               grand_total=grand_total+price
          grand_total=grand_total
          if request.session.has_key('refercode'):
               coup=request.session['refercode']
               if coupon.objects.filter(coupon_code=coup):
                    coup=coupon.objects.get(coupon_code=coup)
                    grand_total=(grand_total-((grand_total/100)*coup.coupon_percentage))
                    grand_total=int(grand_total/72)
                    # del request.session['refercode']
               elif Referal.objects.filter(referal_code=coup):
                    grand_total=(grand_total-((grand_total/100)*10))
                    grand_total=int(grand_total/72)
                    # del request.session['refercode']
          else:
               grand_total=int(grand_total/72)
          context={'grand_total':grand_total}
          return render(request,'User/paypal.html',context)

def paypal_success(request):
     if request.user.is_authenticated:
          user=request.user
          address_id=request.session['add']
          address=Address.objects.get(id=address_id)
          cart=Cart.objects.filter(user=user)
          if request.method=='POST':
               for i in cart:
                    if i.products.category.discount==0:
                         price=i.count*i.products.price
                    else:
                         price=i.count*i.products.discountprice

                    Order.objects.create(user=i.user,products=i.products,address=address,status='Ordered',payment_method='RAZORPAY',count=i.count,price=price)
                    i.delete()

          else:
               for i in cart:
                    if i.products.category.discount==0:
                         price=i.count*i.products.price
                    else:
                         price=i.count*i.products.discountprice
                    Order.objects.create(user=i.user,products=i.products,address=address,status='Ordered',payment_method='PAYPAL',count=i.count,price=price)
                    i.delete()
          if request.session.has_key('refercode'):
               coup=request.session['refercode']
               if coupon.objects.filter(coupon_code=coup):
                    coup=coupon.objects.get(coupon_code=coup)
                    del request.session['refercode']
               elif Referal.objects.filter(referal_code=coup):
                    refer=Referal.objects.get(referal_code=coup)
                    refer.delete()
                    del request.session['refercode']
          return render(request,'User/confirmationpage.html')
     else:
          return redirect(index) 
def razorpay(request):
     if request.user.is_authenticated:
          user=request.user
          cart=Cart.objects.filter(user=user)
          grand_total=0 
          for i in cart:
               if i.products.category.discount==0:
                    price=i.count*i.products.price
               else:
                    price=i.count*i.products.discountprice
               grand_total=grand_total+price
          grand_total=grand_total
          if request.session.has_key('refercode'):
               coup=request.session['refercode']
               if coupon.objects.filter(coupon_code=coup):
                    coup=coupon.objects.get(coupon_code=coup)
                    grand_total=(grand_total-((grand_total/100)*coup.coupon_percentage))
               elif Referal.objects.filter(referal_code=coup):
                    grand_total=(grand_total-((grand_total/100)*10))
          else:
               grand_total=grand_total
          context={'grand_total':grand_total}
          return render(request,'User/razorpay.html',context)
def my_account(request):
     if request.user.is_authenticated:
          host=request.get_host()
          address1=Address.objects.filter(user=request.user)
          order=Order.objects.filter(user=request.user)
          my = myuser.objects.get(user=request.user)
          if Referal.objects.filter(user=request.user).exists():
                refer=Referal.objects.filter(user=request.user)
          else:
               refer= str(0)
          print(refer)
          coupon_get=coupon.objects.all()
          print(my.image1)
          
          return render(request,'User/profile.html',{'address':address1,'orders':order,'profile':my,'coupon_get':coupon_get,'host':host,'refer':refer}) 
     else:
          return redirect(index) 
def edit_profile(request):
     if request.user.is_authenticated:

          if request.method =='POST':
               print('favas')
               current_entered=request.POST['passwordss']    
               current_password=request.user.password
               new_password1=request.POST['password1']
               check = check_password(current_entered,current_password)
               if check == True:
                    user1=User.objects.get(id=request.user.id)
                    user1.set_password(new_password1)
                    user1.save()
                    return JsonResponse('true',safe=False)
          else:

               return render(request,'User/editform.html')
     else:
          return redirect(index) 
def edit_details(request):
     if request.user.is_authenticated:

          if request.method =='POST':
               print('favas')
               user=request.user
               id=request.user.id
               username=request.POST['username']    
               email=request.POST['email']
               if User.objects.filter(username=user.username).exclude(id=id).exists():
                    return JsonResponse('false',safe=False)
               elif User.objects.filter(email=user.email).exclude(id=id).exists():
                    return JsonResponse('false1',safe=False)
               else:
                    user= User.objects.filter(id=id).update(username=username,email=email)
                    return JsonResponse('true',safe=False)
     else:
          return redirect(index) 
def otp_requset(request):
          if request.method=='POST':
               mobile=request.POST['mobile']
               if myuser.objects.filter(mobile_number=mobile).exists():
                    request.session['mobile']=mobile
                    random_num=random.randint(1000,9999)
                    global Otp
                    Otp=random_num
                   
                    account_sid='AC06f290594b57ddf6e4c4ddc2b6443242'
                    auth_token='24ea5f82f08045f5bbbb86c78476bffa'
                    client=Client(account_sid,auth_token)

                    message=client.messages.create(
                         body=f"your otp for login is {Otp}",
                         from_='+15806861457',
                         to=f'+919947913385'
                    )
                    
                    return JsonResponse('true',safe=False)
               else:
                    return JsonResponse('false',safe=False)
          else:
               return render(request,'User/otp.html')
def otp_validate(request):
     if request.method =='POST':
          mobile=request.session['mobile']
          users=myuser.objects.get(mobile_number=mobile)
          user1 = users.user
          otp_entered = request.POST['otp1']
          
          global Otp
          if Otp == int(otp_entered) :
               auth.login(request,user1)
               return JsonResponse('true',safe=False)

     else:
         return render(request,'User/otpvalidate.html') 
def addimage(request):
     if request.user.is_authenticated:
        imageget=request.FILES.get('image_upload')
        y = myuser.objects.get(user=request.user)
        y.image1=imageget
        y.save() 
        return JsonResponse('true',safe=False)

     else:
          return redirect(index)   
def search(request):
     if request.user.is_authenticated:
          if request.method=='POST':
               search_product=request.POST['products']
               print(search_product)
               cache.set('search_Product',search_product)
               product=products.objects.filter(product_name__icontains=search_product)
               cache.set('products',product)
               return redirect(search)

          else:
               category=product_category.objects.all()
               product=cache.get('products')
               search_product=cache.get('search_Product')
               cache.delete('products')
               cache.delete('search_Product')

               context={
                    'category':category,
                    'product':product
               }
               return render(request,"User/index.html",context)
     else:
          return redirect(index) 
def cancel_order(request,id):
     if request.user.is_authenticated:
          orders=Order.objects.filter(id=id).update(status="Cancelled")
          return redirect(my_account)
     else:
          return redirect(index)
def referal_code(request,id):
     users=User.objects.get(id=id)
     # if request.user.is_authenticated:
     #      return redirect(index)
     if request.method=='POST':
          users=User.objects.get(id=id)
          username=request.POST['username']
          firstname=request.POST['first_name']
          lastname=request.POST['last_name']
          email= request.POST['email']
          password1= request.POST['password1']
          password2=request.POST['password2']
          mobile_number=request.POST['mobile_number']
          if User.objects.filter(email=email).exists():
               return JsonResponse('false',safe=False)

          elif User.objects.filter(username=username).exists():
               return JsonResponse('false1',safe=False) 
          elif myuser.objects.filter(mobile_number=mobile_number).exists():
               return JsonResponse('false2',safe=False)   

          elif (password1==password2):
               user= User.objects.create_user(username=username,password=password1,email=email,first_name=firstname,last_name=lastname)
               myuser.objects.create(user=user,mobile_number=mobile_number)
               coupon_refer=random.randint(100000,999999)
               print(coupon_refer)
               print(referal_code)
               Referal.objects.create(user=users,referal_code='REFERAL '+str(coupon_refer),coupon_percentage='10')
               refer_get=random.randint(100000,999999)
               Referal.objects.create(user=user,referal_code='REFERAL '+str(refer_get),coupon_percentage='10')
               return JsonResponse('true',safe=False)
     else:

          return render(request,'User/referal.html',{'user':users})
