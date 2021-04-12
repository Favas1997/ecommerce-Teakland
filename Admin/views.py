from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import JsonResponse,HttpResponse
from .models import product_category
from django.contrib import messages
from django.core.files import File
from .models import products
from users.models import Order,coupon
import base64
from django.core.files.base import ContentFile
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import xlwt
from django.http import HttpResponse
import csv
from django.utils.encoding import smart_str

# Create your views here.
def login(request):
     if request.session.has_key('key'):
          return redirect(home)
     else:
          if request.method=='POST':
               username= request.POST['username']
               password= request.POST['password']
               if (username=='favas' and password=='123456'):
                    request.session['key'] = 'favas'
                    return JsonResponse('true',safe=False)
               else:
                    return JsonResponse('false',safe=False)
          else:
               return render(request,'Admin/admin.html')
def home(request):
     if request.session.has_key('key'):
          order=Order.objects.all()
          order_delivered=Order.objects.filter(status="deliverd")
          user=User.objects.all()
          order_count=order.count()
          users_count=user.count()
          revenue=0
          for i in order_delivered:
               revenue=revenue+i.price
          revenues=revenue
          today_date=date.today()
          current_month=today_date.month
          current_year=today_date.year
          order_in_month=Order.objects.filter(date__month=current_month,status="deliverd")
          revenue_month=0
          for i in order_in_month:
               revenue_month=revenue_month+i.price
          revenues_month=revenue_month
          order_year=Order.objects.filter(date__year=current_year,status="deliverd")
          revenue_year=0
          for j in order_year:
               revenue_year=revenue_year+j.price
          Revenue_year=revenue_year
          order_today=Order.objects.filter(date__day=today_date.day,status="deliverd")
          revenue_today=0
          for j in order_today:
               revenue_today=revenue_today+j.price
          Revenue_today=revenue_today
          return render(request,'Admin/dashboard.html',{'order_count':order_count,'user_count':users_count,'revenue':revenues,'revenue_month':revenues_month,
          'revenue_year':Revenue_year,'revenue_today':Revenue_today,'order':order})
     else:
          return redirect(login)
def user(request):
     if request.session.has_key('key'):
          if 'q' in request.GET:
               q=  request.GET['q']
               user=(User.objects.filter(username__contains=q)) or (User.objects.filter(email__contains=q))
               return render(request,'Admin/user.html',{'user': user})
          else:
               user = User.objects.all()
               return render(request,'Admin/user.html',{'user': user})
     else:
          return redirect(login)
def delete(request,id):
     user= User.objects.get(id=id)
     user.delete()
     return redirect('user')
def block(request,id):
     if request.session.has_key('key'):
       user= User.objects.get(id=id)
       if user.is_active == True:
          user.is_active =False
          user.save()
          return redirect('user')
       else:
          user.is_active=True
          user.save()
          return redirect('user')
     else:
          return redirect(login)
def viewcategory(request):
     if request.session.has_key('key'):
          category=product_category.objects.all()
          return render(request,'Admin/viewcategory.html',{'category':category})
     else:
          return redirect(login)
def addcategory(request):
     if request.session.has_key('key'):
               if request.method=='POST':
                    category=request.POST['category_name']
                    if product_category.objects.filter(category=category).exists():
                         messages.info(request,'category all exist')
                    else:
                         category=product_category.objects.create(category=category)
                         category.save()
                         return redirect(viewcategory)
               else:
                    return render(request,'Admin/addcategory.html')
     else:
          return redirect(login)
def category_delete(request,id):
     category=product_category.objects.get(id=id)
     category.delete()
     return redirect(viewcategory)
def addproducts(request):
          if request.session.has_key('key'):
               if request.method=='POST':
                    product_name=request.POST['product_name']
                    print(product_name)
                    price=request.POST['price']
                    material=request.POST['material']
                    diamension=request.POST['diamension']
                    caring_instructions=request.POST['caring_instructions']
                    description=request.POST['description']
                    finish=request.POST['finish']
                    category=request.POST['category']
                    image1=request.POST['image1']
                    format ,imgstr = image1.split(';base64,')
                    ext = format.split('/')[-1]
                    img1=ContentFile(base64.b64decode(imgstr),name=product_name+'.'+ext)
                    image2=request.POST['image2']
                    format , imgstr2=image2.split(';base64,')
                    img2=ContentFile(base64.b64decode(imgstr2),name=product_name+'.'+ext)
                    image3=request.POST['image3']
                    format , imgstr3=image3.split(';base64,')
                    img3=ContentFile(base64.b64decode(imgstr3),name=product_name+'.'+ext)
                    

                    if products.objects.filter(product_name=product_name).exists():
                         messages.info(request,'already exist')
                    else:
                         category=product_category.objects.get(category=category)
                         product=products.objects.create(product_name=product_name,description=description,image1=img1,image2=img2,image3=img3,price=price,material=material,CaringInstructions=caring_instructions,finish=finish,category=category,Diamensions=diamension)
                         product.save()
                         return JsonResponse('true', safe=False)
               else:
                    category=product_category.objects.all()
                    return render(request,'Admin/addproducts.html',{'category': category})
          else:
                    return redirect(login)
