
import datetime
import json
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseRedirect
from .models import *
from django.urls import reverse


def cart_order(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        cartItems = order.get_cart_items

    else:

        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = order['get_cart_items']
    context = {

        "order": order,
        "cartItems": cartItems
    }
    return context


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    if request.method == "POST":
        first_name = request.POST['first_Name']
        last_name = request.POST['last_Name']
        email = request.POST['email']
        username = request.POST['username']
        mobile = request.POST['mobile']
        Password = request.POST['Password']
        confirm_password = request.POST['confirm_password']

        if Password != confirm_password:
            passnotmatch = True
            return render(request, "student_registration.html", {'passnotmatch': passnotmatch})
        if User.objects.filter(username=username):
            return render(request, "register.html")
        else:
            user = User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name,
                                            password=Password)
            register_models = Register_models.objects.create(user=user, mobile=mobile)
            user.save()
            register_models.save()
            login(request, user)
            return redirect("/")
            # return render(request, "register.html")
    return render(request, "register.html")


def login1(request):
    if request.method == "POST":
        usernam = request.POST['email']
        passwor = request.POST['Password']
        user = authenticate(username=usernam, password=passwor)
        print("User",usernam)
        print("password", passwor)
        print(user)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/admin")
            return redirect("/")
        return redirect("/")
    return render(request, "login.html")


@login_required(login_url='/login')
def my_account(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            edit_user = Register_models.objects.get(user=request.user)
            first_name = request.POST['first_name']
            last_Name = request.POST['last_name']
            mobile = request.POST['mobile']
            email = request.POST['email']
            address = request.POST['address']
            edit_user.user.email = email
            edit_user.mobile = mobile
            edit_user.user.first_name = first_name
            edit_user.user.last_name = last_Name
            edit_user.address = address
            edit_user.user.save()
            edit_user.save()
           
            
            context = {
                'mobile': edit_user.mobile,
                'address': edit_user.address,
               
            }
            return render(request, "my_account.html", context)

        else:
            try:
                edit_user = Register_models.objects.get(user=request.user)
    
            except Register_models.DoesNotExist:
                edit_user = None
            ord = Order.objects.filter(user=request.user,complete=True)
            items = []
            shippingAddress=[]
            for order in ord:
                orderItem = OrderItem.objects.filter(order=order)
                sh_address= ShippingAddress.objects.filter(order=order)
                for item in orderItem:
                    items.append(item)

                for address in sh_address:
                    shippingAddress.append(address)
                        
            
            # items = OrderItem.objects.filter(order=ord)
            context = {
                'edit_user': edit_user,
                'items':items,
                'shippingAddress':shippingAddress
            }
            return render(request, "my_account.html", context)
    else:
        return render(request, "index.html")


@login_required(login_url='/login')
def change_password(request):
    if request.user.is_authenticated:
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password != confirm_password:
            passnotmatch = True
            return render(request, "my-account.html", {'passnotmatch': passnotmatch})
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "my-account.html", {'alert': alert})
            else:
                currpasswrong = True
                return render(request, "my-account.html", {'currpasswrong': currpasswrong})
        except:
            return render(request, "my-account.html", {'passnotmatch': passnotmatch})
    else:
        return render(request, "index.html")


