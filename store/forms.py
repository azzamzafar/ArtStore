from django import forms
from store.models import Item

# class OrdersForm(forms.ModelForm):
#     model = Order
#     fields = ['customer','product','price','Qty']
#     Qty = forms.IntegerField(max_value=2)
    
class ItemsForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['product','price','Qty']
    choices = [(f'{i}',i) for i in range(1,6)]
    Qty = forms.IntegerField(widget=forms.Select(choices=choices))

# OrdersFormSet = forms.formset_factory(OrdersForm)
# ItemsFormSet = forms.modelformset_factory(Item,form=ItemsForm,exclude=['price'])