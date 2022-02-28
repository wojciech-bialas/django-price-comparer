from django.shortcuts import render, redirect
from .forms import AccountsForm


def register_view(request, *args, **kwargs):
    form = AccountsForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect('home')
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)
