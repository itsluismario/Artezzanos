from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, logout as do_logout, login as do_login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from core.forms import UserSignUpForm, UserLoginForm, PaymentForm, ShippingForm

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse

from core.models import Item, Artist, CartHeader, CartBody, ShippingAddress, Payment, Category, SubCategory, About, TeamMemeber, FAQ

from django.conf import settings

from django.contrib.auth.forms import AuthenticationForm

from django.core.paginator import Paginator

import openpay

import itertools

User = settings.AUTH_USER_MODEL











def categories(request):
    login_user = request.user.is_authenticated

    categories = Category.objects.filter().all()
    subcategories = SubCategory.objects.filter().all()

    try:
        car = CartHeader.objects.get(pk=request.COOKIES["cookieCar"])
    except:
        car = None
    # Reminder: You can use exist() when you have first()
    if car == None:
        if login_user:
            car = CartHeader.objects.create(user=request.user,total=0,quantity=0)
        else:
            car = CartHeader.objects.create(total=0,quantity=0)

    if 'subcategory_id' in request.GET:
        subobj = SubCategory.objects.get(pk=request.GET["subcategory_id"])
        obj = Item.objects.filter(subcategory=SubCategory.objects.get(pk=request.GET["subcategory_id"]))
    else:
        obj =  Item.objects.all()

    paginate = Paginator(obj,4)
    page_number = request.GET.get('page')
    page_obj = paginate.get_page(page_number)
    return render(request,'categories.html', {
        'items': page_obj,
        'car': car,
        'categories': categories,
        'subcategories': subcategories,
        'subobj': subobj,
    })












def index(request):
    login_user = request.user.is_authenticated

    categories = Category.objects.filter().all()
    subcategories = SubCategory.objects.filter().all()

    try:
        car = CartHeader.objects.get(pk=request.COOKIES["cookieCar"])
    except:
        car = None
    # Reminder: You can use exist() when you have first()
    if car == None:
        if login_user:
            car = CartHeader.objects.create(user=request.user,total=0,quantity=0)
        else:
            car = CartHeader.objects.create(total=0,quantity=0)

    obj =  Item.objects.all()

    paginate = Paginator(obj,4)
    page_number = request.GET.get('page')
    page_obj = paginate.get_page(page_number)
    return render(request,'index.html', {
        'items': page_obj,
        'car': car,
        'categories': categories,
        'subcategories': subcategories,
    })











def update_item(request):
    # Find the item with this ID
    item = Item.objects.get(pk=request.GET["id_item"])
    # Find the cartBody with this item
    cartWithThisItem = CartBody.objects.get(item=item)

    # Find the quantity of item that the user wants to add
    addQuantityItem = int(request.GET["quatityItem"])-cartWithThisItem.quantityByItems

    # Sum the new quantity
    cartWithThisItem.quantityByItems = addQuantityItem + cartWithThisItem.quantityByItems

    # Calculate the subtotal
    cartWithThisItem.subtotal = item.price*cartWithThisItem.quantityByItems
    cartWithThisItem.save()

    # All the items of the car
    items = CartBody.objects.filter(cartHeader__pk=request.COOKIES["cookieCar"])

    car = cartWithThisItem.cartHeader
    total_tmp=0
    quantity_tmp = 0
    for item in items:
        total_tmp = total_tmp+item.subtotal
        quantity_tmp = quantity_tmp+item.quantityByItems
    car.total = total_tmp
    car.quantity = quantity_tmp
    car.save()

    return JsonResponse({'success':False,
                        'total': car.total,
                        'quantity': car.quantity
                        })











def delete_item(request):
        # Find the carHeader
        car = CartHeader.objects.get(pk=request.COOKIES["cookieCar"])
        print(car)
        # Find the item with this ID
        item = Item.objects.get(pk=request.GET["id_item"])
        print(item)

        # All the items of the car
        items = CartBody.objects.filter(cartHeader=car)

        # Find the cartBody with this item
        cartWithThisItem = CartBody.objects.get(item=item, cartHeader=car)

        # Delete the cartBody of the cartHeader
        cartWithThisItem.delete()

        total_tmp=0
        quantity_tmp = 0
        for item in items:
            total_tmp = total_tmp+item.subtotal
            quantity_tmp = quantity_tmp+item.quantityByItems

        car.total = total_tmp
        car.quantity = quantity_tmp
        car.save()
        print(car)

        return JsonResponse({'success':False,
                            'total': car.total,
                            'quantity': car.quantity
                            })











