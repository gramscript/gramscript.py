try:
    import ujson as json
except ImportError:
    import json

from ..object import JsonDeserializable, JsonSerializable
from ..chat_and_user import User


class LabeledPrice(JsonSerializable):
    def __init__(self, label, amount):
        self.label: str = label
        self.amount: int = amount

    def to_dict(self):
        return {
            'label': self.label, 'amount': self.amount
        }

    def to_json(self):
        return json.dumps(self.to_dict())


class Invoice(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None):
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, title, description, start_parameter, currency, total_amount, **kwargs):
        self.title: str = title
        self.description: str = description
        self.start_parameter: str = start_parameter
        self.currency: str = currency
        self.total_amount: int = total_amount


class ShippingAddress(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None):
            return None
        obj = cls.check_json(json_string, dict_copy=False)
        return cls(**obj)

    def __init__(self, country_code, state, city, street_line1, street_line2, post_code, **kwargs):
        self.country_code: str = country_code
        self.state: str = state
        self.city: str = city
        self.street_line1: str = street_line1
        self.street_line2: str = street_line2
        self.post_code: str = post_code


class OrderInfo(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None):
            return None
        obj = cls.check_json(json_string)
        obj['shipping_address'] = ShippingAddress.de_json(
            obj.get('shipping_address'))
        return cls(**obj)

    def __init__(self, name=None, phone_number=None, email=None, shipping_address=None, **kwargs):
        self.name: str = name
        self.phone_number: str = phone_number
        self.email: str = email
        self.shipping_address: ShippingAddress = shipping_address


class ShippingOption(JsonSerializable):
    def __init__(self, id, title):
        self.id: str = id
        self.title: str = title
        self.prices: List[LabeledPrice] = []

    def add_price(self, *args):
        """
        Add LabeledPrice to ShippingOption
        :param args: LabeledPrices
        """
        for price in args:
            self.prices.append(price)
        return self

    def to_json(self):
        price_list = [p.to_dict() for p in self.prices]
        return json.dumps({'id': self.id, 'title': self.title, 'prices': price_list})


class SuccessfulPayment(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None):
            return None
        obj = cls.check_json(json_string)
        obj['order_info'] = OrderInfo.de_json(obj.get('order_info'))
        return cls(**obj)

    def __init__(self, currency, total_amount, invoice_payload, shipping_option_id=None, order_info=None,
                 telegram_payment_charge_id=None, provider_payment_charge_id=None, **kwargs):
        self.currency: str = currency
        self.total_amount: int = total_amount
        self.invoice_payload: str = invoice_payload
        self.shipping_option_id: str = shipping_option_id
        self.order_info: OrderInfo = order_info
        self.telegram_payment_charge_id: str = telegram_payment_charge_id
        self.provider_payment_charge_id: str = provider_payment_charge_id


class ShippingQuery(JsonSerializable):
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None):
            return None
        obj = cls.check_json(json_string)
        obj['from_user'] = User.de_json(obj.pop('from'))
        obj['shipping_address'] = ShippingAddress.de_json(
            obj['shipping_address'])
        return cls(**obj)

    def __init__(self, id, from_user, invoice_payload, shipping_address, **kwargs):
        self.id: str = id
        self.from_user: User = from_user
        self.invoice_payload: str = invoice_payload
        self.shipping_address: ShippingAddress = shipping_address


class PreCheckoutQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string):
        if (json_string is None):
            return None
        obj = cls.check_json(json_string)
        obj['from_user'] = User.de_json(obj.pop('from'))
        obj['order_info'] = OrderInfo.de_json(obj.get('order_info'))
        return cls(**obj)

    def __init__(self, id, from_user, currency, total_amount, invoice_payload, shipping_option_id=None, order_info=None, **kwargs):
        self.id: str = id
        self.from_user: User = from_user
        self.currency: str = currency
        self.total_amount: int = total_amount
        self.invoice_payload: str = invoice_payload
        self.shipping_option_id: str = shipping_option_id
        self.order_info: OrderInfo = order_info
