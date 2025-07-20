from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    customer_id = forms.IntegerField(required=False, label="Customer ID")

    class Meta:
        model = Ticket
        fields = ['counter', 'template', 'quantity', 'payment_mode', 'customer_id']

    def clean(self):
        cleaned_data = super().clean()
        payment_mode = cleaned_data.get('payment_mode')
        customer_id = cleaned_data.get('customer_id')

        if payment_mode == 'credit' and not customer_id:
            raise forms.ValidationError("Credit payment requires a valid company client.")

        return cleaned_data
