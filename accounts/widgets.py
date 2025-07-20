from django import forms

# yourapp/widgets.py
class NepaliDatePickerWidget(forms.DateInput):
    class Media:
        css = {
            'all': [
                'https://cdn.jsdelivr.net/npm/nepali-datepicker@4.0.0/css/nepali.datepicker.min.css',
            ]
        }
        js = [
            'https://code.jquery.com/jquery-3.6.0.min.js',
            'https://cdn.jsdelivr.net/npm/nepali-datepicker@4.0.0/js/nepali.datepicker.min.js',
            'js/datepicker-init.js',
        ]

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'nepali-datepicker', 'autocomplete': 'off'}
        if attrs:
            final_attrs.update(attrs)
        super().__init__(attrs=final_attrs, format=format or '%Y-%m-%d')
