from django.shortcuts import render,redirect
from .models import ims_customer,ims_category,ims_brand,ims_supplier,ims_product,ims_purchase,ims_order
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.models import User

from django.views.decorators.cache import never_cache


def create_user(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('create_user')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken')
            return redirect('create_user')
        
        user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
        
        messages.success(request, 'User created successfully. Please login.')
        return redirect('login')
    else:
        return render(request, 'your_template_name.html')  # Render your template for the modal form


def loginpage(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard') 
        else:
            messages.error(request,'Email or password are incorrect')
    return render(request, 'login.html')


def logout1(request):
    logout(request)
    return redirect ('login')
    

@login_required(login_url='login')
@never_cache
def dashboard(request):
    products=ims_product.objects.all()
    purchases=ims_purchase.objects.all()
    orders=ims_order.objects.all()
    data=[]
    for product in products:
        productmodel =products.model
        startinventory= product.quantity
        inventoryrecieved = 0
        inventoryshipped = 0
        for purchase in purchases:
            if purchase.product_id.pname == product.pname:
                inventoryrecieved += int(purchase.quantity)
                
        for order in orders:
            if order.product_id.pname == product.pname:
                inventoryshipped += order.total_shiped
                
        inventory__in_hand= startinventory + inventoryrecieved - inventoryshipped 
        data.append(
            {
                'pname':product.pname,
                'modal':product.model,
                'startinventory':startinventory,
                'inventoryrecieved':inventoryrecieved,
                'inventoryshipped':inventoryshipped,
                'inventory__in_hand':inventory__in_hand,
            }
        )
    context={
        'product':products,
        'purchase':purchases,
        'order':orders,
        'data':data,
    }
    return render(request,'dashboardscreen.html',context)


@login_required(login_url='login')
@never_cache
#customermodule start heree
def customermodule(request):
    data=ims_customer.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        data = ims_customer.objects.filter(name__icontains=search_query)  # Filter based on the customer name
    else:
        print("there is no search products")


    if request.method == "POST":
        if 'add_customer' in request.POST:
            a=request.POST.get('name')
            b=request.POST.get('mobile')
            c=request.POST.get('balance')
            d=request.POST.get('address')
            save =ims_customer(name=a,address=d,mobile=b,balance=c)
            save.save()
            return redirect('customermodule')
        
        elif 'del_customer' in request.POST:
            recordid=request.POST.get('id')
            ims_customer.objects.filter(id=recordid).delete()
            return redirect('customermodule')
        
        elif 'submit_edit' in request.POST:
            # Assuming 'id' is passed in POST data to identify the record to edit
            record_id = request.POST.get('id')
            a = request.POST.get('name')
            b = request.POST.get('mobile')
            c = request.POST.get('balance')
            d = request.POST.get('address')
            ims_customer.objects.filter(id=record_id).update(name=a, address=d, mobile=b, balance=c)
            return redirect('customermodule')
        
    
    context={
        'data':data,
    }
    return render(request,'customermodule.html',context)


@login_required(login_url='login')
@never_cache
# categorymodule start here
def categorymodule(request):
    categorydata=ims_category.objects.all()
    if request.method == 'POST':
        a=request.POST.get('categoryname')
        save=ims_category(c_name=a)
        save.save()
        return redirect('categorymodule')
        
    context={
        'categorydata':categorydata,
    }
    return render(request,'categorymodule.html',context)

@login_required(login_url='login')
@never_cache
def deletecategory(request,categoryid):
    delcat=ims_category.objects.get(categoryid=categoryid)
    delcat.delete()
    return redirect('categorymodule')

@login_required(login_url='login')
@never_cache
def editcategory(request,categoryid):
    category=ims_category.objects.get(categoryid=categoryid)
   
    return render(request,'categorymodule.html',{'category':category})

@login_required(login_url='login')
@never_cache
def updatecategory(request,categoryid):
    data=ims_category.objects.all()
    if request.method == 'POST':
        a=request.POST.get('editcategoryname')
        save=ims_category(categoryid=categoryid,c_name=a)
        save.save()
        return redirect('categorymodule')
    context={
        'data':data,
    }
    return render(request,'categorymodule.html',context)

@login_required(login_url='login')
@never_cache
def brandmodule(request):
    data1=ims_category.objects.all()
    data2=ims_brand.objects.all()

    if request.method == 'POST':
        if 'add_brand' in request.POST:
            a=ims_category.objects.get(pk=request.POST.get('categoryid'))
            b=request.POST.get('brandname')
            save=ims_brand(categoryid=a,bname=b)
            save.save()
            return redirect('brandmodule')
        if 'delete_brand' in request.POST:
            brandid=request.POST.get('id')
            ims_brand.objects.filter(id=brandid).delete()
            return redirect('brandmodule')
        # if 'edit_brand' in request.POST:
        #     brandid=request.POST.get('id')
        #     a=request.POST.get('categoryid')
        #     b=request.POST.get('brandname')
        elif 'edit_brand' in request.POST:
            brandid = request.POST.get('id')
            brand = ims_brand.objects.get(id=brandid)
            brand.bname = request.POST.get('brandname')
            brand.categoryid = ims_category.objects.get(pk=request.POST.get('categoryid'))
            brand.save()
            return redirect('brandmodule')

    context={
        'data1':data1,
        'data2':data2,
    }
    return render(request,'brandmodule.html',context)


@login_required(login_url='login')
@never_cache
# supplier module start heree
def suppliermodule(request):
    supplierdata=ims_supplier.objects.all()
    if request.method == 'POST':
        b=request.POST.get('suppliername')
        c=request.POST.get('suppliermobile')
        d=request.POST.get('supplieraddress')
        save=ims_supplier(suppliername=b,mobile=c,address=d)
        save.save()
        return redirect('suppliermodule')
    
    context={
        'supplierdata':supplierdata,
    }
    return render(request,'suppliermodule.html',context)

@login_required(login_url='login')
@never_cache
def deletesupplier(request,supplierid):
    data=ims_supplier.objects.get(supplierid=supplierid)
    data.delete()
    return redirect('suppliermodule')

@login_required(login_url='login')
@never_cache
def editsupplier(request,supplierid):
    data=ims_supplier.objects.get(supplierid=supplierid)
    context={
        'data':data,
    }
    return redirect('suppliermodule')

@login_required(login_url='login')
@never_cache
def updatesupplier(request,supplierid):
    updatesupplierdata=ims_supplier.objects.all()
    if request.method == "POST":
        a=request.POST.get('editsuppliername')
        b=request.POST.get('editmobile')
        c=request.POST.get('editaddress')
        data=ims_supplier(pk=supplierid,suppliername=a,mobile=b,address=c)
        data.save()
        return redirect('suppliermodule')
    return redirect('suppliermodule')

@login_required(login_url='login')
@never_cache
def productmodule(request):
    data1=ims_product.objects.all()
    data2=ims_category.objects.all()
    data3=ims_brand.objects.all()
    data4=ims_supplier.objects.all()
    

    if request.method == 'POST':
            if 'add_product' in request.POST:
                a=ims_category.objects.get(pk=request.POST.get('categoryid'))
                b=ims_brand.objects.get(pk=request.POST.get('id'))
                c=request.POST.get('productname')
                d=request.POST.get('productmodel')
                e=request.POST.get('productdescription')
                f=request.POST.get('productquality')
               
                h=request.POST.get('productbaseprice')
                i=request.POST.get('producttax')
                j=ims_supplier.objects.get(pk=request.POST.get('supplierid'))
                save=ims_product(categoryid=a,brandid=b,pname=c,model=d,description=e,quantity=f,base_price=h,tax=i,supplier=j, date=datetime.now())
                save.save()
                return redirect('productmodule')
            elif "del_product" in request.POST:
                productid=request.POST.get('pid')
                ims_product.objects.filter(pid=productid).delete()
                return redirect('productmodule')
            
            elif 'edit_product' in request.POST:
            # Code to edit a product
                pid = request.POST.get('pid')
                product =ims_product.objects.get(pid=pid)
                product.categoryid = ims_category.objects.get(pk=request.POST.get('category_id'))
                product.brandid = ims_brand.objects.get(pk=request.POST.get('id'))
                product.pname = request.POST.get('productname')
                product.model = request.POST.get('productmodel')
                product.description = request.POST.get('productdescription')
                product.quantity = request.POST.get('productquality')
                product.base_price = request.POST.get('productbaseprice')
                product.tax = request.POST.get('producttax')
                product.supplier = ims_supplier.objects.get(pk=request.POST.get('supplierid'))
                product.save()
                return redirect('productmodule')
    context={
        'data1':data1,
        'data2':data2,
        'data3':data3,
        'data4':data4,
        
    }
    return render(request,'productmodule.html',context)

@login_required(login_url='login')
@never_cache
def purchasemodule(request):
    productdata=ims_product.objects.all()
    supplierdata=ims_supplier.objects.all()
    purchasedata=ims_purchase.objects.all()
    if request.method == 'POST':
        a=ims_product.objects.get(pk=request.POST.get('pid'))
        b=request.POST.get('productquantity')
        c=ims_supplier.objects.get(pk=request.POST.get('supplierid'))
        save=ims_purchase(product_id=a,quantity=b,supplier_id=c)
        save.save()
        return redirect('purchasemodule')
    context={
        "productdata":productdata,
        'supplierdata':supplierdata,
        'purchasedata':purchasedata,
    }
    return render(request,'purchasemodule.html',context)

@login_required(login_url='login')
@never_cache
def deletepurchase(request,purchase_id):
    data=ims_purchase.objects.get(purchase_id=purchase_id)
    data.delete()
    return redirect('editpurchasedata')

@login_required(login_url='login')
@never_cache
def editpurchase(request,purchase_id):
    editpurchasedata=ims_purchase.objects.get(purchase_id=purchase_id)
    context={
        'editpurchasedata':editpurchasedata,
    }
    return redirect('purchasemodule',context
                    
                    )

@login_required(login_url='login')
@never_cache
def updatepurchase(request,purchase_id):
    updatepurchasedata=ims_purchase.objects.all()
    productdata=ims_product.objects.all()
    supplierdata=ims_supplier.objects.all()
    if request.method == 'POST':
        a=ims_product.objects.get(pk=request.POST.get('pid'))
        b=request.POST.get('editproductquantity')
        c=ims_supplier.objects.get(pk=request.POST.get('supplierid'))
        save=ims_purchase(purchase_id=purchase_id,product_id=a,quantity=b,supplier_id=c)
        save.save()
        return redirect('purchasemodule')
    context={
        'updatepurchasedata':updatepurchasedata,
        'productdata':productdata,
        'supplierdata':supplierdata,
        
    }
    return render(request,'purchasemodule.html',context)
    
@login_required(login_url='login')
@never_cache
def ordersmodule(request):
    orderdata=ims_order.objects.all()
    customerdata=ims_customer.objects.all()
    productdata=ims_product.objects.all()
    if request.method == 'POST':
        if 'add_order' in request.POST:
            b=ims_product.objects.get(pk=request.POST.get('pid'))
            c=request.POST.get('productquantity')
            d=ims_customer.objects.get(pk=request.POST.get('id'))
            save=ims_order(product_id=b,total_shiped=c,cutomer_id=d)
            save.save()
            return redirect('ordersmodule')
        elif 'del_order' in request.POST:
            orderid=request.POST.get('order_id')
            ims_order.objects.filter(order_id=orderid).delete()
            return redirect('ordersmodule')
        
        # elif 'edit_order' in request.POST:
        #     orderid=request.POST.get('order_id')
        #     order=ims_order.objects.get(order_id=orderid)
        #     order.product_id=ims_product.objects.get(pk=request.POST.get('pid'))
        #     order.total_shiped=request.POST.get('edittotalquantity')
        #     cutomer_id=request.POST.get('id') 
        #     order.cutomer_id=ims_customer.objects.get(pk=cutomer_id)
        #     order.save()
        #     return redirect('ordersmodule')
            
                # pid = request.POST.get('pid')
                # product =ims_product.objects.get(pid=pid)
                # product.categoryid = ims_category.objects.get(pk=request.POST.get('categoryid'))

    context={
        'orderdata':orderdata,
        'customerdata':customerdata,
        'productdata':productdata,
    }
    return render(request,'ordersmodule.html',context)

@login_required(login_url='login')
@never_cache
def editorder(request,order_id):
    editorderdata=ims_order.objects.get(order_id=order_id)
    return redirect('ordersmodule',{'editorderdata':editorderdata})
@login_required(login_url='login')
@never_cache
def updateorder(request,order_id):
    orderdata=ims_order.objects.all()
    customerdata=ims_customer.objects.all()
    productdata=ims_product.objects.all()
    if request.method == 'POST':
        a=ims_product.objects.get(pk=request.POST.get('pid'))
        b=request.POST.get('edittotalquantity')
        c=ims_customer.objects.get(pk=request.POST.get('id'))
        save=ims_order(order_id=order_id,product_id=a,total_shiped=b,cutomer_id=c)
        save.save()
        return redirect('ordersmodule')
    context={
        'orderdata':orderdata,
        'customerdata':customerdata,
        'productdata':productdata,
    }
    return render(request,'ordersmodule.html',context)



   


