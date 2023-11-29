"""
URL configuration for djangoTestStripe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from .views import (GetItemView, GetItemsView, GetOrderedItemsView,
                    UserLoginView, AddOrderView, UserRegisterView, DeleteOrderView, BuyItemsView)

urlpatterns = [
    path('item/<int:item_id>', GetItemView.as_view(), name='get_item'),
    path('items', GetItemsView.as_view(), name='get_items'),
    path('ordered-items', GetOrderedItemsView.as_view(), name='get_ordered_items'),
    path('login', UserLoginView.as_view(), name='user_login'),
    path('register', UserRegisterView.as_view(), name='user_register'),
    path('add-to-order', AddOrderView.as_view(), name='add_to_order'),
    path('delete-ordered-product/<int:product_id>', DeleteOrderView.as_view(), name='delete_ordered_product'),
    path('buy-all-items', BuyItemsView.as_view(), name='buy_all_items'),
]
