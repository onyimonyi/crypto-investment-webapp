from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    logout_view,
    asset_create_view,
    ItemDetailView,
    product_list_view,
    investment,
    invest_view,
    profile_update_view,
    profile_view,
    assets_delete_view,
    transaction_delete_view,
    withdrawal_view,
deposit_view,
wallet_view
)

app_name = 'btc'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('create/', asset_create_view, name='create-assets'),
    path('<int:id>/', ItemDetailView, name='assets-detail'),
    path('assets-list', product_list_view.as_view(), name='assets-list'),
    path('investment/<int:id>/', investment, name='invested'),
    path('invest-view', invest_view, name='invest-view'),
    path('profile-update/', profile_update_view, name='profile-update'),
    path('profile/', profile_view, name='profile'),
    path('delete/<int:id>/', assets_delete_view, name='delete-item'),
    path('delete/<int:id>/', transaction_delete_view, name='transact-delete'),
    path('withdrawal/', withdrawal_view, name='withdrawal'),
    path('deposit/', deposit_view, name='deposit_view'),
    path('wallet/', wallet_view, name='wallet'),

]
