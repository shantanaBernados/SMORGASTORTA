from django.contrib import admin
from sweden.models import HWQuestion, SleepQuestion, Assessment, User_HWQ_Assessment

# Register your models here.
admin.site.register(HWQuestion)
admin.site.register(SleepQuestion)
admin.site.register(Assessment)
admin.site.register(User_HWQ_Assessment)