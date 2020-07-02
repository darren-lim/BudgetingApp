# from django import forms
# from .fields import ListTextWidget
# from .models import Transaction, Total


# class TransactionForm(forms.ModelForm):

#     class Meta:
#         model = Transaction
#         fields = ['t_type', 'amount', 'source', 'category', 'date_posted', 'notes']
#         widgets = {
#             'date_posted': forms.DateInput(format='%m/%d/%Y', attrs={'placeholder': 'e.g. 02/15/2020'}),
#             'source': forms.TextInput(attrs={'placeholder': 'e.g. Part-time job, Utilities, Gas'}),
#         }

#     def __init__(self, *args, **kwargs):
#         _source_list = kwargs.pop('source', None)
#         user = kwargs.pop('user', None)
#         super(TransactionForm, self).__init__(*args, **kwargs)

#         # the "name" parameter will allow you to use the same widget more than once in the same
#         # form, not setting this parameter differently will cuse all inputs display the
#         # same list.
#         self.fields['source'].widget = ListTextWidget(
#             data_list=_source_list, name='source')


# class UpdateForm(TransactionForm):

#     class Meta:
#         model = Transaction
#         fields = ['t_type', 'amount', 'source', 'date_posted', 'notes']
#         widgets = {
#             'date_posted': forms.DateInput(format='%m/%d/%Y', attrs={'placeholder': 'e.g. 02/15/2020'}),
#             'source': forms.TextInput(attrs={'placeholder': 'e.g. Part-time job, Utilities, Gas'})
#         }


# class TotalForm(forms.ModelForm):

#     class Meta:
#         model = Total
#         fields = ['initial_amount']
