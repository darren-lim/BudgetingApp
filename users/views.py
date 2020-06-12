from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from .forms import UserRegisterForm, UserUpdateForm


# def register(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, 'Your Account has been Created, you are now able to Log In')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})


# @login_required
# def profile(request):
#     if request.method == "POST":
#         # username
#         u_form = UserUpdateForm(request.POST, instance=request.user)
#         if u_form.is_valid():
#             u_form.save()
#             messages.success(request, 'Your Account has been Updated')
#             return redirect('profile')
#     else:
#         u_form = UserUpdateForm(instance=request.user)

#     context = {
#         'u_form': u_form,
#     }
#     return render(request, 'users/profile.html', context)
