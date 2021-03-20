from django.contrib import admin
# Register your models here.
from .models import Artist, Item, Payment, ShippingAddress, UserProfile, CartHeader, CartBody, Region, Category, Community


from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)

def make_refund_accepted(modeladmin, request, queryset):
    queryset.update(refund_requested=False, refund_granted=True)


make_refund_accepted.short_description = 'Update orders to refund granted'


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'shipping_zip',
        'phone_number',
        'instructions',
        'country',
        'is_delivered'
    ]
    list_filter = ['is_delivered', 'country']
    search_fields = ['user', 'street_address','shipping_zip']

class ItemInline(admin.TabularInline):
    model = Item
    extra = 1

class ArtistInline(admin.TabularInline):
    model = Artist
    extra = 1

class CommunityAdmin(admin.ModelAdmin):
    inlines = [ArtistInline,]

class RegionAdmin(admin.ModelAdmin):
    inlines = [ArtistInline,]

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ItemInline,]

admin.site.register(Region,RegionAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Community,CommunityAdmin)
admin.site.register(Artist)
admin.site.register(Item)
admin.site.register(CartHeader)
admin.site.register(CartBody)
admin.site.register(Payment)
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(UserProfile)
