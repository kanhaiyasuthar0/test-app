from django import forms
from .models import Product,Contact,Coupon


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'price', 'description','discount_percent','types',
            'image', 'image1', 'image2', 'image3', 'image4', 'image5', 'zipfile'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter product title'
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Enter product price'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter product description',
                'rows': 4
            }),
            'discount_percent': forms.NumberInput(attrs={
                'placeholder': 'Enter discount value'
            }),
            'image': forms.FileInput(),
            'image1': forms.FileInput(),
            'image2': forms.FileInput(),
            'image3': forms.FileInput(),
            'image4': forms.FileInput(),
            'image5': forms.FileInput(),
            'zipfile': forms.FileInput(),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message',]


class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount', 'is_active']
