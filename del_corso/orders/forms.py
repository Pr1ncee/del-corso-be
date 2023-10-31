from django.contrib.admin.helpers import ActionForm
from django import forms

from orders.enums.status_enum import OrderStatus


class OrderStatusForm(ActionForm):
    class Meta:
        fields = ('status', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'] = forms.ChoiceField(choices=OrderStatus.choices, required=False)