# --------------------------------------------------------------------------------------
# product Details page
def product_Details(request, pk):
    product = Product.objects.get(pk=pk)
    imeges = Image_Product.objects.filter(product=product.pk)
    attribute = Attribute_product.objects.filter(product=product.pk)
    categories = Category.objects.all()
    category = Category.objects.get(pk=product.category.pk)
    related_products = Product.objects.filter(category=category.pk)
    attribute_value = []
    for att in attribute:
        attribute_value.append(att.attribute.name)
    MyAttributeset = set(attribute_value)
    attribute_value = list(MyAttributeset)

    spacification = Specification_Product.objects.filter(product=product.pk)
    prands = Prand.objects.all()
    tags = Tag_product.objects.filter(product=product.pk)
    products = Product.objects.all()
    prandinfo = []
    for pran in prands:
        count = 0
        pranditem = {}
        for prducta in products:

            if prducta.prand.pk == pran.pk:
                count += 1
        if count > 0:
            pranditem.update({"name": pran})
            pranditem.update({"count": count})
            pranditem.update({"pk": pran.pk})
            pranditem.update({"icon":pran.icon})
            prandinfo.append(pranditem)
    products_r = Product.objects.all().order_by('-created_at')
    recent_products = products_r[:10]
    review = Review.objects.filter(product=product.pk)

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        cartItems = order.get_cart_items

    else:

        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = order['get_cart_items']
    context = {
        'product': product,
        'imeges': imeges,
        'attributes': attribute,
        'attributeValue': attribute_value,
        'spacification': spacification,
        'recent_products': recent_products,
        'categories': categories,
        'category': category,
        'related_products': related_products,
        'prands': prandinfo,
        'tags': tags,
        'reviews': review,
        'cartItems': cartItems


    }
    if request.method == "POST":
        name = request.user.first_name
        email = request.user.email
        review = request.POST['review']
        review = Review.objects.create(name=name, email=email, review=review, product=product)
        review.save()
        return render(request, "product-detail.html", context)
    return render(request, "product-detail.html", context)


# --------------------------------------------------------------------------------------
# deeply all the products
def product_list(request):
    if request.user.is_authenticated:

        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    categories = Category.objects.all()
    prands = Prand.objects.all()
    tags = Tags.objects.all()
    prandinfo = []
    for pran in prands:
        count = 0
        pranditem = {}
        for prducta in products:
            if prducta.prand.pk == pran.pk:
                count += 1
        if count > 0:
            pranditem.update({"name": pran})
            pranditem.update({"count": count})
            pranditem.update({"pk": pran.pk})
            pranditem.update({'icon':pran.icon})
            prandinfo.append(pranditem)

    products_r = Product.objects.all().order_by('-created_at')
    recent_products = products_r[:10]
    context = {
        'products': products,
        'categories': categories,
        'prands': prandinfo,
        'tags': tags,
        'cartItems': cartItems,
        'recent_products': recent_products,
    }
    return render(request, "product-list.html", context)


# --------------------------------------------------------------------------------------
# desply all the products with pagination
def product_list_pagination(request, page):
    products = Product.objects.all()
    paginator = Paginator(products, per_page=9)
    page_object = paginator.get_page(page)
    categories = Category.objects.all()
    prands = Prand.objects.all()
    tags = Tags.objects.all()
    prandinfo = []
    for pran in prands:
        count = 0
        pranditem = {}
        for prducta in products:
            if prducta.prand.pk == pran.pk:
                count += 1
        if count > 0:
            pranditem.update({"name": pran})
            pranditem.update({"count": count})
            pranditem.update({"pk": pran.pk})
            pranditem.update({"icon":pran.icon})
            prandinfo.append(pranditem)

    products_r = Product.objects.all().order_by('-created_at')
    recent_products = products_r[:10]

    has_pre = page_object.has_previous()
    has_next = page_object.has_next()
    pre = page_object.number - 1
    next = page_object.number + 1
    context = {
        'products': page_object,
        'categories': categories,
        'prands': prandinfo,
        'recent_products': recent_products,
        'tags': tags,
        'page_num': page,
        'has_pre': has_pre,
        'has_next': has_next,
        'pre': pre,
        'next': next,
    }
    return render(request, "product-list.html", context)


