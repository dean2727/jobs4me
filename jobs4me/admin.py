from django.contrib import admin
from .models import *

admin.site.register(AppUser)
admin.site.register(Resume)
admin.site.register(Job)
admin.site.register(SuitableJob)