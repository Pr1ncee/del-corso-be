from django import forms

from store.models import Product, Size


class BulkUpdateProductSizeForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.order_by("-created_at"),
        empty_label="Выберите товар",
    )
    sizes = forms.ModelMultipleChoiceField(queryset=Size.objects.all(), widget=forms.CheckboxSelectMultiple)