# --------------------------------------------------------------------------------------
# desply all the products with pagination API
def product_list_api(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    prands = Prand.objects.all()
    tags = Tags.objects.all()
    prandinfo = []
    for pran in prands:
        count = 0
        pranditem = {}
        for prducta in products:
            if prducta.prand.pk == pran.pk:
                count += 1
        if count > 0:
            pranditem.update({"name": pran})
            pranditem.update({"count": count})
            pranditem.update({"pk": pran.pk})
            pranditem.update({"icon":pran.icon})
            prandinfo.append(pranditem)

    products_r = Product.objects.all().order_by('-created_at')
    recent_products = products_r[:10]
    context = {
        'products': products,
        'categories': categories,
        'prands': prandinfo,
        'tags': tags,
        'recent_products': recent_products,

    }
    return render(request, "product-list_api.html", context)


# ---------------------------------------------------------------------
# API for all products 
def listing_api(request):
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 9)
    keywords = Product.objects.all()
    paginator = Paginator(keywords, per_page)
    page_obj = paginator.get_page(page_number)
    data = [{"name": product.name, "price": product.price, "imge": product.image.url, "pk": product.pk} for product in
            page_obj.object_list]
    payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "page_range": len(paginator.page_range),

        },
        "data": data,

    }
    return JsonResponse(payload)


# ---------------------------------------------------------------------
# API for spacific category  
def listing_category_api(request, category_pk):
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 9)
    products = Product.objects.filter(category=category_pk)
    paginator = Paginator(products, per_page)
    page_obj = paginator.get_page(page_number)
    data = [{"name": product.name, "price": product.price, "imge": product.image.url, "pk": product.pk} for product in
            page_obj.object_list]
    payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "page_range": len(paginator.page_range),
            "category": category_pk

        },
        "data": data,

    }
    return JsonResponse(payload)


# -----------------------------------------------------------
# Prand products
def product_prand_list(request, prand_pk, page=1):
    products = Product.objects.filter(prand=prand_pk)
    categories = Category.objects.all()
    prands = Prand.objects.all()
    tags = Tags.objects.all()
    ProductsPrand = Prand.objects.get(pk=prand_pk)
    allProducts = Product.objects.all()
    paginator = Paginator(products, per_page=9)
    page_object = paginator.get_page(page)
    prandinfo = []
    for pran in prands:
        count = 0
        pranditem = {}
        for prducta in allProducts:
            if prducta.prand.pk == pran.pk:
                count += 1
        if count > 0:
            pranditem.update({"name": pran})
            pranditem.update({"count": count})
            pranditem.update({"pk": pran.pk})
            prandinfo.append(pranditem)
    products_r = Product.objects.all().order_by('-created_at')
    recent_products = products_r[:10]
    has_pre = page_object.has_previous()
    has_next = page_object.has_next()
    pre = page_object.number - 1
    next = page_object.number + 1
    context = {
        'products': page_object,
        'categories': categories,
        'tags': tags,
        'prands': prandinfo,
        'recent_products': recent_products,
        'ProductsPrand': ProductsPrand,
        'page_num': page,
        'has_pre': has_pre,
        'has_next': has_next,
        'pre': pre,
        'next': next
    }
    return render(request, "product-list.html", context)


# -----------------------------------------------------------
# Prand products
def product_tag_list(request, tag_pk, page=1):
    tags = Tag_product.objects.all()
    tag = Tags.objects.get(pk=tag_pk)
    my_products = []
    for item in tags:
        if item.tag.pk == tag_pk:
            prodct = Product.objects.get(pk=item.product.pk)
            my_products.append(prodct)
    categories = Category.objects.all()
    prands = Prand.objects.all()
    tags = Tags.objects.all()
    allProducts = Product.objects.all()
    prandinfo = []
    for pran in prands:
        count = 0
        pranditem = {}
        for prducta in allProducts:
            if prducta.prand.pk == pran.pk:
                count += 1
        if count > 0:
            pranditem.update({"name": pran})
            pranditem.update({"count": count})
            pranditem.update({"pk": pran.pk})
            prandinfo.append(pranditem)
    products_r = Product.objects.all().order_by('-created_at')
    recent_products = products_r[:10]

    paginator = Paginator(my_products, per_page=9)
    page_object = paginator.get_page(page)
    has_pre = page_object.has_previous()
    has_next = page_object.has_next()
    pre = page_object.number - 1
    next = page_object.number + 1
    context = {
        'products': page_object,
        'categories': categories,
        'tags': tags,
        'recent_products': recent_products,
        'prands': prandinfo,
        'tag': tag,
        'page_num': page,
        'has_pre': has_pre,
        'has_next': has_next,
        'pre': pre,
        'next': next
    }
    return render(request, "product-list.html", context)


