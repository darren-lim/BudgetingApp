# use this for month amounts
import datetime
# very import import!! Allows us to return a rendered template.
# Our views need to return an HttpResponse or exception.Render returns an HttpResponse in the background
import decimal

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Transaction, Total, History, Categories
from .forms import TransactionForm, UpdateForm, TotalForm, CategoryForm, CategoryUpdateForm
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
                                        transaction.d_amount
                    else:
                        amount_gained = transaction.d_amount
                    obj_tuple = History.objects.update_or_create(
                        month=month, year=year, author=self.request.user, defaults={'monthly_amount_gained': amount_gained})
                    obj_tuple[0].save()
                elif transaction.t_type == 'Expense':
                    if historyqueryset.first() is not None and historyqueryset.first().monthly_amount_spent is not None:
                        amount_spent = historyqueryset.first().monthly_amount_spent + \
                                       transaction.d_amount
                    else:
                        amount_spent = transaction.d_amount
                    obj_tuple = History.objects.update_or_create(
                        month=month, year=year, author=self.request.user, defaults={'monthly_amount_spent': amount_spent})
                    obj_tuple[0].save()
                obj_tuple_t = Transaction.objects.update_or_create(id=transaction.id,
                                                                   defaults={'month': month, 'year': year, 'in_history': True})
                obj_tuple_t[0].save()

            # setting total amount to user's current balance when they first started using the app (initial_amount)
            total_amount = decimal.Decimal(
                totalqueryset.first().initial_amount) * 100
            total_amount = int(total_amount)
            # checking to see if there any existing transactions
            # if there are we have to update our totals database
            # if not, we just return the total_amount
            transqueryset2 = Transaction.objects.filter(
                author=self.request.user).order_by('-date_posted')
            transdict = transqueryset2.aggregate(Sum('d_amount'))
            if transdict.get('d_amount__sum') is not None:
                historyqueryset2 = History.objects.filter(
                    author=self.request.user)
                historydict1 = historyqueryset2.aggregate(
                    Sum('monthly_amount_gained'))
                incomes = historydict1.get("monthly_amount_gained__sum")
                historydict2 = historyqueryset2.aggregate(
                    Sum('monthly_amount_spent'))
                expenses = historydict2.get("monthly_amount_spent__sum")
                if incomes is not None and expenses is not None:
                    total_amount -= expenses
                    total_amount += incomes

                elif incomes is None and expenses is not None:
                    total_amount -= expenses

                elif incomes is not None and expenses is None:
                    total_amount += incomes
                totalqueryset.update(
                    total_amount=total_amount, total_amount_gained=incomes, total_amount_spent=expenses)
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

                '''-----------------------------------------------------------------'''

                ExpenseLabels = []
                ExpenseData = []
                IncomeLabels = []
                IncomeData = []

                expense_dict = dict()
                income_dict = dict()

                current_queryset = Transaction.objects.filter(
                    author=self.request.user, year=current_year, month=current_month)

                for transaction in current_queryset:
                    if transaction.t_type == 'Expense':
                        if transaction.source in expense_dict:
                            expense_dict[transaction.source] += float(transaction.d_amount)/100
                        else:
                            expense_dict[transaction.source] = float(transaction.d_amount)/100
                    elif transaction.t_type == 'Income':
                        if transaction.source in income_dict:
                            income_dict[transaction.source] += float(
                                transaction.d_amount)/100
                        else:
                            income_dict[transaction.source] = float(
                                transaction.d_amount)/100

                for key, value in expense_dict.items():
                    ExpenseLabels.append(key)
                    ExpenseData.append(value)

                for key, value in income_dict.items():
                    IncomeLabels.append(key)
                    IncomeData.append(value)

                if monthly_gain is None:
                    monthly_gain = 0
                if monthly_spent is None:
                    monthly_spent = 0
                '''-----------------------------------------------------------------'''
                # Category goals
                # categoryDict = categoryQuerySet.aggregate(
                # Sum('d_amount'))
                # we still need to request the user's goals in a different view...
                # also remember to divide output by 100 since we are storing amounts as ints.

                return {'total': round(decimal.Decimal(total_amount)/100, 2),
                        'transaction_list': transqueryset2[:5],
                        'monthly_gain': round(decimal.Decimal(monthly_gain)/100, 2),
                        'monthly_spent': round(decimal.Decimal(monthly_spent)/100, 2),
                        'expense_labels': ExpenseLabels,
                        'expense_data': ExpenseData,
                        'income_labels': IncomeLabels,
                        'income_data': IncomeData,
                        # 'category_dict': categoryDict
                        }

            return {'total': round(decimal.Decimal(total_amount)/100, 2),
                    'transaction_list': [],
                    'monthly_gain': 0,
                    'monthly_spent': 0,
                    'expense_labels': [],
                    'expense_data': [],
                    'income_labels': [],
                    'income_data': [],
                    # 'category_dict': {}
                    }
        return {'total': None,
                'transaction_list': [],
                'monthly_gain': 0,
                'monthly_spent': 0,
                'expense_labels': [],
                'expense_data': [],
                'income_labels': [],
                'income_data': [],
                # 'category_dict': {}
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
    choices = None

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs['parameter'] == "Income":
            self.choices = Categories.objects.filter(
                author=request.user).filter(is_expense=False)
        elif self.kwargs['parameter'] == "Expense":
            self.choices = Categories.objects.filter(
                author=request.user).filter(is_expense=True)
        return super(TransCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TransCreateView, self).get_context_data(**kwargs)
        context['t_type'] = self.kwargs['parameter']
        return context

    # if I leave out get_form() the object is successfully saved
    # but the user's choice is not limited

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['choices'] = self.choices
        return kwargs

    def form_valid(self, form):  # sets the logged in user as the author of that transaction
        form.instance.author = self.request.user
        form.instance.t_type = self.kwargs['parameter']
        # we set "amount"s value * 100 equal to the "d_amount" which is what we use to aggregate in the end.
        form.instance.d_amount = int(form.cleaned_data['amount'] * 100)

        #category = Categories.objects.get(
        #    author=self.request.user, category=form.cleaned_data['category'])
        if self.kwargs['parameter'] == "Income":
            m_income = int(form.cleaned_data['amount'] * 100)
            m_amount = round(decimal.Decimal(m_income)/100, 2)
            category_tuple = Categories.objects.update_or_create(author=self.request.user, category=form.cleaned_data['category'],
                                                                 defaults={'monthly_amount': m_amount, 'current_monthly_income': m_amount})
            category_tuple[0].save()
        else:
            m_expense = int(form.cleaned_data['amount'] * 100)
            m_amount = round(decimal.Decimal(m_expense) / 100, 2)
            '''
            category.current_monthly_spent += int(
                form.cleaned_data['amount'] * 100)
            category.monthly_amount = round(decimal.Decimal(
                category.current_monthly_spent) / 100, 2)
            '''
            category_tuple = Categories.objects.update_or_create(author=self.request.user, category=form.cleaned_data['category'],
                                                                 defaults={'monthly_amount': m_amount, 'current_monthly_spent': m_expense})
            category_tuple[0].save()

        return super().form_valid(form)


# UserPassesTestMixin can be used as a parameter if we implement test_func
class TransUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = UpdateForm
    template_name = 'budgeting/transaction_update.html'
    choices = None
    success_url = '/all_transactions/'
    # if I leave out get_form() the object is successfully saved
    # but the user's choice is not limited

    def dispatch(self, request, *args, **kwargs):
        thisTrans = self.get_object()
        category = Categories.objects.get(
            author=request.user, category=thisTrans.category)
        t_type = thisTrans.t_type
        print(t_type)
        if t_type == "Income":
            print("THIS INCOME")
            category.current_monthly_income -= thisTrans.d_amount
            category.save()
            self.choices = Categories.objects.filter(
                author=request.user, is_expense=False)
        else:
            print("THIS EXPEMSE")
            category.current_monthly_spent -= thisTrans.d_amount
            category.save()
            self.choices = Categories.objects.filter(
                author=request.user, is_expense=True)
        return super(TransUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['choices'] = self.choices
        return kwargs

    def form_valid(self, form):  # sets the logged in user as the author of that transaction
        form.instance.author = self.request.user
        form.instance.d_amount = int(form.cleaned_data['amount'] * 100)
        self.update()
        return super().form_valid(form)

    def update(self):
        # totalQuerySet = Total.objects.filer(author=self.request.user)
        transaction = self.get_object()
        year = transaction.year
        month = transaction.month
        # creating history queryset!
        historyObj = History.objects.get(
            author=self.request.user, year=year, month=month)
        category = Categories.objects.get(
            author=self.request.user, category=transaction.category)
        if transaction.t_type == 'Income':
            updated_amount = historyObj.monthly_amount_gained - transaction.d_amount

            obj_tuple = History.objects.update_or_create(month=month, year=year, author=self.request.user,
                                                         defaults={'monthly_amount_gained': updated_amount})
            obj_tuple[0].save()

            category.current_monthly_income += transaction.d_amount
            category.monthly_amount = round(decimal.Decimal(
                category.current_monthly_income) / 100, 2)
            category_tuple = Categories.objects.update_or_create(author=self.request.user, category=self.model.category,
                                                                 defaults={'monthly_amount': category.monthly_amount, 'current_monthly_income': category.current_monthly_income})
            category_tuple[0].save()

        elif transaction.t_type == "Expense":
            updated_amount = historyObj.monthly_amount_spent - transaction.d_amount
            obj_tuple = History.objects.update_or_create(month=month, year=year, author=self.request.user,
                                                         defaults={'monthly_amount_spent': updated_amount})
            obj_tuple[0].save()

            category.current_monthly_spent += transaction.d_amount
            category.monthly_amount = round(decimal.Decimal(
                category.current_monthly_spent) / 100, 2)
            category_tuple = Categories.objects.update_or_create(author=self.request.user, category=transaction.category,
                                                                 defaults={'monthly_amount': category.monthly_amount, 'current_monthly_spent': category.current_monthly_spent})
            category_tuple[0].save()


class TransDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    success_url = '/all_transactions/'  # goes to the homepage with all transactions.

    def delete(self, *args, **kwargs):
        transaction = self.get_object()
        year = transaction.year
        month = transaction.month
        # creating history queryset!
        category = Categories.objects.get(
            author=self.request.user, category=transaction.category)
        historyqueryset = History.objects.filter(
            author=self.request.user, year=year, month=month)
        if transaction.t_type == 'Income':

            updated_amount = historyqueryset.first().monthly_amount_gained - \
                transaction.d_amount
            obj_tuple = History.objects.update_or_create(month=month, year=year, author=self.request.user,
                                                         defaults={'monthly_amount_gained': updated_amount})
            obj_tuple[0].save()
            m_income = category.current_monthly_income - transaction.d_amount
            m_amount = round(decimal.Decimal(m_income) / 100, 2)
            category_tuple = Categories.objects.update_or_create(author=self.request.user, category=transaction.category,
                                                                 defaults={'monthly_amount': m_amount, 'current_monthly_income': m_income})
            category_tuple[0].save()

        elif transaction.t_type == "Expense":
            updated_amount = historyqueryset.first().monthly_amount_spent - \
                transaction.d_amount
            obj_tuple = History.objects.update_or_create(month=month, year=year, author=self.request.user,
                                                         defaults={'monthly_amount_spent': updated_amount})
            obj_tuple[0].save()

            # category.current_monthly_spent -= transaction.d_amount
            # category.monthly_amount = round(decimal.Decimal(
            #    category.current_monthly_spent) / 100, 2)
            m_spent = category.current_monthly_spent - transaction.d_amount
            m_amount = round(decimal.Decimal(m_spent) / 100, 2)
            category_tuple = Categories.objects.update_or_create(author=self.request.user, category=transaction.category,
                                                                 defaults={'monthly_amount': m_amount, 'current_monthly_spent': m_spent})
            category_tuple[0].save()

        return super(TransDeleteView, self).delete(*args, **kwargs)


class TotalCreateView(LoginRequiredMixin, CreateView):
    model = Total
    form_class = TotalForm
    template_name = 'budgeting/total_form.html'

    def form_valid(self, form):  # sets the logged in user as the author of that transaction and sets the type when user clicks Income/Expense
        form.instance.author = self.request.user
        return super().form_valid(form)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Categories
    form_class = CategoryForm
    template_name = 'budgeting/category_form.html'
    success_url = '/category_details/'

    def form_valid(self, form):  # sets the logged in user as the author of that transaction and sets the type when user clicks Income/Expense
        form.instance.author = self.request.user
        m_goal = form.cleaned_data["monthly_goal"]
        if m_goal is None:
            m_goal = 0
        self.model.int_monthly_goal = m_goal*100
        form.cleaned_data["monthly_goal"] = 0
        return super().form_valid(form)


class CategoryListView(ListView):
    model = Categories
    template_name = 'budgeting/category_details.html'
    context_object_name = 'categories'
    paginate_by = 15

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(author=self.request.user)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    # only updates the monthly goal
    model = Categories
    form_class = CategoryUpdateForm
    template_name = 'budgeting/category_update.html'
    success_url = '/category_details/'

    def dispatch(self, request, *args, **kwargs):
        return super(CategoryUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_valid(self, form):  # sets the logged in user as the author of that transaction
        form.instance.author = self.request.user
        self.model.int_monthly_goal = form.cleaned_data["monthly_goal"] * 100
        return super().form_valid(form)

    def update(self, *args, **kwargs):
        return super(CategoryUpdateView, self).update(*args, **kwargs)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Categories
    template_name = 'budgeting/category_confirm_delete.html'
    success_url = '/category_details/'

    def delete(self, *args, **kwargs):
        return super(CategoryDeleteView, self).delete(*args, **kwargs)


def about(request):
    # in the 3rd paramter we pass in the title directly as a dictionary. This will pass into our about.html.
    return render(request, 'budgeting/about.html', {'title': 'About'})
