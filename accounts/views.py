from django.shortcuts import render
from .forms import AccountsForm


def register_view(request, *args, **kwargs):
    form = AccountsForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {'form': form}
    return render(request, 'registration/register.html', context)
