# from django.db import models
# from django.conf import settings


# class CustomerType(models.Model):
#     name = models.CharField(max_length=255, unique=True)

#     def __str__(self):
#         return self.name


# class Customer(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20, blank=True)
#     address = models.TextField(blank=True)
#     country = models.CharField(max_length=100, blank=True)
#     notes = models.TextField(blank=True)
#     customer_type = models.ForeignKey(CustomerType, on_delete=models.SET_NULL, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name



from django.db import models

class BaseCustomer(models.Model):
    CUSTOMER_TYPES = [
        ('corporate', 'Corporate'),
        ('ordinary', 'Ordinary'),
        ('organization', 'Organization'),
    ]
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class CorporateCustomer(BaseCustomer):
    company_name = models.CharField(max_length=255)
    company_address = models.TextField()
    registration_number = models.CharField(max_length=100)
    pan_or_vat_number = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=20)

    spokesperson_name = models.CharField(max_length=255)
    spokesperson_email = models.EmailField()
    spokesperson_phone = models.CharField(max_length=20)
    spokesperson_id_image = models.ImageField(upload_to='corporate_ids/', null=True, blank=True)


class OrdinaryCustomer(BaseCustomer):
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    dob = models.DateField()
    email = models.EmailField()
    nationality = models.CharField(max_length=100)
    id_image = models.ImageField(upload_to='ordinary_ids/', null=True, blank=True)

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    town = models.CharField(max_length=100)


class OrganizationCustomer(BaseCustomer):
    ORGANIZATION_TYPES = [
        ('ngo', 'Non-Governmental Organization'),
        ('npo', 'Non-Profit Organization'),
        ('charity', 'Charity'),
        ('social_enterprise', 'Social Enterprise'),
    ]

    organization_name = models.CharField(max_length=255)
    organization_type = models.CharField(max_length=50, choices=ORGANIZATION_TYPES, default='npo')
    
    organization_address = models.TextField()
    registration_number = models.CharField(max_length=100, help_text="Issued by Social Welfare Council or other body")
    pan_or_tax_exemption_number = models.CharField(max_length=100, blank=True, null=True)
    
    official_email = models.EmailField()
    official_contact_number = models.CharField(max_length=20)

    representative_name = models.CharField(max_length=255)
    representative_email = models.EmailField()
    representative_phone = models.CharField(max_length=20)
    
    representative_id_image = models.ImageField(upload_to='organization_ids/', blank=True, null=True)

    def __str__(self):
        return self.organization_name

