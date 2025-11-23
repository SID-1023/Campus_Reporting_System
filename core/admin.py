from django.contrib import admin
from .models import Complaint, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Dynamically load all model fields
    list_display = [field.name for field in Profile._meta.get_fields() 
                    if not field.many_to_many and not field.one_to_many]

    search_fields = ('user__username', 'user__email')
    list_filter = ()
    ordering = ('id',)


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'created_at', 'status')
    list_filter = ('category', 'status')
    search_fields = ('title', 'description', 'location')
    ordering = ('-created_at',)
