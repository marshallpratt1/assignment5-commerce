from django.contrib import admin
from .models import *

# Register your models here.
#####################
#user:   marshall
#p-word: 1
#####################
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)