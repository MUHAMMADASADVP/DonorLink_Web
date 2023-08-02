from django.contrib import admin
from .models import User,Donor,Hospital,Bloodbank,Patient,Bankstock,History,Notification,Donationlist
# Register your models here.

admin.site.register(User)
admin.site.register(Donor)
admin.site.register(Hospital)
admin.site.register(Bloodbank)
admin.site.register(Patient)
admin.site.register(Bankstock)
admin.site.register(Notification)
admin.site.register(History)
admin.site.register(Donationlist)


