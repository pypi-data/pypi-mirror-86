from django.contrib import admin

from budget.models import Budget, LineItem, Transaction


class BudgetAdmin(admin.ModelAdmin):
    pass


class LineItemAdmin(admin.ModelAdmin):
    pass


class TransactionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Budget, BudgetAdmin)
admin.site.register(LineItem, LineItemAdmin)
admin.site.register(Transaction, TransactionAdmin)
