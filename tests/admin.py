from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Branch)
admin.site.register(models.Subject)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.UserAttempt)
admin.site.register(models.Solution)
