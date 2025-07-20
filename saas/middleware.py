# import threading
# from .models import Tenant

# _local = threading.local()

# def get_current_tenant():
#     return getattr(_local, "tenant", None)

# class TenantMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         domain = request.get_host().split(':')[0]
#         tenant = Tenant.objects.filter(domain=domain).first()
#         _local.tenant = tenant
#         request.tenant = tenant
#         return self.get_response(request)
