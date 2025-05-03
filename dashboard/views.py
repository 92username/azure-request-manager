from django.shortcuts import render
from .forms import ConfiguracaoForm
import requests

def index(request):
    form = ConfiguracaoForm(request.POST or None)
    config = None
    response_status = None

    if request.method == 'POST' and form.is_valid():
        config = form.cleaned_data

        # Montar a URL da Azure
        base_url = "http://191.234.214.44"
        rota = config['rota']
        if config['erro_simulado']:
            rota = "/api/v1/status/500"  # Simulação de erro

        url_final = f"{base_url}{rota}"

        try:
            r = requests.get(url_final, timeout=5)
            response_status = r.status_code
        except Exception as e:
            response_status = f"Erro: {e}"

    return render(request, 'dashboard/index.html', {
        'form': form,
        'config': config,
        'status': response_status
    })
