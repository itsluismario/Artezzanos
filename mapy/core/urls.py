from django.urls import path,include
from core import views
from django.conf.urls import url

app_name = 'core'

urlpatterns = [
    path('', views.index, name="index"),
    path('login/',views.user_login, name="login"),
    path('signup/',views.user_signup, name="signup"),
    path('logout/', views.user_logout, name='logout'),
    path('cart', views.shop_cart, name='cart'),
    path('artist/<int:artist_id>', views.artist, name='artist'),
    path('item/<int:item_id>', views.item, name='item'),
    path('update_item',views.update_item, name='updateItem'),
    path('delete_item',views.delete_item, name='deleteItem'),
    path('payment',views.payment, name='payment'),
    path('shipping',views.shipping, name='shipping')
]
