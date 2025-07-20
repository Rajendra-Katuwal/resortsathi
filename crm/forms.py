# from django import forms
# from .models import Customer, CustomerType

# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = [
#             'name', 'email', 'phone', 'address',
#             'country', 'notes', 'customer_type'
#         ]


# class CustomerTypeForm(forms.ModelForm):
#     class Meta:
#         model = CustomerType
#         fields = ['name']


from django import forms
from .models import CorporateCustomer, OrdinaryCustomer, OrganizationCustomer

class CorporateCustomerForm(forms.ModelForm):
    class Meta:
        model = CorporateCustomer
        fields = '__all__'

class OrdinaryCustomerForm(forms.ModelForm):
    class Meta:
        model = OrdinaryCustomer
        fields = '__all__'

class OrganizationCustomerForm(forms.ModelForm):
    class Meta:
        model = OrganizationCustomer
        fields = '__all__'