# -----------------------------------------------------------
# Categoty Prand products
def product_category_prand_list(request, category_pk, prand_pk, page=1):
    products = Product.objects.filter(prand=prand_pk)
    categories = Category.objects.all()
    prands = Prand.objects.all()
    tags = Tags.objects.all()
    selected_products = []
    ProductsPrand = Prand.objects.get(pk=prand_pk)
    for product in products:
        print('aaaa')
        if product.category.pk == category_pk:
            selected_products.append(product)
            print('sss')
    category = Category.objects.get(pk=category_pk)
    allProducts = Product.objects.filter(category=category_pk)
    prandinfo = []
    for pran in prands:
        count = 0
        pranditem = {}
        for prducta in allProducts:
            if prducta.prand.pk == pran.pk:
                count += 1
        if count > 0:
            pranditem.update({"name": pran})
            pranditem.update({"count": count})
            pranditem.update({"pk": pran.pk})
            prandinfo.append(pranditem)

    products_r = Product.objects.all().order_by('-created_at')
    recent_products = products_r[:10]

    paginator = Paginator(selected_products, per_page=9)
    page_object = paginator.get_page(page)
    has_pre = page_object.has_previous()
    has_next = page_object.has_next()
    pre = page_object.number - 1
    next = page_object.number + 1
    cat_prand = {'category_pk': category_pk, 'prand_pk': prand_pk}

    context = {
        'products': page_object,
        'categories': categories,
        'category': category,
        'tags': tags,
        'prands': prandinfo,
        'recent_products': recent_products,
        'ProductsPrand': ProductsPrand,
        'cat_prand': cat_prand,
        'page_num': page,
        'has_pre': has_pre,
        'has_next': has_next,
        'pre': pre,
        'next': next

    }
    return render(request, "product-list.html", context)


# --------------------------------------------------------------------------------------
# filter the products based on it's price
def product_list_price(request, price_cat, page=1):
    products = Product.objects.all()
    categories = Category.objects.all()
    products_filtered = []
    max_price = 0
    min_price = 0
    price_text = ''
    if price_cat == 1:
        min_price = 0
        max_price = 50
        price_text = '$0 to $50'
    elif price_cat == 2:
        min_price = 50
        max_price = 100
        price_text = '$50 to $100'
    elif price_cat == 3:
        min_price = 100
        max_price = 150
        price_text = '$100 to $150'
    elif price_cat == 4:
        min_price = 150
        max_price = 200
        price_text = '$150 to $200'
    elif price_cat == 5:
        min_price = 200
        max_price = 250
        price_text = '$200 to $250'
    elif price_cat == 6:
        min_price = 250
        max_price = 300
        price_text = '$250 to $300'
    elif price_cat == 7:
        min_price = 300
        max_price = 350
        price_text = '$300 to $350'
    elif price_cat == 8:
        min_price = 350
        max_price = 400
        price_text = '$350 to $400'
    elif price_cat == 9:
        min_price = 400
        max_price = 450
        price_text = '$400 to $450'
    elif price_cat == 10:
        min_price = 450
        max_price = 3000
        price_text = '$450 to $3000'

    tags = Tags.objects.all()
    for product in products:
        if int(product.price) > min_price:
            if int(product.price) <= max_price:
                products_filtered.append(product)

    prands = Prand.objects.all()
    prandinfo = []
    for pran in prands:
        count = 0
        pranditem = {}
        for prducta in products_filtered:
            if prducta.prand.pk == pran.pk:
                count += 1
        if count > 0:
            pranditem.update({"name": pran})
            pranditem.update({"count": count})
            pranditem.update({"pk": pran.pk})
            prandinfo.append(pranditem)

    products_r = Product.objects.all().order_by('-created_at')
    recent_products = products_r[:10]

    paginator = Paginator(products_filtered, per_page=9)
    page_object = paginator.get_page(page)
    has_pre = page_object.has_previous()
    has_next = page_object.has_next()
    pre = page_object.number - 1
    next = page_object.number + 1
    context = {
        'products': page_object,
        'categories': categories,
        'price_cat': price_cat,
        'tags': tags,
        'recent_products': recent_products,
        'prands': prandinfo,
        'price_text': price_text,
        'page_num': page,
        'has_pre': has_pre,
        'has_next': has_next,
        'pre': pre,
        'next': next
    }
    return render(request, "product-list.html", context)


