from django.contrib import admin
from .models import UserProfile, Dependent, TaxDocument, TaxReturn

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'filing_status', 'phone_number')
    search_fields = ('user__username', 'user__email', 'phone_number')

@admin.register(Dependent)
class DependentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'relationship', 'date_of_birth')
    search_fields = ('first_name', 'last_name', 'ssn')

@admin.register(TaxDocument)
class TaxDocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'tax_year', 'status', 'uploaded_at')
    list_filter = ('document_type', 'status', 'tax_year')
    search_fields = ('user__username', 'document_type')

@admin.register(TaxReturn)
class TaxReturnAdmin(admin.ModelAdmin):
    list_display = ('user', 'tax_year', 'status', 'total_income', 'total_tax', 'refund_amount')
    list_filter = ('status', 'tax_year')
    search_fields = ('user__username',)
    readonly_fields = ('created_at', 'updated_at', 'filed_date') 