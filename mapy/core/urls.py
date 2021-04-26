from django.urls import path,include
from core import views
from django.conf.urls import url

app_name = 'core'

urlpatterns = [
    path('', views.index, name="index"),
    path('categories', views.categories, name="categories"),
    path('login',views.user_login, name="login"),
    path('signup/',views.user_signup, name="signup"),
    path('logout/', views.user_logout, name='logout'),
    path('cart', views.shop_cart, name='cart'),
    path('artist', views.artist, name='artist'),
    path('update_item',views.update_item, name='updateItem'),
    path('delete_item',views.delete_item, name='deleteItem'),
    path('payment',views.payment, name='payment'),
    path('shipping',views.shipping, name='shipping'),
    path('edit',views.edit, name='edit'),
    path('about',views.about, name='about'),
    path('thanks',views.thanks, name='thanks'),
    path('404',views.not_found, name='notFound'),
]
