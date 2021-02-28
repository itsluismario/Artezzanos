from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from core.models import User

"""""
START MODIFICATION
"""""
Usuario = get_user_model()

class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=32,required=True,
                           widget= forms.TextInput
                           (attrs={'type':'text','class':'form-control',
				                   'name':'firstName','id':'fullNameSrEmail','placeholder':'Roger',
                                   'aria-label':'Roger','data-msg':'Por favor pon tu nombre.','autocomplete':'off'}))

    last_name = forms.CharField(max_length=32,required=True,
                           widget= forms.TextInput
                           (attrs={'type':'text','class':'form-control',
				                   'name':'lastName','placeholder':'Federer',
                                   'aria-label':'Federer','data-msg':'Por favor pon tu apellido.','autocomplete':'off'}))

    email = forms.CharField(max_length=32,required=True,
                           widget= forms.TextInput
                           (attrs={'type':'email','class':'form-control',
				                   'name':'email','id':'signupSrEmail','placeholder':'rogerfederer@example.com',
                                   'aria-label':'Federer@example.com','data-msg':'Por favor introduce un email valido.'}))

    password1 = forms.CharField(max_length=100,required=True,
                           widget= forms.TextInput
                           (attrs={'type':'password','class':'form-control','autocomplete':'off',
				                   'name':'password','placeholder':'8+ caracteres requeridos',
                                   'aria-label':'8+ caracteres requeridos','data-msg':'Por favor intenta de nuevo, tu contraseña es invalida.',
                                   'data-hs-toggle-password-options':'{"target": [".js-toggle-password-target-1", ".js-toggle-password-target-2"],"defaultClass": "tio-hidden-outlined","showClass": "tio-visible-outlined", "classChangeTarget": ".js-toggle-passowrd-show-icon-1"}'}))


    password2 = forms.CharField(max_length=100,required=True,
                           widget= forms.TextInput
                           (attrs={'type':'password','class':'form-control','autocomplete':'off',
                                   'name':'confirmPassword','placeholder':'8+ caracteres requeridos',
                                   'aria-label':'8+ caracteres requeridos','data-msg':'Tu contraseña no coincide.',
                                   'data-hs-toggle-password-options':'{"target":[".js-toggle-password-target-1", ".js-toggle-password-target-2"],"defaultClass": "tio-hidden-outlined","showClass": "tio-visible-outlined","classChangeTarget": ".js-toggle-passowrd-show-icon-2"}'}))


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email','password1','password2','first_name','last_name']


class UserLoginForm(forms.ModelForm):
    email = forms.CharField(max_length=32,required=True,
                               widget= forms.TextInput
                               (attrs={'type':'email','class':'form-control',
    				                   'name':'email','placeholder':'rogerfederer@example.com',
                                       'aria-label':'Federer@example.com','data-msg':'Por favor introduce un email valido.'}))

    password = forms.CharField(max_length=100,required=True,
                           widget= forms.TextInput
                           (attrs={'type':'password','class':'form-control','autocomplete':'off',
				                   'name':'password','placeholder':'8+ caracteres requeridos',
                                   'aria-label':'8+ caracteres requeridos','data-msg':'Por favor intenta de nuevo, tu contraseña es invalida.',
                                   'data-hs-toggle-password-options':'{"target": [".js-toggle-password-target-1", ".js-toggle-password-target-2"],"defaultClass": "tio-hidden-outlined","showClass": "tio-visible-outlined", "classChangeTarget": ".js-toggle-passowrd-show-icon-1"}'}))

    # password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('email','password')

class PaymentForm(forms.Form):
    holder_name = forms.CharField(max_length=64,required=True)
    expiration_year = forms.IntegerField(min_value=0, max_value=2)
    expiration_month = forms.IntegerField(min_value=0, max_value=2)
    cvv2 = forms.IntegerField(min_value=0, max_value=3)

"""""
END MODIFICATION
"""""
PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    # shipping_country = CountryField(blank_label='(select country)').formfield(
    #     required=False,
    #     widget=CountrySelectWidget(attrs={
    #         'class': 'custom-select d-block w-100',
    #     }))
    shipping_zip = forms.CharField(required=False)

    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    # billing_country = CountryField(blank_label='(select country)').formfield(
    #     required=False,
    #     widget=CountrySelectWidget(attrs={
    #         'class': 'custom-select d-block w-100',
    #     }))
    billing_zip = forms.CharField(required=False)

    same_billing_address = forms.BooleanField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'aria-label': 'Recipient\'s username',
        'aria-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()
