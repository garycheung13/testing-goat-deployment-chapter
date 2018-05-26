from django import forms

from lists.models import Item

## using a widget
# class ItemForm(forms.Form):
#     item_text = forms.CharField(
#         widget=forms.fields.TextInput(attrs={
#             'placeholder': 'Enter a to-do item',
#             'class': 'form-control input-lg'
#         }),
#     )

EMPTY_ITEM_ERROR = "You can't have an empty list item"

class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg'
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR }
        }

    # overloading the save method from the parent modelform class
    def save(self, for_list):
        # self.istance is an instance of the model object defined in class Meta
        self.instance.list = for_list
        return super().save()