def artist(request):
    login_user = request.user.is_authenticated
    categories = Category.objects.filter().all()
    subcategories = SubCategory.objects.filter().all()

    try:
        car = CartHeader.objects.get(pk=request.COOKIES["cookieCar"])
    except:
        car = None
    # Reminder: You can use exist() when you have first()
    if car == None:
        if login_user:
            car = CartHeader.objects.create(user=request.user,total=0,quantity=0)
        else:
            car = CartHeader.objects.create(total=0,quantity=0)
    return render(request,'artist.html', {
        "artist": Artist.objects.get(pk=request.GET["artist_id"]),
        "items": Item.objects.select_related('artist').filter(artist=request.GET["artist_id"]).exclude(pk=request.GET["item_id"]),
        'car': car,
        "item": Item.objects.get(pk=request.GET["item_id"]),
        'categories': categories,
        'subcategories': subcategories,
    })









def shop_cart(request):
    login_user = request.user.is_authenticated
    categories = Category.objects.filter().all()
    subcategories = SubCategory.objects.filter().all()

    try:
        car = CartHeader.objects.get(pk=request.COOKIES["cookieCar"])
    except:
        car = None
    # Reminder: You can use exist() when you have first()
    if car == None:
        if login_user:
            car = CartHeader.objects.create(user=request.user,total=0,quantity=0)
        else:
            car = CartHeader.objects.create(total=0,quantity=0)

    if "item" in request.GET:

        # Try to search the item in the CarBody
        item = Item.objects.get(pk=request.GET["item"])
        try:
            cartWithThisItem = CartBody.objects.get(item=item,cartHeader=car)
        except:
            cartWithThisItem = None
        # If it is not in the CartBody
        if cartWithThisItem == None:
            # Create a new one
            CartBody.objects.create(item=item,cartHeader=car,subtotal=item.price,quantityByItems=1)

        else:
            # If it is, add the price of the item and one quantity
            cartWithThisItem.quantityByItems = 1 + cartWithThisItem.quantityByItems
            cartWithThisItem.subtotal = item.price*cartWithThisItem.quantityByItems
            cartWithThisItem.save()
        return redirect('/cart')
    # All the items of the car
    items = CartBody.objects.filter(cartHeader=car)

    total_tmp=0
    quantity_tmp = 0
    for item in items:
        print(item.item.artist.id)
        total_tmp = total_tmp+item.subtotal
        quantity_tmp = quantity_tmp+item.quantityByItems
    car.total = total_tmp
    car.quantity = quantity_tmp
    car.save()

    returnHTML = render(request,'shop_cart.html', {
        'car': car,
        'items': items,
        'categories': categories,
        'subcategories': subcategories,
    })
    returnHTML.set_cookie("cookieCar",car.id)
    return returnHTML











def shipping(request):
    login_user = request.user.is_authenticated
    categories = Category.objects.filter().all()
    subcategories = SubCategory.objects.filter().all()

    if login_user:
        shippingaddressess = ShippingAddress.objects.filter(user=request.user)
        car = CartHeader.objects.get(pk=request.COOKIES["cookieCar"])
        items = CartBody.objects.filter(cartHeader=car)

        form = ShippingForm()

        if request.method == "POST":
            shipping_form = ShippingForm(data=request.POST)

            if shipping_form.is_valid():
                obj = shipping_form.save(commit=False)
                obj.user = request.user
                obj.cartheader = car
                obj.save()

                car.user = request.user
                car.save()

                print('Saved!')

                return redirect("/payment"+ '?id=' + str(obj.id))

            else:
                print(shipping_form.errors)
                # HERE SHOULD SEND A MESSAGE !!!!!
                return render(request,'shipping_address.html',{
                    'form': form,
                    'car': car,
                    'items': items,
                    'errors':shipping_form.errors,
                    'shippingaddressess': shippingaddressess,
                    'categories': categories,
                    'subcategories': subcategories
                })

        return render(request,'shipping_address.html', {
            'form': form,
            'car': car,
            'items': items,
            'shippingaddressess': shippingaddressess,
            'categories': categories,
            'subcategories': subcategories
            })
    else:
        return redirect("/login")











