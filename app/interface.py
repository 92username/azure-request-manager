import streamlit as st

# Configuração da página
st.set_page_config(page_title="Azure Request Manager", layout="wide")

# Menu lateral
st.sidebar.title("🔧 Azure Request Manager")
page = st.sidebar.radio("Navegar", ["Configuração", "Execução", "Logs", "Status"])

# Página: Configuração
if page == "Configuração":
    st.title("🔧 Configuração de Requisições")

    freq = st.slider("Frequência das requisições (em segundos)", 5, 60, 10)
    rota = st.selectbox("Rota da Azure API", [
        "/api/v1/event",
        "/api/v1/users",
        "/api/v1/status/200",
        "/api/v1/delay/3"
    ])
    simular_erro = st.checkbox("Simular erro intencional?")

    st.session_state["config"] = {
        "freq": freq,
        "rota": rota,
        "erro": simular_erro
    }

    st.success("Configuração salva em sessão.")

# Página: Execução
elif page == "Execução":
    st.title("🚀 Execução das Requisições")

    config = st.session_state.get("config", None)

    if config:
        st.write("**Configuração atual:**")
        st.json(config)

        if st.button("Iniciar requisições"):
            st.warning("Envio de requisições em breve... (módulo em desenvolvimento)")
    else:
        st.info("Configure os parâmetros antes de iniciar.")

# Página: Logs
elif page == "Logs":
    st.title("📜 Visualizar Logs")
    st.info("Logs recentes aparecerão aqui quando implementados.")

# Página: Status
elif page == "Status":
    st.title("📈 Status da API na Azure")
    st.info("Aqui será exibido se a API está online ou offline.")
