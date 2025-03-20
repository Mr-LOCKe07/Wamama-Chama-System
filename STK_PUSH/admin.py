from django.contrib import admin
from .models import Meetings, RegisterChama, SignUp, Article

# Register your models here.
admin.site.register (Meetings)


@admin.register(RegisterChama)
class RegisterChamaAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'name_of_chama', 'phone_number', 'email', 'id_number', 'county', 'password')
    search_fields = ['first_name', 'last_name', 'name_of_chama', 'phone_number', 'email', 'id_number','county']


@admin.register(SignUp)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'email','password')
    search_fields = ['first_name', 'last_name', 'password']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'headline', 'link')
    search_fields = ['title', 'headline']