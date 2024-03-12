from rest_framework.serializers import ValidationError
from rest_framework import status
import razorpay
from django.conf import settings

class RazorpayClient:
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    def create_order(self, amount, currency):
        data = {
            "amount": amount * 100,
            "currency": currency,
        }
        try:
            self.order = self.client.order.create(data=data)
            return self.order
        except Exception as e:
            raise ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": e
                }
            )
    
    def verify_payment_signature(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        try:
            
            self.verify_signature = self.client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            return self.verify_signature
        except Exception as e:
            raise ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": e
                }
            )
            