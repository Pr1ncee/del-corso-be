import logging

from django import forms

from del_corso import setup_logging
from store.models import Product, Size, Color

setup_logging()
logger = logging.getLogger(__name__)


class BulkUpdateProductSizeForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.order_by("-created_at"),
        empty_label="Выберите товар",
    )
    sizes = forms.ModelMultipleChoiceField(queryset=Size.objects.all(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(BulkUpdateProductSizeForm, self).__init__(*args, **kwargs)

        for size in Size.objects.all():
            self.fields[f'quantity_{size.size}'] = forms.IntegerField(
                min_value=0,
                required=False
            )

    def clean(self):
        cleaned_data = super(BulkUpdateProductSizeForm, self).clean()
        size_quantities = {}

        logger.info("Creating new products with sizes... Mapping received sizes and quantities...")
        for key, quantity in cleaned_data.items():
            if key.startswith('quantity_') and quantity is not None:
                size_number = int(key.split('_')[1])
                if cleaned_data["sizes"].filter(size=size_number):
                    size_quantities[size_number] = quantity

        logger.info(f"Mapped successfully! Result is: {size_quantities}")
        if not size_quantities:
            logger.info("Error: couldn't map sizes and quantities")
            raise forms.ValidationError("Пожалуйста, укажите количество выбранных размеров.")

        cleaned_data['size_quantities'] = size_quantities
        return cleaned_data


class BulkUpdateProductColorForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.order_by("-created_at"),
        empty_label="Выберите товар",
    )
    colors = forms.ModelMultipleChoiceField(queryset=Color.objects.all(), widget=forms.CheckboxSelectMultiple)