def viewproducts(request):
     if request.session.has_key('key'):
          product=products.objects.all()
          return render(request,'Admin/viewproducts.html',{'products':product})
     else:
          return redirect(login)
def product_delete(request,id):
     product=products.objects.get(id=id)
     product.delete()
     return redirect(viewproducts)
def product_edit(request,id):
          if request.session.has_key('key'):
               product = products.objects.get(id=id)
               category=product_category.objects.all()
               passing={'product':product,'category':category}
               if request.method=='POST':
                    print('1112233333')
                    product_name=request.POST['product_name']
                    print(product_name)
                    price=request.POST['price']
                    material=request.POST['material']
                    diamension=request.POST['diamension']
                    caring_instructions=request.POST['caring_instructions']
                    description=request.POST['description']
                    finish=request.POST['finish']
                    category=request.POST['category']
                    image1=request.POST['image1']
                    format ,imgstr = image1.split(';base64,')
                    ext = format.split('/')[-1]
                    img1=ContentFile(base64.b64decode(imgstr),name=product_name+'.'+ext)
                    image2=request.POST['image2']
                    format , imgstr2=image2.split(';base64,')
                    img2=ContentFile(base64.b64decode(imgstr2),name=product_name+'.'+ext)
                    image3=request.POST['image3']
                    format , imgstr3=image3.split(';base64,')
                    img3=ContentFile(base64.b64decode(imgstr3),name=product_name+'.'+ext)
                    

                    if products.objects.filter(product_name=product_name).exists():
                         messages.info(request,'already exist')
                    else:
                         category=product_category.objects.get(category=category)
                         print(id)
                         product.product_name=product_name
                         product.description=description
                         product.image1=img1
                         product.image2=img2
                         product.image3=img3
                         product.price=price
                         product.material=material
                         product.CaringInstructions=caring_instructions
                         product.finish=finish
                         product.category=category
                         product.Diamensions=diamension
                         product.save()
                         return JsonResponse('true',safe=False)
               else:
                    return render(request,'Admin/editproduct.html',passing)
          else:
               return redirect(login)
def logout(request):
     request.session.flush()
     return redirect(login)
def order_list(request):
     orders=Order.objects.all()
     return render(request,'Admin/order_list.html',{'orders':orders})
@csrf_exempt
def order_status(request):
     if request.method =='POST':
          status1=request.POST['status']
          id=request.POST['id1']
          orders=Order.objects.get(id=id)
          orders.status=status1
          orders.save()
          return JsonResponse('true',safe=False)
     else:
          return redirect(home)
     
def report_search(request):
     if request.method == 'POST':
          date_from=request.POST['datefrom']
          date_to=request.POST['dateto']
          order_search=Order.objects.filter(date__range=[date_from,date_to])
          return render(request,'Admin/report.html',{'order':order_search})
     else:
         order=Order.objects.all() 
         return render(request,'Admin/report.html',{'order':order}) 
def addoffer(request,id):
     discount=request.POST['disc']
     cat=product_category.objects.get(id=id)
     cat.discount=discount
     cat.save()
     return redirect(viewcategory)
def deleteoffer(request,id):
     offer=product_category.objects.get(id=id)
     offer.discount=0
     offer.save()
     return redirect(viewcategory)
def view_coupon(request):
     if request.method=="POST":
          coupon_code=request.POST['coupon_code']
          offer=request.POST['offer_percentage']
          Coupon=coupon.objects.create(coupon_code=coupon_code,coupon_percentage=offer)
          Coupon.save()
     coupon_get=coupon.objects.all()
     return render(request,'Admin/view_coupon.html',{'coupon':coupon_get})
def delete_coupon(request,id):
     coup=coupon.objects.get(id=id)
     coup.delete()
     return  redirect(view_coupon)

   