def payment(request):
    categories = Category.objects.filter().all()
    subcategories = SubCategory.objects.filter().all()
    form = PaymentForm()
    errors = None
    car = CartHeader.objects.get(pk=request.COOKIES["cookieCar"])

    # Create a list for the cart description
    items = CartBody.objects.filter(cartHeader=car)
    listItems = ""
    for item in items:
        if listItems == "":
            listItems = str(item.item)
        else:
            listItems = listItems+","+str(item.item)

    if 'id' in request.GET:
        shippingaddress = ShippingAddress.objects.get(pk=request.GET["id"])

    if request.method == "POST":

        try:
            # Check all the customers
            customers = openpay.Customer.all()
            # customer1 = openpay.Customer.retrieve()
            # Crear un usuario openpay al entrar shipping_address
            # Guardar un token = al id de openpay
            # Revisar con retrive si ya existe un token y sino crear uno
            # Fun verifique el usuario de openpay (revisr is el toke existe en mis db .... revisen si existen un token si si envia que si o no existen)
            # Otra verfique las direcciones openpay

            for customer in customers["data"]:
                userEmail=request.user.email
                # Check if OpenPay has already a user with the same email as the username
                if customer["email"] == userEmail:
                    # Check if the customer already exist
                    customer = openpay.Customer.retrieve(customer["id"])
                    """
                    NOTE: The customer might have many cards
                    """
                    # Check if the customer´s card already exist
                    cards = customer.cards.all()
                    for card in cards["data"]:
                        card = customer.cards.retrieve(card["id"])
                        if not card:
                            # Create a card for the customer
                            card = customer.cards.create(
                            	card_number=request.POST["card_number"],
                            	holder_name=request.POST["holder_name"],
                            	expiration_year=request.POST["expiration_year"],
                            	expiration_month=request.POST["expiration_month"],
                            	cvv2=request.POST["cvc"]
                            )
                        # Create a transfer for the customer
                        charge = customer.charges.create(
                            source_id=card.id,
                            method="card",
                            amount=car.total,
                            description=listItems, #Products
                            redirect_url='http://127.0.0.1:8000/thanks', # Thanks page
                            device_session_id=request.POST["csrfmiddlewaretoken"], # csrf_token
                        )

                # if the customer DOES NOT exist
                else:
                    # Create an user where it is saved as customer
                    customer = openpay.Customer.create(
                    name=request.user.first_name,
                    email=request.user.email,
                    address={
                        "city": shippingaddress.city,
                        "state":shippingaddress.state,
                        "line1":shippingaddress.street_address,
                        "postal_code":shippingaddress.shipping_zip,
                        "line2":shippingaddress.instructions,
                        "country_code":shippingaddress.country
                    },
                    last_name=request.user.last_name,
                    phone_number=shippingaddress.phone_number
                    )
                    # Create a card for the customer
                    card = customer.cards.create(
                    	card_number=request.POST["card_number"],
                        holder_name=request.POST["holder_name"],
                        expiration_year=request.POST["expiration_year"],
                        expiration_month=request.POST["expiration_month"],
                        cvv2=request.POST["cvc"]
                    )
                    # Create a transfer for the customer
                    charge = customer.charges.create(
                        source_id=card.id,
                        method="card",
                        amount=car.total,
                        description=listItems, #Product
                        redirect_url='http://127.0.0.1:8000/thanks', # Thanks page
                        device_session_id=request.POST["csrfmiddlewaretoken"], # csrf_token
                    )

                    print(request.POST["csrfmiddlewaretoken"])

        except Exception as e:
            print(e)
            raise
    else:
        print("Payment Error")

    return render(request,'payment.html', {
        'form': form,
        'car': car,
        'items': items,
        'shippingaddress': shippingaddress,
        'errors':form.errors,
        'categories': categories,
        'subcategories': subcategories
        })









def thanks(request):
    categories = Category.objects.filter().all()
    subcategories = SubCategory.objects.filter().all()
    return render(request,'thanks_page.html', {
        'categories': categories,
        'subcategories': subcategories
        })









def not_found(request):
    categories = Category.objects.filter().all()
    subcategories = SubCategory.objects.filter().all()
    return render(request,'not_found.html', {
        'categories': categories,
        'subcategories': subcategories
        })











