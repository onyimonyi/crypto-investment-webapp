from builtins import ValueError
from PIL import Image
from datetime import datetime, timedelta
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils import timezone
from math import *

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager,
)


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not full_name:
            raise ValueError("Users must have surname and other names")
        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self, full_name, email, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,

            is_staff=True
        )
        return user

    def create_superuser(self, full_name, email, password=None):
        user = self.create_user(
            email,
            full_name,
            password=password,

            is_staff=True,
            is_admin=True
        )
        return user


class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin


class UserTransaction(models.Model):
    class Meta:
        verbose_name = 'User Transactions'
        verbose_name_plural = 'User Transactuons'

    TRANSACTION_TYPE_CHOICES = (
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),

    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=200, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.FloatField(default=0.0)

    def __str__(self):
        return self.transaction_type


def len(balance):
    pass


def balance(args):
    pass


class UserBalance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='user_balance')
    balance = models.FloatField(default='0:00')

    class Meta:
        verbose_name_plural = 'UserBalance'

    def save(self, *args, **kwargs):
        self.balance = round(self.balance, 2)
        super(UserBalance, self).save(*args, **kwargs)


class Wallet(models.Model):
    address = models.CharField(max_length=255, default=None)

    def __str__(self):
        return f"{self.address}"


class Assets(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=1000000, decimal_places=2, null=True, blank=True, )
    description = models.TextField(null=True, blank=True)
    percentage = models.FloatField(default=None)
    picture = models.ImageField(upload_to='picture', max_length=255, null=True, blank=True)
    added_on = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("btc:assets-detail", kwargs={"id": self.id})

    def get_invest_url(self):
        return reverse("btc:assets-detail", kwargs={"id": self.id})


class Deposit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    amount = models.CharField(max_length=12, default=None)

    def __str__(self):
        return f"{self.user}"


class Withdrawal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    amount = models.CharField(max_length=12, default=None)
    address = models.CharField(max_length=12, default=None)
    withdrawal_date = models.DateTimeField(auto_now_add=True)
    withdrawal_requested = models.BooleanField(default=False)
    withdrawal_granted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}"

    def get_withdrawal_status(self):
        if self.withdrawal_requested:
            return f" {self.amount} pending withdrawal "
        elif self.withdrawal_granted:
            return f" {self.amount} withdrawal approved"
        else:
            return "no withdrawal approved"


class Investment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    duration = models.CharField(max_length=12, default=None)
    start_date = models.DateTimeField(auto_now_add=True)
    exp_date = models.DateTimeField()
    assets = models.CharField(max_length=12, default=None)
    amount = models.FloatField(null=True, blank=True, default=None)
    done = models.BooleanField(default=False)
    added_on = models.FloatField(null=True, blank=True, default=None)
    interest = models.FloatField(default=False)

    def __str__(self):
        return f"Hello {self.user} your investment started on  {self.start_date}"

    def invest_amount(self):
        return self.amount

    def get_profit(self):
        duration = self.duration
        added_on = self.added_on
        # check the investment has expired
        current_date = timezone.now()
        interest_rate = self.interest
        period = 86400
        profit = 0
        if current_date > self.exp_date:  # expired
            user_balance_obj = UserBalance.objects.filter(id=self.user.id).first()
            if user_balance_obj:
                if float(duration) > interest_rate and float(duration) / 2 == 1:
                    if added_on:
                        main = interest_rate * float(duration)
                        mark = added_on * float(duration)
                        profits = (main + mark) * self.amount
                        profit = round(profits, 2)
                        user_balance_obj.balance += profit
                        user_balance_obj.save()
                        self.done = True
                        self.save()
                    else:
                        main = interest_rate * float(duration)
                        profits = (main + float(duration)) * self.amount
                        profit = round(profits, 2)
                        user_balance_obj.balance += profit
                        user_balance_obj.save()
                        self.done = True
                        self.save()
                elif float(duration) > 2:
                    if added_on:
                        mark = added_on * float(duration)
                        main = interest_rate * float(duration)
                        profits = (main + mark) * self.amount
                        profit = round(profits, 2)
                        user_balance_obj.balance += profit
                        user_balance_obj.save()
                        self.done = True
                        self.save()
                    else:
                        main = interest_rate * float(duration)
                        profits = (main + float(duration)) * self.amount
                        profit = round(profits, 2)
                        user_balance_obj.balance += profit
                        user_balance_obj.save()
                        self.done = True
                        self.save()
                else:
                    profits = interest_rate * self.amount
                    profit = round(profits, 2)
                    user_balance_obj.balance += profit
                    user_balance_obj.save()
                    self.done = True
                    self.save()
        else:  # not expired /
            td = current_date - self.start_date
            profits = (interest_rate * int(self.amount) * td.total_seconds()) / period
            profit = round(profits, 2)
        return profit


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.user}"


class Address(models.Model):
    address = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.address}"

    def get_address(self):
        address = Address.objects.filter(address=self.address[-1])
        return address

