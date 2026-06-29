import streamlit as st
import urllib.parse

# Configuração da página
st.set_page_config(page_title="Simulador de Orçamento", page_icon="🚗", layout="centered")

st.title("🚗 Simulador de Orçamento Estético Automotivo")
st.write("Preencha os detalhes para obter uma estimativa rápida do serviço.")

st.divider()

# --- 1. DADOS DE CONTATO ---
st.subheader("📱 Seus Dados de Contato")
nome = st.text_input("Seu Nome:", placeholder="Ex: João Silva")
telefone = st.text_input("Seu Telefone / WhatsApp:", placeholder="Ex: (47) 99999-9999")

st.divider()

# --- 2. INPUTS DO SERVIÇO ---
st.subheader("🔧 Detalhes do Serviço")

# Quantidade de peças (Pode ser 0 agora)
quantidade_pecas = st.number_input(
    "1. Quantidade de peças para reparo de defeito (opcional):", 
    min_value=0, 
    value=0, 
    step=1
)

# Gravidade do defeito
defeito = st.selectbox(
    "2. Qual a gravidade média do defeito das peças?",
    ["Nenhum (Apenas Estética/Lavação/Finalização)", "Leve", "Mediana", "Muito avariada"],
    help="Leve (R$ 20,00) | Mediana (R$ 40,00) | Muito avariada (R$ 70,00)"
)

# Finalização (Cobrada por serviço ou lote se quantidade for 0, vamos assumir taxa única se for 0 peças ou multiplicar por 1 se for avulso)
finalizacao = st.radio(
    "3. Tipo de Finalização desejada:",
    ["Nenhuma / Não precisa", "Básica (Inclusa no reparo)", "Completa (+ R$ 15,00)"],
    index=0,
    horizontal=True
)

# Lavação à parte
tipo_lavacao = st.radio(
    "4. Deseja incluir Lavação no serviço?",
    ["Nenhuma / Não precisa", "Básica (+ R$ 10,00)", "Completa (+ R$ 25,00)"],
    index=0,
    horizontal=True
)

st.divider()

# --- 3. LÓGICA DE CÁLCULO (O MOTOR) ---

# Preço base do defeito
if defeito == "Leve":
    preco_base_peca = 20.00
elif defeito == "Mediana":
    preco_base_peca = 40.00
elif defeito == "Muito avariada":
    preco_base_peca = 70.00
else:
    preco_base_peca = 0.00

# Adicional de finalização
if "Completa" in finalizacao:
    adicional_finalizacao = 15.00
else:
    adicional_finalizacao = 0.00

# Adicional de lavação
if "Básica" in tipo_lavacao:
    adicional_lavacao = 10.00
elif "Completa" in tipo_lavacao:
    adicional_lavacao = 25.00
else:
    adicional_lavacao = 0.00

# Nova lógica de cálculo flexível:
# Se o usuário colocar peças, multiplica tudo pelas peças. 
# Se deixar 0 peças mas escolher lavação/finalização, calcula como 1 serviço avulso.
multiplicador = quantidade_pecas if quantidade_pecas > 0 else 1

custo_reparo_total = preco_base_peca * quantidade_pecas # Reparo sempre depende de ter peças
custo_finalizacao_total = adicional_finalizacao * multiplicador
custo_lavacao_total = adicional_lavacao * multiplicador

valor_total = custo_reparo_total + custo_finalizacao_total + custo_lavacao_total

# --- 4. EXIBIÇÃO DO RESULTADO ---

st.subheader("📊 Resumo da Estimativa")

# Se não tiver peças, mostra o valor do serviço avulso
if quantidade_pecas == 0 and valor_total > 0:
    st.metric(label="Valor Total (Serviço Avulso)", value=f"R$ {valor_total:,.2f}")
else:
    col1, col2 = st.columns(2)
    with col1:
        valor_por_peca = preco_base_peca + adicional_finalizacao + adicional_lavacao
        st.metric(label="Média por Peça", value=f"R$ {valor_por_peca:,.2f}")
    with col2:
        st.metric(label="Valor Total Estimado", value=f"R$ {valor_total:,.2f}")

# Detalhamento Visual Dinâmico
if valor_total > 0:
    with st.expander("🔍 Ver detalhamento dos custos"):
        if custo_reparo_total > 0:
            st.write(f"• Reparo de defeito ({quantidade_pecas}x {defeito}): R$ {custo_reparo_total:,.2f}")
        if custo_finalizacao_total > 0:
            st.write(f"• Finalização Completa: R$ {custo_finalizacao_total:,.2f}")
        if custo_lavacao_total > 0:
            st.write(f"• Lavação ({tipo_lavacao.split(' (+')[0]}): R$ {custo_lavacao_total:,.2f}")

st.divider()

# --- 5. AÇÃO DE AGENDAMENTO (WHATSAPP) ---
st.subheader("🗓️ Agendar Avaliação Pessoalmente")

# Lembre-se de colocar o seu número real aqui!
SEU_WHATSAPP = "5500000000000" 

texto_mensagem = f"""Olá! Gostaria de agendar uma avaliação física para o meu veículo.
Aqui estão os detalhes do meu orçamento simulado:

*Nome:* {nome}
*Telefone:* {telefone}
*Quantidade de peças:* {quantidade_pecas}
*Gravidade do Defeito:* {defeito}
*Finalização:* {finalizacao.split(' (+')[0]}
*Lavação:* {tipo_lavacao.split(' (+')[0]}

*Valor Total Estimado:* R$ {valor_total:,.2f}"""

mensagem_codificada = urllib.parse.quote(texto_mensagem)
link_whatsapp = f"https://wa.me/{SEU_WHATSAPP}?text={mensagem_codificada}"

# CONDIÇÃO ATUALIZADA: Só precisa de Nome, Telefone e que o valor seja maior que R$ 0
if nome and telefone and valor_total > 0:
    st.link_button("🟢 Enviar Orçamento e Agendar pelo WhatsApp", link_whatsapp, use_container_width=True)
else:
    st.warning("⚠️ Para liberar o botão de agendamento, preencha seu *Nome*, *Telefone* e selecione pelo menos um serviço (Lavação, Finalização ou Peças).")