def edit(request):
    categories = Category.objects.filter().all()
    subcategories = SubCategory.objects.filter().all()
    login_user = request.user.is_authenticated
    shippingaddressess = ShippingAddress.objects.filter(user=request.user)
    if login_user:

        car = CartHeader.objects.get(pk=request.COOKIES["cookieCar"])
        items = CartBody.objects.filter(cartHeader=car)
        if "id" in request.GET:
            subobj = ShippingAddress.objects.get(pk=request.GET["id"])
            print(subobj)
        else:
            subobj = None

        form = ShippingForm(instance=subobj)

        if request.method == "POST":
            shipping_form = ShippingForm(data=request.POST,instance=subobj)

            if shipping_form.is_valid():
                obj = shipping_form.save(commit=False)
                obj.user = request.user
                obj.cartheader = car
                obj.save()

                car.user = request.user
                car.save()

                print('Saved!')
                return redirect("/shipping")

            else:
                print(shipping_form.errors)
                # HERE SHOULD SEND A MESSAGE !!!!!
                return render(request,'edit_address.html',{
                    'form': form,
                    'car': car,
                    'items': items,
                    'errors':shipping_form.errors,
                    'shippingaddressess': shippingaddressess,
                    'categories': categories,
                    'subcategories': subcategories,
                })

        return render(request,'edit_address.html', {
            'form': form,
            'car': car,
            'items': items,
            'shippingaddressess': shippingaddressess,
            'categories': categories,
            'subcategories': subcategories,
            })
    else:
        return redirect("/login")










def user_login(request):
    categories = Category.objects.filter().all()
    subcategories = SubCategory.objects.filter().all()
    form = UserLoginForm()
    # If the user is not log in send to "/"
    if not request.user.is_authenticated:

        if request.method == 'POST':
            user = authenticate(username=request.POST['email'], password=request.POST['password'])

            if user is not None:
                print("Login")

                # verifica si existe cookie
                if "cookieCar" in request.session:

                    carWithThisCookie = CartHeader.objects.get(pk=request.COOKIES["cookieCar"])

                    # verifica si existe el carrito
                    if carWithThisCookie is not None:

                        # asigna el carrito al usuario
                        carWithThisCookie.user = user

                        # guardas carrito
                        carWithThisCookie.save()

                        # iniciar sesion
                        do_login(request,user)
                        # Redirect to a success page.
                        return redirect("/cart")

                do_login(request,user)
                # Redirect to a success page.
                return redirect("/")
            else:
                print(form.errors)

    return render(request,'login.html', {
        'form': form,
        'categories': categories,
        'subcategories': subcategories
        })











def user_signup(request):
    categories = Category.objects.filter().all()
    subcategories = SubCategory.objects.filter().all()
    form = UserSignUpForm()
    # If the user is logged in send to "/"
    if not request.user.is_authenticated:

        if request.method == "POST":
            user_form = UserSignUpForm(data=request.POST)

            if user_form.is_valid():
                # email = user_form.cleaned_data['email']
                user = user_form.save(commit=False)
                user.username = user.email
                user.first_name = user.first_name
                user.last_name = user.last_name

                if user.save():
                     return render(request,'signup.html',{
                         'form':form,
                         'errors':'The user already exist',
                         'categories': categories,
                         'subcategories': subcategories,
                     })
                else:
                    user.set_password(user.password)
                    user.save()
                    print('saved!')
                    do_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    # Redirect to a success page.
                    return redirect("/")

                    # do_login(request,user)
                    # return user_signup(request)
            else:
                print(user_form.errors)
                # HERE SHOULD SEND A MESSAGE !!!!!
                return render(request,'signup.html',{
                    'form':form,
                    'errors':user_form.errors,
                    'categories': categories,
                    'subcategories': subcategories,
                })

        form = UserSignUpForm()
        return render(request,"signup.html",{
            'form': form,
            'categories': categories,
            'subcategories': subcategories,
        })
    else:
        return redirect( "/" )











@login_required
def user_logout(request):
    do_logout(request)
    return HttpResponseRedirect(reverse('core:index'))











def about(request):
    categories = Category.objects.filter().all()
    subcategories = SubCategory.objects.filter().all()
    about = About.objects.get(pk=1)
    members = TeamMemeber.objects.filter().all()
    faqs = FAQ.objects.filter().all()

    return render(request,'about.html', {
        'about': about,
        'members': members,
        'faqs': faqs,
        'categories': categories,
        'subcategories': subcategories,
        })
