from django.contrib import admin

from concept.models import Art
from concept.models import Artist
from concept.models import CustomUser
from concept.models import Return
from concept.models import Price
from concept.models import Order

admin.site.register(Art)
admin.site.register(Artist)
admin.site.register(CustomUser)
admin.site.register(Return)
admin.site.register(Price)
admin.site.register(Order)
#管理者サイトに追加したい情報を記入
# Register your models here.
