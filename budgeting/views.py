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
from django.shortcuts import redirect
from django.contrib import messages


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
                if transaction.t_type == 'Income':
                    if historyqueryset.first() is not None and historyqueryset.first().monthly_amount_gained is not None:
                        amount_gained = historyqueryset.first().monthly_amount_gained + \
                            transaction.amount
                    else:
                        amount_gained = transaction.amount
                    obj_tuple = History.objects.update_or_create(
                        month=month, year=year, author=self.request.user, defaults={'monthly_amount_gained': amount_gained})
                    obj_tuple[0].save()
                elif transaction.t_type == "Expense":
                    if historyqueryset.first() is not None and historyqueryset.first().monthly_amount_spent is not None:
                        amount_spent = historyqueryset.first().monthly_amount_spent + transaction.amount
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
                Incomes = historydict1.get("monthly_amount_gained__sum")
                historydict2 = historyqueryset2.aggregate(
                    Sum('monthly_amount_spent'))
                Expenses = historydict2.get("monthly_amount_spent__sum")
                if Incomes is not None and Expenses is not None:
                    total_amount -= Expenses
                    total_amount += Incomes

                elif Incomes is None and Expenses is not None:
                    total_amount -= Expenses

                elif Incomes is not None and Expenses is None:
                    total_amount += Incomes
                '''-----------------------------------------------------------------'''
                # creating current year and month string
                now = datetime.date.today()
                current_year = now.year
                current_month = now.month

                currentqueryset = History.objects.filter(
                    author=self.request.user, year=current_year, month=current_month)
                if currentqueryset.first() is None:
                    monthly_gain = None
                    monthly_spent = None
                else:
                    monthly_gain = currentqueryset.first().monthly_amount_gained
                    monthly_spent = currentqueryset.first().monthly_amount_spent
                totalqueryset.update(
                    total_amount=total_amount, total_amount_gained=Incomes, total_amount_spent=Expenses)

                ExpenseLabels = []
                ExpenseData = []
                IncomeLabels = []
                IncomeData = []

                expenses = dict()
                income = dict()

                piequeryset = Transaction.objects.filter(
                    author=self.request.user, year=current_year, month=current_month)
                for transaction in piequeryset:
                    if transaction.t_type == 'Expense':
                        if transaction.source in expenses:
                            expenses[transaction.source] += float(transaction.amount)
                        else:
                            expenses[transaction.source] = float(transaction.amount)
                    elif transaction.t_type == 'Income':
                        if transaction.source in income:
                            income[transaction.source] += float(transaction.amount)
                        else:
                            income[transaction.source] = float(transaction.amount)

                for key, value in expenses.items():
                    ExpenseLabels.append(key)
                    ExpenseData.append(value)

                for key, value in income.items():
                    IncomeLabels.append(key)
                    IncomeData.append(value)

                if monthly_gain is None:
                    monthly_gain = 0
                if monthly_spent is None:
                    monthly_spent = 0
                return {'total': total_amount,
                        'transaction_list': transqueryset2[:5],
                        'monthly_gain': monthly_gain,
                        'monthly_spent': monthly_spent,
                        'expense_labels': ExpenseLabels,
                        'expense_data': ExpenseData,
                        'income_labels': IncomeLabels,
                        'income_data': IncomeData
                        }

            return {'total': total_amount,
                    'transaction_list': [],
                    'monthly_gain': 0,
                    'monthly_spent': 0,
                    'expense_labels': [],
                    'expense_data': [],
                    'income_labels': [],
                    'income_data': []
                    }
        return {'total': None,
                'transaction_list': [],
                'monthly_gain': 0,
                'monthly_spent': 0,
                'expense_labels': [],
                'expense_data': [],
                'income_labels': [],
                'income_data': []
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
        if transaction.t_type == 'Income':
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
        elif transaction.t_type == "Expense":
            total_updated_amount = totalqueryset.first().total_amount + transaction.amount
            total_updated_spent_amount = totalqueryset.first().total_amount_spent - \
                transaction.amount

            updated_amount = historyqueryset.first().monthly_amount_spent - \
                transaction.amount
            obj_tuple_total = Total.objects.update_or_create(author=self.request.user, defaults={'total_amount': total_updated_amount,
                                                                                                 'total_amount_spent': total_updated_spent_amount})
            obj_tuple_total[0].save()
            obj_tuple = History.objects.update_or_create(month=month, year=year, author=self.request.user,
                                                         defaults={'monthly_amount_spent': updated_amount})
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

    def get(self, request, *args, **kwargs):
        total = None
        try:
            total = Total.objects.get(author=request.user)
        except Exception as e:
            print(e)
        if total:
            form = TotalForm(instance=total)
        else:
            form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        total = Total.objects.filter(author=request.user).first()
        if total:
            form = TotalForm(request.POST, instance=total)
        else:
            form = TotalForm(request.POST)
        if form.is_valid():
            total_obj = form.save(commit=False)
            total_obj.author = request.user
            total_obj.save()
            return redirect('budgeting-home')
        return render(request, self.template_name, {'form': form})

    def form_valid(self, form):  # sets the logged in user as the author of that transaction and sets the type when user clicks Income/Expense
        form.instance.author = self.request.user
        return super().form_valid(form)


def about(request):
    # in the 3rd paramter we pass in the title directly as a dictionary. This will pass into our about.html.
    return render(request, 'budgeting/about.html', {'title': 'About'})
