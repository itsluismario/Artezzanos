
from django.urls import re_path, path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserPasswordResetForm

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
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html',
         form_class=UserPasswordResetForm),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete')
]
