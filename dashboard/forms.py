from django import forms

class ConfiguracaoForm(forms.Form):
    FREQUENCIA_CHOICES = [(x, f"{x} segundos") for x in range(5, 65, 5)]
    ROTA_CHOICES = [
        ("/api/v1/event", "/api/v1/event"),
        ("/api/v1/users", "/api/v1/users"),
        ("/api/v1/status/200", "/api/v1/status/200"),
        ("/api/v1/delay/3", "/api/v1/delay/3"),
    ]

    frequencia = forms.ChoiceField(choices=FREQUENCIA_CHOICES, label="Frequência")
    rota = forms.ChoiceField(choices=ROTA_CHOICES, label="Rota da API Azure")
    erro_simulado = forms.BooleanField(label="Simular erro?", required=False)