# --------------------------------------------------------------------------------------
# filter the products based on its price and categores
def product_list_priceAndCategory(request, category_pk, price_cat, page=1):
    products = Product.objects.filter(category=category_pk)
    category = Category.objects.get(pk=category_pk)
    categories = Category.objects.all()
    products_filtered = []
    max_price = 0
    min_price = 0
    price_text = ''
    if price_cat == 1:
        min_price = 0
        max_price = 50
        price_text = '$0 to $50'
    elif price_cat == 2:
        min_price = 50
        max_price = 100
        price_text = '$50 to $100'
    elif price_cat == 3:
        min_price = 100
        max_price = 150
        price_text = '$100 to $150'
    elif price_cat == 4:
        min_price = 150
        max_price = 200
        price_text = '$150 to $200'
    elif price_cat == 5:
        min_price = 200
        max_price = 250
        price_text = '$200 to $250'
    elif price_cat == 6:
        min_price = 250
        max_price = 300
        price_text = '$250 to $300'
    elif price_cat == 7:
        min_price = 300
        max_price = 350
        price_text = '$300 to $350'
    elif price_cat == 8:
        min_price = 350
        max_price = 400
        price_text = '$350 to $400'
    elif price_cat == 9:
        min_price = 400
        max_price = 450
        price_text = '$400 to $450'
    elif price_cat == 10:
        min_price = 450
        max_price = 3000
        price_text = '$450 to $3000'
    tags = Tags.objects.all()
    for product in products:
        if int(product.price) > min_price:
            if int(product.price) <= max_price:
                products_filtered.append(product)

    prands = Prand.objects.all()
    prandinfo = []
    for pran in prands:
        count = 0
        pranditem = {}
        for prducta in products:
            if prducta.prand.pk == pran.pk:
                count += 1
        if count > 0:
            pranditem.update({"name": pran})
            pranditem.update({"count": count})
            pranditem.update({"pk": pran.pk})
            prandinfo.append(pranditem)

    products_r = Product.objects.all().order_by('-created_at')
    recent_products = products_r[:10]

    paginator = Paginator(products_filtered, per_page=9)
    page_object = paginator.get_page(page)
    has_pre = page_object.has_previous()
    has_next = page_object.has_next()
    pre = page_object.number - 1
    next = page_object.number + 1

    cat_price = {'category_pk': category_pk, 'price_cat': price_cat}
    context = {
        'products': page_object,
        'categories': categories,
        'category': category,
        'price_cat': price_cat,
        'price_text': price_text,
        'tags': tags,
        'recent_products': recent_products,
        'prands': prandinfo,
        'cat_price': cat_price,
        'page_num': page,
        'has_pre': has_pre,
        'has_next': has_next,
        'pre': pre,
        'next': next
    }
    return render(request, "product-list.html", context)


# --------------------------------------------------------------------------------------
# filter the products based on it's category
def product_category(request, category_pk, page=1):
    products = Product.objects.filter(category=category_pk)
    category = Category.objects.get(pk=category_pk)
    categories = Category.objects.all()
    tags = Tags.objects.all()
    paginator = Paginator(products, per_page=9)
    page_object = paginator.get_page(page)
    prands = Prand.objects.all()
    prandinfo = []
    for pran in prands:
        count = 0
        pranditem = {}
        for prducta in products:
            if prducta.prand.pk == pran.pk:
                count += 1
        if count > 0:
            pranditem.update({"name": pran})
            pranditem.update({"count": count})
            pranditem.update({"pk": pran.pk})
            prandinfo.append(pranditem)

    products_r = Product.objects.all().order_by('-created_at')
    recent_products = products_r[:10]

    has_pre = page_object.has_previous()
    has_next = page_object.has_next()
    pre = page_object.number - 1
    next = page_object.number + 1
    current=page_object.number
    context = {
        'products': page_object,
        'category': category,
        'categories': categories,
        'recent_products': recent_products,
        'prands': prandinfo,
        'tags': tags,
        'page_num': page,
        'has_pre': has_pre,
        'has_next': has_next,
        'pre': pre,
        'next': next,
        'current':current
    }
    return render(request, "product-list.html", context)


