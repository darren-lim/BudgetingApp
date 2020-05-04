from django import forms
from .fields import ListTextWidget
from .models import Transaction


class FormForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['amount', 'source', 'notes']

    def __init__(self, *args, **kwargs):
        _source_list = kwargs.pop('source', None)
        user = kwargs.pop('user', None)
        super(FormForm, self).__init__(*args, **kwargs)

        # the "name" parameter will allow you to use the same widget more than once in the same
            # form, not setting this parameter differently will cuse all inputs display the
            # same list.
        self.fields['source'].widget = ListTextWidget(data_list=_source_list, name='source')
