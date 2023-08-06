from django.utils.translation import gettext as _


def detach_payment_detail(payment_detail):
    try:
        payment_detail.save_history()
        payment_detail.premium = None
        payment_detail.save()
        return []
    except Exception as exc:
        return [{
            'title': payment_detail.uuid,
            'list': [{
                'message': _("payment.mutation.failed_to_detach_payment_detail") % {'payment_detail': str(payment_detail)},
                'detail': payment_detail.uuid}]
        }]
