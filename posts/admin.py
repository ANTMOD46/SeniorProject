from django.contrib import admin
from .models import SellItem, Donation, GeneralAnnouncement, Comment


# SellItem Admin
class SellItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'location', 'is_closed', 'created_at', 'updated_at')
    list_filter = ('is_closed', 'user')
    search_fields = ('title', 'description', 'location', 'phone')


# Donation Admin
class DonationAdmin(admin.ModelAdmin):
    list_display = ('title', 'role', 'user', 'location', 'is_closed', 'created_at')
    list_filter = ('is_closed', 'role', 'user')
    search_fields = ('title', 'description', 'location', 'phone')


# GeneralAnnouncement Admin
class GeneralAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'location', 'phone')
    list_filter = ('user', 'created_at')
    search_fields = ('title', 'content', 'location')


# Comment Admin
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at', 'content')
    search_fields = ('content',)
    list_filter = ('created_at', 'user')


# ลงทะเบียนโมเดลใน Django Admin
admin.site.register(SellItem, SellItemAdmin)
admin.site.register(Donation, DonationAdmin)
admin.site.register(GeneralAnnouncement, GeneralAnnouncementAdmin)
admin.site.register(Comment, CommentAdmin)
