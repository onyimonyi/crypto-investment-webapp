# Register your models here.
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import RegisterForm, UserAdminChangeForm
from .models import UserTransaction, UserBalance, Investment, Assets, Profile, Withdrawal, Deposit, Address

User = get_user_model()


class InvestmentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'duration',
        'assets',
        'start_date',
        'amount',
        'exp_date',
        'done',
        'added_on',
        'interest'

    ]


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'amount',
        'transaction_type',
        'date',
    ]
    list_display_links = [
        'user',
        'transaction_type',
    ]

    list_filter = [
        'transaction_type',
    ]

    search_fields = [
        'user__email',
        'transaction_type'
    ]


class DepositAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'amount',
    ]


def make_withdrawal_approved(modeladmin, request, queryset):
    queryset.update(withdrawal_requested=False, withdrawal_granted=True)


make_withdrawal_approved.short_description = 'Update pending withdrawals to approved'


class WithdrawalAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'amount',
        'address',
        'withdrawal_date',
        'withdrawal_requested',
        'withdrawal_granted'
    ]
    list_display_links = [
        'user',
        'amount',
    ]

    list_filter = [
        'user',
        'amount',
        'withdrawal_requested',
    ]

    search_fields = [
        'user__email',
        'amount',
        'withdrawal_requested',
        'withdrawal_granted'
    ]

    actions = [make_withdrawal_approved]


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'address',

    ]


class BalanceAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'balance',

    ]

    list_filter = [
        'user',

    ]

    search_fields = [
        'user__email',

    ]


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm  # update view
    add_form = RegisterForm  # create view
    list_display = ('email', 'full_name', 'admin', 'active', 'staff',)
    list_filter = ('admin', 'active', 'staff')
    fieldsets = (
        (None, {'fields': ('full_name', 'email', 'password')}),
        # ('FULL NAME', {'fields': ('full_name',)}),
        ('permissions', {'fields': ('admin', 'active', 'staff')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(UserTransaction, TransactionAdmin)
admin.site.unregister(Group)
# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(UserBalance, BalanceAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(Assets)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(Withdrawal, WithdrawalAdmin)
