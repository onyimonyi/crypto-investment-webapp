import decimal
from builtins import map, str
import os
from django.contrib.auth import get_user_model

User = get_user_model()
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserBalance, UserTransaction, Profile, UserBalance


@receiver(post_save, sender=User)
def create_initial_balance(sender, instance, created, **kwargs):
    if created:
        UserBalance.objects.create(
            user=instance,
            balance=0.00
        )


@receiver(post_save, sender=UserTransaction)
def save_transaction(sender, instance, created, *args, **kwargs):
    if created:
        balance = UserBalance.objects.get(user=instance.user).balance
        if instance.transaction_type == "Deposit":
            user_balance = UserBalance.objects.get(
                user=instance.user
            )
            user_balance.balance += float(instance.amount)
            user_balance.save()

        if instance.transaction_type == "Withdrawal" and balance >= instance.amount:
            user_balance = UserBalance.objects.get(
                user=instance.user,
            )
            user_balance.balance -= float(instance.amount)
            user_balance.save()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()
