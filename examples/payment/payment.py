import sys
import time
from pprint import pprint
import gramscript
from gramscript.loop import MessageLoop
from gramscript.namedtuple import LabeledPrice, ShippingOption
from gramscript.delegate import (
    per_invoice_payload, pave_event_space, create_open,
    per_message, call)

"""
Run it by:
$ python3.5 script.py <bot-token> <payment-provider-token>
"""


class OrderProcessor(gramscript.helper.InvoiceHandler):
    def __init__(self, *args, **kwargs):
        super(OrderProcessor, self).__init__(*args, **kwargs)

    def on_shipping_query(self, msg):
        query_id = self._extracted_from_on_pre_checkout_query_2(
            msg, 'shipping_query', 'Shipping query:')

        bot.answerShippingQuery(
            query_id, True,
            shipping_options=[
                ShippingOption(id='fedex', title='FedEx', prices=[
                    LabeledPrice(label='Local', amount=345),
                    LabeledPrice(label='International', amount=2345)]),
                ShippingOption(id='dhl', title='DHL', prices=[
                    LabeledPrice(label='Local', amount=342),
                    LabeledPrice(label='International', amount=1234)])])

    def on_pre_checkout_query(self, msg):
        query_id = self._extracted_from_on_pre_checkout_query_2(
            msg, 'pre_checkout_query', 'Pre-Checkout query:')

        bot.answerPreCheckoutQuery(query_id, True)

    # TODO Rename this here and in `on_shipping_query` and `on_pre_checkout_query`
    def _extracted_from_on_pre_checkout_query_2(self, msg, flavor, arg2):
        result, from_id, invoice_payload = gramscript.glance(
            msg, flavor=flavor)
        print(arg2)
        pprint(msg)
        return result

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = gramscript.glance(msg)

        if content_type == 'successful_payment':
            print('Successful payment RECEIVED!!!')
        else:
            print('Chat message:')

        pprint(msg)


def send_invoice(seed_tuple):
    msg = seed_tuple[1]

    content_type, chat_type, chat_id = gramscript.glance(msg)

    if content_type == 'text':
        sent = bot.sendInvoice(
            chat_id, "Nick's Hand Cream", "Keep a man's hand like a woman's",
            payload='a-string-identifying-related-payment-messages-tuvwxyz',
            provider_token=PAYMENT_PROVIDER_TOKEN,
            start_parameter='abc',
            currency='HKD', prices=[
                LabeledPrice(label='One Case', amount=987),
                LabeledPrice(label='Package', amount=12)],
            need_shipping_address=True, is_flexible=True)  # required for shipping query

        print('Invoice sent:')
        pprint(sent)


TOKEN = sys.argv[1]
PAYMENT_PROVIDER_TOKEN = sys.argv[2]

bot = gramscript.DelegatorBot(TOKEN, [
    (per_message(flavors=['chat']), call(send_invoice)),
    pave_event_space()(
        per_invoice_payload(), create_open, OrderProcessor, timeout=30,
    )
])

MessageLoop(bot).run_as_thread()

while 1:
    time.sleep(10)
