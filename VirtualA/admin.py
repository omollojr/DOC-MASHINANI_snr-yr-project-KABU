from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Patient, User, ActivityLog, Services


class PatientInline(admin.TabularInline):
    model = Patient
    extra = 0

class UserAdmin(BaseUserAdmin):
    search_fields = ['email']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(id=request.user.id)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)
    
    
class PatientAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            action = "Edited"
        else:
            action = "Added"
        ActivityLog.objects.create(user=request.user, action=action, details=f"{obj} was {action} by {request.user}")
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        ActivityLog.objects.create(user=request.user, action="Deleted", details=f"{obj} was deleted by {request.user}")
        super().delete_model(request, obj)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Patient)
admin.site.register(ActivityLog)
admin.site.register(Services)
