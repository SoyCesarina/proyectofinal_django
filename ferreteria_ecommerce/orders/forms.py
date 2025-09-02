from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name',
            'customer_email',
            'customer_phone',
            'shipping_address',
            'shipping_city',
            'shipping_state',
            'shipping_zip_code',
            'notes'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono'
            }),
            'shipping_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa'
            }),
            'shipping_city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ciudad'
            }),
            'shipping_state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Estado/Provincia'
            }),
            'shipping_zip_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código postal'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales (opcional)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos requeridos
        for field_name in self.fields:
            if field_name != 'notes':
                self.fields[field_name].required = True
