from django.contrib import admin
from .models import User,Pos_User,Station,Velo,Card,Transaction
# Register your models here.
admin.site.register(User)
admin.site.register(Pos_User)
admin.site.register(Station)
admin.site.register(Velo)
admin.site.register(Card)
admin.site.register(Transaction)

