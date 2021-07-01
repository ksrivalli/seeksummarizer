from django.contrib import admin
from .models import ContactForm, save_sum, all_sum, Comment
# Register your models here.

admin.site.register(save_sum)
admin.site.register(all_sum)
admin.site.register(Comment)
admin.site.register(ContactForm)