from django.contrib import admin
from django.utils.text import capfirst

def remove_app_labels():
    original_get_app_list = admin.site.get_app_list

    def custom_get_app_list(request):
        app_list = original_get_app_list(request)
        flat_models = []
        for app in app_list:
            for model in app["models"]:
                flat_models.append(model)
        return [{
            "name": "Core",
            "app_label": "all",
            "models": flat_models,
        }]

    admin.site.get_app_list = custom_get_app_list

remove_app_labels()
