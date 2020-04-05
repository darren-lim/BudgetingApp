# very import import!! Allows us to return a rendered template.
# Our views need to return an HttpResponse or exception.Render returns an HttpResponse in the background
from django.shortcuts import render
from django.http import HttpResponse

transactions = [
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
    context = {'transactions': transactions}
    # reference subdirectory within the template file.
    # in the 3rd paramter we pass in the information for our home page in the form of a dictionary called posts.
    # our views will look for 'posts'(key)
    return render(request, 'budgeting/home.html', context)


def about(request):
    # in the 3rd paramter we pass in the title directly as a dictionary. This will pass into our about.html.
    return render(request, 'budgeting/about.html', {'title': 'About'})
