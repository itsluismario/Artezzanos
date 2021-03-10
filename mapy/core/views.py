from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, logout as do_logout, login as do_login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from core.forms import UserSignUpForm, UserLoginForm, PaymentForm, ShippingForm

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse

from core.models import Item, Artist, CartHeader, CartBody

from django.conf import settings

from django.contrib.auth.forms import AuthenticationForm

from django.core.paginator import Paginator


User = settings.AUTH_USER_MODEL

def index(request):
    login_user = request.user.is_authenticated

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
        "items": page_obj,
        'car': car
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

def artist(request, artist_id):
    login_user = request.user.is_authenticated

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
        "artist": Artist.objects.get(pk=artist_id),
        "items": Item.objects.select_related('artist').filter(artist=artist_id),
        'car': car
    })

def item(request, item_id):
    login_user = request.user.is_authenticated

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
    return render(request,'item.html', {
        "item": Item.objects.get(pk=item_id),
        "car": car
    })

def shop_cart(request):
    login_user = request.user.is_authenticated

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
        total_tmp = total_tmp+item.subtotal
        quantity_tmp = quantity_tmp+item.quantityByItems
    car.total = total_tmp
    car.quantity = quantity_tmp
    car.save()

    returnHTML = render(request,'shop-cart.html', {
        'car': car,
        'items': items
    })
    returnHTML.set_cookie("cookieCar",car.id)
    return returnHTML

def payment(request):
    form = PaymentForm()
    car = CartHeader.objects.get(pk=request.COOKIES["cookieCar"])
    items = CartBody.objects.filter(cartHeader=car)
    return render(request,'payment.html', {
        'form': form,
        'car': car,
        'items': items
        })

def shipping(request):
    form = ShippingForm()
    car = CartHeader.objects.get(pk=request.COOKIES["cookieCar"])
    items = CartBody.objects.filter(cartHeader=car)
    if request.method == "POST":
        shipping_form = ShippingForm(data=request.POST)

        if shipping_form.is_valid():
            shipping = shipping_form.save(commit=False)
            shipping.save()
            print('Saved!')
        else:
            print(shipping_form.errors)
            # HERE SHOULD SEND A MESSAGE !!!!!
            return render(request,'shipping_address.html',{
                'form': form,
                'car': car,
                'items': items,
                'errors':shipping_form.errors
            })

    return render(request,'shipping_address.html', {
        'form': form,
        'car': car,
        'items': items
        })

def user_login(request):
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
        'form': form
        })

def user_signup(request):
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
                         'errors':'The user already exist'
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
                    'errors':user_form.errors
                })

        form = UserSignUpForm()
        return render(request,"signup.html",{
            'form': form
        })
    else:
        return redirect( "/" )

@login_required
def user_logout(request):
    do_logout(request)
    return HttpResponseRedirect(reverse('core:index'))
