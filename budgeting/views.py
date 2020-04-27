# very import import!! Allows us to return a rendered template.
# Our views need to return an HttpResponse or exception.Render returns an HttpResponse in the background
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.http import HttpResponse
from .models import Transaction


class TransListView(ListView):
    model = Transaction
    template_name = 'budgeting/home.html'
    context_object_name = 'transactions'
    # the "-" sign makes transactions order from newest to oldest (top-bottom order)
    ordering = ['-date_posted']

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
    model = Transaction
    fields = ['t_type', 'amount', 'source', 'notes']

    def form_valid(self, form):  # sets the logged in user as the author of that transaction
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = "Create Transaction"
        context["title"] = title
        return context


# UserPassesTestMixin can be used as a parameter if we implement test_func
class TransUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = ['t_type', 'amount', 'source', 'notes']

    def form_valid(self, form):  # sets the logged in user as the author of that transaction
        form.instance.author = self.request.user
        return super().form_valid(form)

    '''def test_func(self): # prevents any other users from updating but this shouldn't happen in the first place because transactions are private (more for smth like twitter)
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False'''


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


'''transactions = [
    {'type': 'Withdrawal',
     'amount': '70',
     'source': 'Groceries',
     'notes': '',
     'date_posted': 'April 4, 2020'},

    {'type': 'Deposit',
     'amount': '20',
     'source': 'Part-time Job',
     'notes': '',
     'date_posted': 'April 4, 2020'}
]


def home(request):
    context = {'transactions': Transaction.objects.all()}
    # reference subdirectory within the template file.
    # in the 3rd paramter we pass in the information for our home page in the form of a dictionary called context.
    # our views will look for 'context'(key)
    return render(request, 'budgeting/home.html', context)
'''
