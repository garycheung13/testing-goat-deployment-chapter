from django import forms
from django.core.exceptions import ValidationError

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
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

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
        # self.instance is an instance of the model object defined in class Meta
        self.instance.list = for_list
        return super().save()


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            # error_dict is a property of the validationError object
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            # update the error message
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)