# --------------------------------------------------------------------------------------
# desply all the products
def orderd_product_list(request, order_cat, page=1):
    if order_cat == 1:
        products = Product.objects.all().order_by('-created_at')
        order_style = 'Newest'
    elif order_cat == 2:
        products = Product.objects.all().order_by('created_at')
        order_style = 'Oldest'
    else:
        Product.objects.all()
    categories = Category.objects.all()
    prands = Prand.objects.all()
    tags = Tags.objects.all()
    paginator = Paginator(products, per_page=9)
    page_object = paginator.get_page(page)
    prandinfo = []
    for pran in prands:
        count = 0
        pranditem = {}
        for prducta in products:
            if (prducta.prand.pk == pran.pk):
                count += 1
        if count > 0:
            pranditem.update({"name": pran})
            pranditem.update({"count": count})
            pranditem.update({"pk": pran.pk})
            prandinfo.append(pranditem)

    products_r = Product.objects.all().order_by('-created_at')
    recent_products = products_r[:10]

    has_pre = page_object.has_previous()
    has_next = page_object.has_next()
    pre = page_object.number - 1
    next = page_object.number + 1

    context = {
        'products': page_object,
        'categories': categories,
        'prands': prandinfo,
        'tags': tags,
        'recent_products': recent_products,
        'order_style': order_style,
        'page_num': page,
        'has_pre': has_pre,
        'has_next': has_next,
        'pre': pre,
        'next': next,
        'order_cat': order_cat
    }
    return render(request, "product-list.html", context)


# -------------------------------------------------------------------------------------------
# Add Order in The Cart
@login_required(login_url='/login')
def cart(request):
    if request.user.is_authenticated:

        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = {"order.get_cart_items"}
    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,

    }

    return render(request, "cart.html", context)


