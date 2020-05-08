# use this for month amounts
import datetime
# very import import!! Allows us to return a rendered template.
# Our views need to return an HttpResponse or exception.Render returns an HttpResponse in the background
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Transaction, Total, History
from .forms import TransactionForm, UpdateForm, TotalForm
from django.db.models import Sum


class HomeView(ListView):
    model = Total
    template_name = 'budgeting/home.html'
    context_object_name = "total"

    def get_queryset(self):
        if self.request.user.is_authenticated and self.model.objects.filter(author=self.request.user).exists():
            # creating querysets for transactions and totals.
            totalqueryset = self.model.objects.filter(
                author=self.request.user)
            transqueryset1 = Transaction.objects.filter(
                author=self.request.user, in_history=False).order_by('-date_posted')

            # filters through every transaction not already in history and assigns them to a history object.
            for transaction in transqueryset1:
                year = transaction.date_posted.year
                month = transaction.date_posted.month
                # creating history queryset!
                historyqueryset = History.objects.filter(
                    author=self.request.user, year=year, month=month)
                if transaction.t_type == 'Deposit':
                    if historyqueryset.first() is not None:
                        amount_gained = historyqueryset.first().monthly_amount_gained + \
                            transaction.amount

                    else:
                        amount_gained = transaction.amount
                    obj_tuple = History.objects.update_or_create(
                        month=month, year=year, author=self.request.user, defaults={'monthly_amount_gained': amount_gained})
                    obj_tuple[0].save()
                elif transaction.t_type == "Withdrawal":
<<<<<<< HEAD
                    if historyqueryset.first() is not None:
                        amount_spent = historyqueryset.first().monthly_amount_spent + transaction.amount
                        obj_tuple = History.objects.update_or_create(
                            month=month, year=year, author=self.request.user, defaults={'monthly_amount_spent': amount_spent})
                        obj_tuple[0].save()
=======
                    amount = transaction.amount * -1
                    if historyqueryset.first().monthly_amount_spent != None:
                        amount_spent = historyqueryset.first().monthly_amount_spent + amount
>>>>>>> e66dfd3312f55e6c09d515172977d98cd3cfc792
                    else:
                        amount_spent = transaction.amount
                    obj_tuple = History.objects.update_or_create(
                        month=month, year=year, author=self.request.user, defaults={'monthly_amount_spent': amount_spent})
                    obj_tuple[0].save()
                obj_tuple_t = Transaction.objects.update_or_create(id=transaction.id,
                                                                   defaults={'month': month, 'year': year, 'in_history': True})
                obj_tuple_t[0].save()

            # setting total amount to user's current balance when they first started using the app (initial_amount)
            total_amount = totalqueryset.first().initial_amount

            # checking to see if there any existing transactions
            # if there are we have to update our totals database
            # if not, we just return the total_amount
            transqueryset2 = Transaction.objects.filter(
                author=self.request.user).order_by('-date_posted')
            transdict = transqueryset2.aggregate(Sum('amount'))

            if transdict.get('amount__sum') is not None:
                historyqueryset2 = History.objects.all()
                historydict1 = historyqueryset2.aggregate(
                    Sum('monthly_amount_gained'))
                deposits = historydict1.get("monthly_amount_gained__sum")
                historydict2 = historyqueryset2.aggregate(
                    Sum('monthly_amount_spent'))
                withdrawals = historydict2.get("monthly_amount_spent__sum")
                if deposits is not None and withdrawals is not None:
                    total_amount -= withdrawals
                    total_amount += deposits

                elif deposits is None and withdrawals is not None:
                    total_amount -= withdrawals

                elif deposits is not None and withdrawals is None:
                    total_amount += deposits
                '''-----------------------------------------------------------------'''
                # creating current year and month string
                now = datetime.date.today()
                current_year = now.year
                current_month = now.month

                currentqueryset = History.objects.filter(
                    author=self.request.user, year=current_year, month=current_month)
                if currentqueryset.first() is None:
                    monthly_gain = 0
                    monthly_spent = 0
                else:
                    monthly_gain = currentqueryset.first().monthly_amount_gained
                    monthly_spent = currentqueryset.first().monthly_amount_spent
                totalqueryset.update(
                    total_amount=total_amount, total_amount_gained=deposits, total_amount_spent=withdrawals)

                labels = []
                data = []
                piequeryset = Transaction.objects.filter(
                    author=self.request.user, year=current_year, month=current_month, t_type='Withdrawal')
                for transaction in piequeryset:
                    labels.append(transaction.source)
                    amount = float(transaction.amount)
                    data.append(amount)
                return {'total': total_amount,
                        'transaction_list': transqueryset2[:5],
                        'monthly_gain': monthly_gain,
                        'monthly_spent': monthly_spent,
                        'labels': labels,
                        'data': data}

            return {'total': total_amount,
                    'transaction_list': None}
        '''
        if self.request.user.is_authenticated:
            labels = []
            data = []
            queryset = self.model.objects.filter(author=self.request.user)
            queryset = queryset.filter(t_type__iexact='Withdraw')
            for transaction in queryset:
                labels.append(transaction.source)
                amount = float(transaction.amount)
                data.append(amount)
            return {'transaction_list': self.model.objects.filter(author=self.request.user)[:5],
                    'labels': labels,
                    'data': data
                    }
        '''
        return {'total': None,
                'transaction_list': None
                }


