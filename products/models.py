from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class Payment(models.Model):
    amount = models.IntegerField()  # in pence
    timestamp = models.DateTimeField(auto_now_add=True)

    def process_payment(self, token):
        try:
            charge = stripe.Charge.create(
                amount=self.amount,
                currency='GBP',
                source=token,
                description='Payment for service',
            )
            return True
        except stripe.error.CardError as e:
            # Handle card error
            return False
        except stripe.error.InvalidRequestError as e:
            # Handle invalid request error
            return False
        except stripe.error.AuthenticationError as e:
            # Handle authentication error
            return False
        except stripe.error.APIConnectionError as e:
            # Handle API connection error
            return False
        except stripe.error.StripeError as e:
            # Handle generic Stripe error
            return False
