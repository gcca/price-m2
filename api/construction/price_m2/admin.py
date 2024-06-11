from django.contrib import admin

from .models import Alcaldia, CatastroInfo, UsoConstruccion


@admin.register(Alcaldia)
class AlcaldiaAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Alcaldia._meta.fields]


@admin.register(UsoConstruccion)
class UsoConstruccionAdmin(admin.ModelAdmin):
    list_display = [f.name for f in UsoConstruccion._meta.fields]


@admin.register(CatastroInfo)
class CatastroInfoAdmin(admin.ModelAdmin):
    list_display = [f.name for f in CatastroInfo._meta.fields]