class TransListView(ListView):
    model = Transaction
    template_name = 'budgeting/all_transactions.html'
    context_object_name = 'transactions'
    # the "-" sign makes transactions order from newest to oldest (top-bottom order)
    # ordering = model.objects.order_by('-date_posted')
    paginate_by = 15

    # maybe get the specific models???

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(author=self.request.user)
        else:
            raise Exception("Unauthorized Access, Please Log In")


class TransDetailView(DetailView):
    model = Transaction
    # we don't have to add the name of the template to search for b/c by default, our classes will look for template with this naming convention:
    # <app>/<model>_<viewtype>.html (as long as our templates are in a directory with budgeting (the name of our app), transaction, and the type, we are good)


class TransCreateView(LoginRequiredMixin, CreateView):
    # source = ('Job', 'Food', 'Gas')
    model = Transaction
    form_class = TransactionForm
    template_name = 'budgeting/transaction_form.html'

    def get_context_data(self, **kwargs):
        context = super(TransCreateView, self).get_context_data(**kwargs)
        context['t_type'] = self.kwargs['parameter']
        return context

    # if I leave out get_form() the object is successfully saved
    # but the user's choice is not limited

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        source = ('Job', 'Food', 'Gas')
        kwargs['source'] = source
        return kwargs

    def form_valid(self, form):  # sets the logged in user as the author of that transaction
        form.instance.author = self.request.user
        form.instance.t_type = self.kwargs['parameter']
        return super().form_valid(form)


# UserPassesTestMixin can be used as a parameter if we implement test_func
class TransUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = UpdateForm
    template_name = 'budgeting/transaction_update.html'

    # if I leave out get_form() the object is successfully saved
    # but the user's choice is not limited

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        source = ('Job', 'Food', 'Gas')
        kwargs['source'] = source
        return kwargs

    def form_valid(self, form):  # sets the logged in user as the author of that transaction
        form.instance.author = self.request.user
        return super().form_valid(form)


class TransDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = '/'  # goes to the homepage with all transactions.
    def delete(self, *args, **kwargs):

        totalqueryset = Total.objects.filter(
            author=self.request.user)

        transaction = self.get_object()
        year = transaction.date_posted.year
        month = transaction.date_posted.month
        # creating history queryset!
        historyqueryset = History.objects.filter(
            author=self.request.user, year=year, month=month)
        if transaction.t_type == 'Deposit':
            total_updated_amount = totalqueryset.first().total_amount - transaction.amount
            total_updated_gained_amount = totalqueryset.first().total_amount_gained - \
                transaction.amount

            updated_amount = historyqueryset.first().monthly_amount_gained - \
                transaction.amount
            obj_tuple_total = Total.objects.update_or_create(author=self.request.user, defaults={'total_amount': total_updated_amount,
                                                                                                 'total_amount_gained': total_updated_gained_amount})
            obj_tuple_total[0].save()
            obj_tuple = History.objects.update_or_create(month=month, year=year, author=self.request.user,
                                                         defaults={'monthly_amount_gained': updated_amount})
            obj_tuple[0].save()
        elif transaction.t_type == "Withdrawal":
            total_updated_amount = totalqueryset.first().total_amount + transaction.amount
            total_updated_spent_amount = totalqueryset.first().total_amount_spent - \
                transaction.amount

            updated_amount = historyqueryset.first().monthly_amount_spent - \
                transaction.amount
            obj_tuple_total = Total.objects.update_or_create(author=self.request.user, defaults={'total_amount': total_updated_amount,
                                                                                                 'total_amount_spent': total_updated_spent_amount})
            obj_tuple_total[0].save()
            obj_tuple = History.objects.update_or_create(month=month, year=year, author=self.request.user,
                                                         defaults={'monthly_amount_spent': total_updated_spent_amount})
            obj_tuple[0].save()

        return super(TransDeleteView, self).delete(*args, **kwargs)

    '''def test_func(self): # prevents any other users from updating but this shouldn't happen in the first place because transactions are private (more for smth like twitter)
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False'''


class TotalCreateView(LoginRequiredMixin, CreateView):
    model = Total
    form_class = TotalForm
    template_name = 'budgeting/total_form.html'

    def form_valid(self, form):  # sets the logged in user as the author of that transaction and sets the type when user clicks deposit/withdrawal
        form.instance.author = self.request.user
        return super().form_valid(form)


def about(request):
    # in the 3rd paramter we pass in the title directly as a dictionary. This will pass into our about.html.
    return render(request, 'budgeting/about.html', {'title': 'About'})
