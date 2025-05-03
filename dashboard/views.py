import threading
import time
import requests
from django.shortcuts import render
from .forms import ConfiguracaoForm

# Variável global para evitar múltiplas threads simultâneas
thread_ativa = False

def enviar_requisicoes(config):
    global thread_ativa
    thread_ativa = True

    frequencia = int(config['frequencia'])
    rota = config['rota']
    if config['erro_simulado']:
        rota = "/api/v1/status/500"

    url = f"http://191.234.214.44:8000{rota}"

    print(f"Iniciando loop de requisições para {url} a cada {frequencia} segundos.")

    for i in range(20):  # Limite de 20 requisições por sessão
        try:
            resposta = requests.get(url, timeout=5)
            print(f"[{i+1}] Status: {resposta.status_code}")
        except Exception as e:
            print(f"[{i+1}] Erro: {e}")

        time.sleep(frequencia)

    print("Loop de requisições encerrado.")
    thread_ativa = False

def index(request):
    global thread_ativa

    form = ConfiguracaoForm(request.POST or None)
    config = None
    mensagem = None

    if request.method == 'POST' and form.is_valid():
        config = form.cleaned_data

        if not thread_ativa:
            t = threading.Thread(target=enviar_requisicoes, args=(config,))
            t.start()
            mensagem = "Loop iniciado com sucesso!"
        else:
            mensagem = "Já existe um loop em execução. Aguarde ou reinicie o servidor."

    return render(request, 'dashboard/index.html', {
        'form': form,
        'config': config,
        'mensagem': mensagem,
    })
