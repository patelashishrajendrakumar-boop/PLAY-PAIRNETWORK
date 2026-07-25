from django.contrib import admin
from app_modules.adminapp import models

# Register your models here.
admin.site.register(models.sport)
admin.site.register(models.team)
admin.site.register(models.player)
admin.site.register(models.tournament)
admin.site.register(models.match)
admin.site.register(models.playerperformance)
admin.site.register(models.announcement)