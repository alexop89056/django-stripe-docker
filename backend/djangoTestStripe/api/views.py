from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from .models import Item, OrderedProduct, Order

from django.conf import settings
from .payment import PaymentStripe


@method_decorator(login_required, name='dispatch')
class GetItemView(View):
    def get(self, request, item_id):
        item = Item.objects.filter(id=item_id).first()
        if not item:
            return render(request, 'item.html')

        context = {'item': item}
        return render(request, 'item.html', context=context)


@method_decorator(login_required, name='dispatch')
class GetItemsView(View):
    def get(self, request):
        items = Item.objects.all()
        context = {'items': items}
        return render(request, 'items.html', context=context)


@method_decorator(login_required, name='dispatch')
class GetOrderedItemsView(View):
    def get(self, request):
        order = Order.objects.filter(user=request.user).first()
        if not order:
            return HttpResponse('У вас нету заказанных товаров')

        ordered_items = OrderedProduct.objects.filter(order=order, user=request.user).all()
        context = {
            'ordered_items': ordered_items,
            'order': order
        }
        return render(request, 'ordered_items.html', context=context)


class UserLoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('get_items')
            else:
                return HttpResponse('Пользователь не найден')

        else:
            return HttpResponse("Введите валидные данные")


class UserRegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            exists_user = User.objects.filter(username=username).first()
            if exists_user:
                return HttpResponse('Юзер с таким юзернеймом уже есть в базе')
            new_user = User.objects.create_user(username=username, password=password)
            new_user.save()

            return redirect('user_login')

        else:
            return HttpResponse('Введите валидные данные')


@method_decorator(login_required, name='dispatch')
class AddOrderView(View):
    def post(self, request):
        item_id = request.POST.get('item_id')
        item = Item.objects.filter(id=item_id).first()
        if not item:
            return HttpResponse('Product not found')

        quantity = request.POST.get('quantity')

        exists_order = Order.objects.filter(user=request.user).first()
        if exists_order:
            order = exists_order
        else:
            order = Order(user=request.user)
            order.save()

        exist_order_product = OrderedProduct.objects.filter(product=item, user=request.user).first()
        if exist_order_product:
            return HttpResponse('Этот товар вы уже заказали')
        new_ordered_product = OrderedProduct(user=request.user, product=item, order=order, quantity=quantity)
        new_ordered_product.save()

        return redirect('get_items')


@method_decorator(login_required, name='dispatch')
class DeleteOrderView(View):
    def get(self, request, product_id):
        exist_ordered_product = OrderedProduct.objects.filter(id=product_id, user=request.user).first()
        if not exist_ordered_product:
            return HttpResponse('Product not found')

        exist_ordered_product.delete()
        return redirect('get_ordered_items')

@method_decorator(login_required, name='dispatch')
class BuyItemsView(View):
    http_method_names = ['post']

    def post(self, request):
        user_order = Order.objects.filter(user=request.user).first()
        if not user_order:
            return HttpResponse('У вас нету ничего в заказаных')

        all_ordered_products = OrderedProduct.objects.filter(user=request.user, order=user_order).all()

        payment = PaymentStripe(stripe_token=settings.STRIPE_TOKEN, items=all_ordered_products)
        session_id = payment.create_payment()

        if session_id:
            context = {'session_id': session_id,
                       'public_key': settings.PUBLIC_STRIPE_TOKEN}
            return render(request, 'payment_apply.html', context=context)

        return HttpResponse('200')
