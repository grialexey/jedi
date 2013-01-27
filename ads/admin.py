# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Ad, Author


class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'price', 'category', 'added', )
    search_fields = ('title', )
    list_filter = ('added', 'category', )
    ordering = ('-added', )


admin.site.register(Ad, AdAdmin)
admin.site.register(Author)
