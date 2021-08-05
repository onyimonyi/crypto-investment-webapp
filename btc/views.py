import datetime
import urllib.request
from builtins import super
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.http import is_safe_url
from django.views.generic import CreateView, FormView
from django.views.generic import ListView
import requests
import json

from .forms import (RegisterForm, LoginForm, AssetForm, CheckoutForm, UserUpdateForm, ProfileUpDateForm, withdrawalForm,
                    DepositForm)
from .models import Assets, UserBalance, Investment, UserTransaction, Withdrawal, Address


# Create your views here.


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/investment/login/'


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form, *args, **kwargs):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['quest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                messages.info(self.request, 'welcome, please invest wisely to maximize profit')
                return redirect('btc:invest-view')
        return super(LoginView, self).form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('home')
    # Redirect to a success page.


@login_required
def asset_create_view(request):
    form = AssetForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = AssetForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/asset_create.html', context)


class product_list_view(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
        url = "https://api.nomics.com/v1/currencies/ticker?key=7c2a3c5d3e3e1fae839e9bd115e45e2f97936300&ids=BTC,ETH,XRP&interval=1d,30d&convert=EUR&per-page=100&page=1"
        response = urllib.request.urlopen(url).read()
        print(response)
        name = response[0].name
        price = response[0].price
        print(price)
        item = Assets.objects.all()
        paginator = Paginator(item, 4)  # Show 4 contacts per page.
        page_number = self.request.GET.get('page')
        item = paginator.get_page(page_number)
        if item.name == name:
            item.price = price
            item.update()
        context = {
            'item': item,
            'page_obj': item
        }
        return render(self.request, 'accounts/assets_list.html', context)


@login_required
def ItemDetailView(request, id):
    obj = get_object_or_404(Assets, id=id)
    form = CheckoutForm()
    context = {
        'obj': obj,
        'form': form
    }
    return render(request, "accounts/assets_detail.html", context)


def investment(request, id):
    obj = get_object_or_404(Assets, id=id)
    asset = obj.name
    form = CheckoutForm(request.POST or None)
    balance_qs = UserBalance.objects.get(user=request.user)
    balance = balance_qs
    if form.is_valid():
        amount = form.cleaned_data.get('amount')
        investment_durations = form.cleaned_data.get('investment_durations')
        start_date = timezone.now()
        if float(amount) <= balance.balance:
            if float(amount) <= 0:
                messages.info(request, 'please, put real values here')
                return redirect("btc:invested", id=id)
            if float(amount) <= balance.balance:
                if float(investment_durations) <= 0:
                    messages.info(request, 'please, put real values here')
                    return redirect("btc:invested", id=id)
            balance.balance -= float(amount)
            balance.save()
            if investment_durations:
                exp_time = start_date + datetime.timedelta(days=float(investment_durations))
                investment = Investment.objects.create(user=request.user, assets=asset, start_date=start_date,
                                                       exp_date=exp_time,
                                                       duration=investment_durations, amount=amount,
                                                       interest=obj.percentage, added_on=obj.added_on)
                investment.save()
                messages.info(request, F" your {investment_durations} day investment plan is initiated successfully")
                return redirect("btc:invest-view")
            else:
                messages.info(request, 'invalid investment parameter')
                return redirect("btc:invest-view")
        else:
            messages.info(request, 'you balance must be greater than you investment amount')
            return redirect("btc:invested", id=id)
    context = {
        'form': form,
        'obj': obj,
    }
    return render(request, "accounts/assets_detail.html", context)


def invest_view(request):
    user_bal = UserBalance.objects.get(user=request.user)
    investments = Investment.objects.filter(user=request.user, done=False)  # get returns only oneitem
    withdrawal = Withdrawal.objects.filter(user=request.user, withdrawal_requested=True)  # get returns only oneitem
    # but filter returns a list
    context = {
        'user_bal': user_bal,
        'withdrawal': withdrawal,
        'investments': investments
    }
    return render(request, "accounts/investments.html", context)


def admin_view(request):
    obj = UserTransaction.objects.all()
    object = Assets.objects.all()
    context = {
        'obj': obj,
        'object': object
    }
    return render(request, "accounts/admin.html", context)


def home_view(request, *args, **kwargs):
    return render(request, "home.html")


def profile_view(request):
    user_balance = UserBalance.objects.get(user=request.user)
    context = {
        'user_balance': user_balance
    }
    return render(request, 'accounts/profile.html', context)


def deposit_view(request):
    form = DepositForm(request.POST or None)
    print(form)
    if form.is_valid():
        amount = form.cleaned_data.get('amount')
        if amount <= 0:
            messages.warning(request, 'Please, enter a valid amount!')
            return redirect('btc:deposit_view')
        return redirect('btc:wallet')
    form = DepositForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/deposit.html', context)


def wallet_view(request):
    ob = Address.objects.all()
    obj = ob.first()
    context = {
        'obj': obj,
    }
    return render(request, 'accounts/detail.html', context)


def withdrawal_view(request):
    form = withdrawalForm(request.POST or None)
    user = UserBalance.objects.get(user=request.user)
    if form.is_valid():
        amount = form.cleaned_data.get('amount')
        amount = Decimal(amount.strip())
        address = form.cleaned_data.get('address')
        if user.balance >= float(amount):
            withdrawal = Withdrawal()
            withdrawal.user = request.user
            withdrawal.amount = amount
            withdrawal.address = address
            withdrawal.withdrawal_requested = True
            withdrawal.save()
            user.balance -= float(amount)
            user.save()
            messages.success(request, 'successful withdrawal')
            return redirect('btc:invest-view')
        messages.info(request, 'insufficient fund')
        return redirect('btc:withdrawal')
    else:
        form = withdrawalForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/withdrawal.html', context)


def profile_update_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpDateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid:
            u_form.save()
            p_form.save()
            print(u_form)
            messages.info(request, 'your profile is successfully updated')

            return redirect('btc:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpDateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'accounts/profile-update.html', context)


def transaction_delete_view(request, id):
    obj = get_object_or_404(UserTransaction, id=id)
    if request.method == 'POST':
        obj.delete()
        return redirect('btc:invest-admin-view')
    context = {
        'object': obj
    }
    return render(request, "accounts/transact-delete.html", context)


def assets_delete_view(request, id):
    obj = get_object_or_404(Assets, id=id)
    if request.method == 'POST':
        obj.delete()
        return redirect('btc:invest-admin-view')
    context = {
        'object': obj
    }
    return render(request, "accounts/delete.html", context)
