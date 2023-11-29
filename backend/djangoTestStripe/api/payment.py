from typing import Optional

import stripe
from forex_python.converter import CurrencyRates
from stripe.error import AuthenticationError

from .models import OrderedProduct


class PaymentStripe:

    def __init__(self, stripe_token: str, items: Optional[OrderedProduct]):
        self.token = stripe_token
        self.items = items
        self.converter = CurrencyRates()

    def create_payment(self) -> str:
        stripe.api_key = self.token

        line_items_data = []
        for item in self.items:
            line_items_data.append(
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item.product.name,
                        },
                        'unit_amount': round(self.convert_to_usd(price=round(item.product.price * 100), currency=item.product.currency)),
                    },
                    'quantity': item.quantity,
                },
            )

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items_data,
                mode='payment',
                success_url='https://example.com/success',
                cancel_url='https://example.com/cancel',
            )

            return session.id
        except AuthenticationError:
            raise Exception('Вы указали не рабочий токен stripe')

    def convert_to_usd(self, price, currency):
        if currency != 'usd':
            exchange_rate = self.converter.get_rate('RUB', 'USD')
            converted_amount = price * exchange_rate
            return converted_amount
        return price
