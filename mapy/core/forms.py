from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from core.models import User, ShippingAddress

"""""
START MODIFICATION
"""""
Usuario = get_user_model()

class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=32,required=True,
                           widget= forms.TextInput
                           (attrs={'type':'text','class':'form-control',
				                   'name':'firstName','id':'fullNameSrEmail','placeholder':'Roger',
                                   'aria-label':'Roger','data-msg':'Please write your first name.','autocomplete':'off'}))

    last_name = forms.CharField(max_length=32,required=True,
                           widget= forms.TextInput
                           (attrs={'type':'text','class':'form-control',
				                   'name':'lastName','placeholder':'Federer',
                                   'aria-label':'Federer','data-msg':'Please write your last name.','autocomplete':'off'}))

    email = forms.CharField(max_length=32,required=True,
                           widget= forms.TextInput
                           (attrs={'type':'email','class':'form-control',
				                   'name':'email','id':'signupSrEmail','placeholder':'rogerfederer@example.com',
                                   'aria-label':'Federer@example.com','data-msg':'Please write your email.'}))

    password1 = forms.CharField(max_length=100,required=True,
                           widget= forms.TextInput
                           (attrs={'type':'password','class':'form-control','autocomplete':'off',
				                   'name':'password','placeholder':'8+ caracteres requeridos',
                                   'aria-label':'8+ caracteres requeridos','data-msg':'Please try again, invalid passowrd.',
                                   'data-hs-toggle-password-options':'{"target": [".js-toggle-password-target-1", ".js-toggle-password-target-2"],"defaultClass": "tio-hidden-outlined","showClass": "tio-visible-outlined", "classChangeTarget": ".js-toggle-passowrd-show-icon-1"}'}))


    password2 = forms.CharField(max_length=100,required=True,
                           widget= forms.TextInput
                           (attrs={'type':'password','class':'form-control','autocomplete':'off',
                                   'name':'confirmPassword','placeholder':'8+ caracteres requeridos',
                                   'aria-label':'8+ caracteres requeridos','data-msg':'Your second password do not do not coincide with the first one.',
                                   'data-hs-toggle-password-options':'{"target":[".js-toggle-password-target-1", ".js-toggle-password-target-2"],"defaultClass": "tio-hidden-outlined","showClass": "tio-visible-outlined","classChangeTarget": ".js-toggle-passowrd-show-icon-2"}'}))


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email','password1','password2','first_name','last_name']


class UserLoginForm(forms.ModelForm):
    email = forms.CharField(max_length=32,required=True,
                               widget= forms.TextInput
                               (attrs={'type':'email','class':'form-control',
    				                   'name':'email','placeholder':'rogerfederer@example.com',
                                       'aria-label':'Federer@example.com','data-msg':'Your email is invalid.'}))

    password = forms.CharField(max_length=100,required=True,
                           widget= forms.TextInput
                           (attrs={'type':'password','class':'form-control','autocomplete':'off',
				                   'name':'password','placeholder':'8+ caracteres requeridos',
                                   'aria-label':'8+ caracteres requeridos','data-msg':'Your second password do not do not coincide with the first one.',
                                   'data-hs-toggle-password-options':'{"target": [".js-toggle-password-target-1", ".js-toggle-password-target-2"],"defaultClass": "tio-hidden-outlined","showClass": "tio-visible-outlined", "classChangeTarget": ".js-toggle-passowrd-show-icon-1"}'}))

    # password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('email','password')

class PaymentForm(forms.Form):
    holder_name = forms.CharField(max_length=64, required=True,
                               widget= forms.TextInput
                               (attrs={'type':'text','class':'form-control',
    				                   'name':'holder_name','placeholder':'Full Name',
                                       'aria-label':'Full Name','data-msg':'Please write your name.'}))
    expiration_month = forms.IntegerField(min_value=0, max_value=2, required=True,
                                        widget= forms.TextInput
                                        (attrs={'type':'number','class':'form-control',
                                                'name':'expiration_month','placeholder':'MM',
                                                'aria-label':'MM','data-msg':'Please write the expiration month.'}))
    expiration_year = forms.IntegerField(min_value=0, max_value=2, required=True,
                                        widget= forms.TextInput
                                        (attrs={'type':'number','class':'form-control',
                                                'name':'expiration_year','placeholder':'YY',
                                                'aria-label':'YY','data-msg':'Please write the expiration year.'}))
    cvc = forms.IntegerField(min_value=0, max_value=3, required=True,
                                widget= forms.TextInput
                                (attrs={'type':'number','class':'form-control',
                                        'name':'cvc','placeholder':'CVC',
                                        'aria-label':'CVC','data-msg':'Please write the CVC.'}))


class ShippingForm(forms.Form):
    holder_name = forms.CharField(max_length=64, required=True,
                               widget= forms.TextInput
                               (attrs={'type':'text','class':'form-control',
    				                   'name':'holder_name','placeholder':'Full Name',
                                       'aria-label':'Full Name','data-msg':'Please write your name.'}))
    shipping_address = forms.CharField(required=True,
                                    widget= forms.TextInput
                                    (attrs={'type':'text','class':'form-control',
                                    'name':'shipping_address','placeholder':'Shipping Address',
                                    'aria-label':'Shipping Address','data-msg':'Please write address.'}))

    shipping_zip = forms.CharField(required=False,
                                    widget= forms.TextInput
                                    (attrs={'type':'number','class':'form-control',
                                            'name':'shipping_zip','placeholder':'Shipping Zip',
                                            'aria-label':'YY','data-msg':'Please write the shipping zip.'}))
    phone_number = forms.IntegerField(min_value=0, max_value=2, required=True,
                                        widget= forms.TextInput
                                        (attrs={'type':'number','class':'form-control',
                                                'name':'phone_number','placeholder':'Phone number',
                                                'aria-label':'Phone number','data-msg':'Please write your phone number.'}))
    instructions = forms.CharField(max_length=64,
                               widget= forms.TextInput
                               (attrs={'type':'text','class':'form-control',
    				                   'name':'instructions','placeholder':'Instructions to find your place',
                                       'aria-label':'Instructions','data-msg':'Please how we can find your place.'}))

    country = CountryField().formfield(widget=CountrySelectWidget(
           attrs={'class':'form-control','name':'country',
           'aria-label':'country','data-msg':'Please select your country.'}
        ))

    class Meta(UserCreationForm.Meta):
        model = ShippingAddress
        fields = ['holder_name','shipping_address','shipping_zip','phone_number','instructions','country']
"""""
END MODIFICATION
"""""