# Create Checkout cart
@login_required(login_url='/login')
def checkout(request):
    if request.user.is_authenticated:
        user = request.user.id
        order, created = Order.objects.get_or_create(user=user, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {"get_cart_items": 0, "get_cart_total": 0}
    context = {
        "order": order,
        "cartItems": cartItems
    }
    return render(request, "checkout.html", context)


@login_required(login_url='/login')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    user = request.user
    product = Product.objects.get(pk=productId)
    order, created = Order.objects.get_or_create(user=user, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

# تحتاج الى تحسين

@login_required(login_url='/login')
def byNowItem(request,pk):
    if request.user.is_authenticated:
        product = Product.objects.get(pk=pk)
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        orderItem.quantity = (orderItem.quantity + 1)
        orderItem.save()
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = {"order.get_cart_items"}
        
    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,

    }
    return render(request,'cart.html',context)


def proccessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        order.transaction_id = transaction_id
        total = float(data['total'])
        if total == order.get_cart_total:
            order.complete = True
            order.save()
        else:
            print("order is not complete")

        if order.complete == True:
            ShippingAddress.objects.create(
                user=user,
                order=order,
                first_name=data['shipping']['first_name'],
                last_name=data['shipping']['last_name'],
                email=data['shipping']['email'],
                phone=data['shipping']['phone'],
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print("You are not authenticated")

    return JsonResponse('Payment subbmitted', safe=False)




# Home page
def home(request):
    products = Product.objects.all().order_by('-created_at')
    recent_products = products[:10]
    old_fetured_products = FeaturedProducut.objects.all().filter(xpiration_time__lt=timezone.now())
    for pr in old_fetured_products:
        pr.delete()
    fetured_products = FeaturedProducut.objects.all().filter(xpiration_time__gt=timezone.now())
    fetured_products = fetured_products[:10]

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        cartItems = order.get_cart_items

    else:

        order = {"get_cart_items": 0, "get_cart_total": 0}
        cartItems = order['get_cart_items']

    categories = Category.objects.all()
    slider = Slider.objects.filter(active=True)[:6]
    vertical_slider = Slider.objects.filter(active=True)[:2]
    category_side = Category_Side.objects.all().filter(active=True)[:6]

    if len(category_side) > 0:
        cat_side1 = category_side[0]
    else:
        cat_side1 = None
    if len(category_side) > 1:
        cat_side2 = category_side[1]
    else:
        cat_side2 = None
    if len(category_side) > 2:
        cat_side3 = category_side[2]
    else:
        cat_side3 = None
    if len(category_side) > 3:
        cat_side4 = category_side[3]
    else:
        cat_side4 = None
    if len(category_side) > 4:
        cat_side5 = category_side[4]
    else:
        cat_side5 = None
    if len(category_side) > 5:
        cat_side6 = category_side[5]
    else:
        cat_side6 = None

    prands = Prand.objects.all()
    prandinfo=[]
    for pran in prands :
        count=0
        pranditem = {}
        for prducta in products:
            if(prducta.prand.pk==pran.pk):
                count+=1
        if count>0:
            pranditem.update({"name":pran})
            pranditem.update({"count":count})
            pranditem.update({"pk":pran.pk})
            pranditem.update({"icon":pran.icon})
            prandinfo.append(pranditem)
            
    if request.user.is_authenticated:
        wish = Wishlist.objects.filter(user=request.user).count()
        wishlist = int(wish)
    else:
        wishlist = 0
    context = {
        'categories': categories,
        'slider': slider,
        'recent_products': recent_products,
        'fetured_products': fetured_products,
        "category_Side": category_side,
        "vertical_slider": vertical_slider,
        "cat_side1": cat_side1,
        "cat_side2": cat_side2,
        "cat_side3": cat_side3,
        "cat_side4": cat_side4,
        "cat_side5": cat_side5,
        "cat_side6": cat_side6,
        "cartItems": cartItems,
        'prands':prandinfo,
        'wish':wishlist,

    }
    return render(request, "index.html", context)


@login_required(login_url='/login')
def contact(request):
    if request.method == "POST":
        subject = request.POST['subject']
        
        message = request.POST['message']
        data_user = Register_models.objects.get(user=request.user)
        email = data_user.user.email
        subjectfrom = "User Email is : " + email +" Subject : "
        Massage1 = subjectfrom+message
        send_mail(
            subject,
            Massage1,
            email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        Contact.objects.create(email=email, subject=subject, message=message)
        return render(request, "contact.html")
    return render(request, "contact.html")


def Logout(request):
    logout(request)
    return redirect("/")

@login_required(login_url='/login')
def wishlist(request):
   
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist':wishlist
    }
    return render(request,"wishlist.html",context)
    
@login_required(login_url='/login')
def addToWishlist(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    if request.method == "POST":
        product_check = Product.objects.get(id=product_id)
        if product_check: 
            if(Wishlist.objects.filter(user=request.user,product_id=product_id)):
                return JsonResponse('Product already in wishlist', safe=False)
            else:
                Wishlist.objects.create(user=request.user,product_id=product_id)
                return JsonResponse('Product already in wishlist', safe=False)
        else:
            return JsonResponse('No such product found', safe=False)
    else:
        return JsonResponse('Login to continue', safe=False)
    return redirect("/")


def delete_cart(request,pk):
    if request.user.is_authenticated:
       
        item = OrderItem.objects.filter(product=pk)
        if item:
            item.delete()
            return HttpResponseRedirect(reverse("cart"))
        else:
            return HttpResponseRedirect(reverse("cart"))
    return HttpResponseRedirect(reverse("cart"))