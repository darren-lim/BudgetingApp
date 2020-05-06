# very import import!! Allows us to return a rendered template.
# Our views need to return an HttpResponse or exception.Render returns an HttpResponse in the background
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Transaction
from .forms import TransactionForm, UpdateForm


class HomeView(ListView):
    model = Transaction
    template_name = 'budgeting/home.html'
    context_object_name = 'transactions'
    # the "-" sign makes transactions order from newest to oldest (top-bottom order)
    ordering = ['-date_posted']

    # maybe get the specific models???

    def get_queryset(self):

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
        return None


class TransListView(ListView):
    model = Transaction
    template_name = 'budgeting/all_transactions.html'
    context_object_name = 'transactions'
    # the "-" sign makes transactions order from newest to oldest (top-bottom order)
    ordering = ['-date_posted']

    # maybe get the specific models???

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.model.objects.filter(author=self.request.user)
        else:
            return None


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

    '''def test_func(self): # prevents any other users from updating but this shouldn't happen in the first place because transactions are private (more for smth like twitter)
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False'''


def about(request):
    # in the 3rd paramter we pass in the title directly as a dictionary. This will pass into our about.html.
    return render(request, 'budgeting/about.html', {'title': 'About'})
