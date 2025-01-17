from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Выберите категорию", required=False)
