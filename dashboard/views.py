from django.shortcuts import render
from .forms import ConfiguracaoForm

def index(request):
    form = ConfiguracaoForm(request.POST or None)
    config = None

    if request.method == 'POST' and form.is_valid():
        config = form.cleaned_data

    return render(request, 'dashboard/index.html', {
        'form': form,
        'config': config
    })
