import streamlit as st
import urllib.parse

# Configuração da página
st.set_page_config(page_title="Simulador de Orçamento", page_icon="🚗", layout="centered")

st.title("🚗 Simulador de Orçamento Estético Automotivo")
st.write("Preencha os detalhes para obter uma estimativa rápida do serviço nas peças do seu veículo.")

st.divider()

# --- 1. DADOS DE CONTATO ---
st.subheader("📱 Seus Dados de Contato")
nome = st.text_input("Seu Nome:", placeholder="Ex: João Silva")
telefone = st.text_input("Seu Telefone / WhatsApp:", placeholder="Ex: (47) 99999-9999")

st.divider()

# --- 2. INPUTS DO SERVIÇO ---
st.subheader("🔧 Detalhes do Serviço")

# Quantidade de peças
quantidade_pecas = st.number_input(
    "1. Quantidade de peças a serem avaliadas:", 
    min_value=1, 
    value=1, 
    step=1
)

# Gravidade do defeito
defeito = st.selectbox(
    "2. Qual a gravidade média do defeito?",
    ["Leve", "Mediana", "Muito avariada"],
    help="Leve (R$ 300,00) | Mediana (R$ 450,00) | Muito avariada (R$ 600,00)"
)
st.caption(f"_*Opção selecionada aplica valor base por peça de acordo com o dano._")

# Finalização com preços visíveis
finalizacao = st.radio(
    "3. Tipo de Finalização desejada:",
    ["Básica (Inclusa)", "Completa (+ R$ 300,00)"],
    horizontal=True
)

# Lavação com preços visíveis
precisa_lavacao = st.toggle("4. Deseja incluir Lavação no serviço?")

tipo_lavacao = "Nenhum"
if precisa_lavacao:
    tipo_lavacao = st.radio(
        "Selecione o tipo de lavação:",
        ["Básica (inclusa)", "Completa (+ R$ 30,00)"],
        horizontal=True
    )

st.divider()

# --- 3. LÓGICA DE CÁLCULO (O MOTOR) ---

# Preço base por peça de acordo com o defeito
if defeito == "Leve":
    preco_base_peca = 300.00
elif defeito == "Mediana":
    preco_base_peca = 450.00
else:
    preco_base_peca = 600.00

# Custo adicional por tipo de finalização
if "Completa" in finalizacao:
    adicional_finalizacao = 300
else:
    adicional_finalizacao = 0.00

# Custo adicional por tipo de lavação
if "Completa" in tipo_lavacao:
    adicional_lavacao = 50.00
else:
    adicional_lavacao = 0.00

# Cálculo dos valores
valor_por_peca = preco_base_peca + adicional_lavacao
valor_total = (valor_por_peca * quantidade_pecas) + adicional_finalizacao

# --- 4. EXIBIÇÃO DO RESULTADO ---

st.subheader("📊 Resumo da Estimativa")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Média por Peça", value=f"R$ {valor_por_peca:,.2f}")
with col2:
    st.metric(label="Valor Total Estimado", value=f"R$ {valor_total:,.2f}")

# Detalhamento Visual
with st.expander("🔍 Ver detalhamento dos custos"):
    st.write(f"• Reparo básico ({defeito}): R$ {preco_base_peca:,.2f} por peça")
    if adicional_finalizacao > 0:
        st.write(f"• Finalização Completa: + R$ {adicional_finalizacao:,.2f} por peça")
    if adicional_lavacao > 0:
        st.write(f"• Lavação selecionada: + R$ {adicional_lavacao:,.2f} por peça")

st.divider()

# --- 5. AÇÃO DE AGENDAMENTO (WHATSAPP) ---
st.subheader("🗓️ Agendar Avaliação Pessoalmente")
st.write("Clique no botão abaixo para enviar esse orçamento direto para o nosso WhatsApp e agendarmos a vistoria do seu veículo.")

# Insira o SEU número de WhatsApp aqui (com DDD, apenas números)
# Exemplo: "5547999999999" (55 do Brasil + DDD + Número)
SEU_WHATSAPP = "5548992103501" 

# Criando o texto da mensagem automática
texto_mensagem = f"""Olá! Gostaria de agendar uma avaliação física para o meu veículo.
Aqui estão os detalhes do meu orçamento simulado:

*Nome:* {nome}
*Telefone:* {telefone}
*Quantidade de peças:* {quantidade_pecas}
*Gravidade:* {defeito}
*Finalização:* {finalizacao.split(' (+')[0]}
*Lavação:* {tipo_lavacao.split(' (+')[0]}

*Valor Total Estimado:* R$ {valor_total:,.2f}"""

# Codificando o texto para formato de link de internet
mensagem_codificada = urllib.parse.quote(texto_mensagem)
link_whatsapp = f"https://wa.me/{SEU_WHATSAPP}?text={mensagem_codificada}"

# Botão bonito que abre o WhatsApp
if nome and telefone:
    st.link_button("🟢 Enviar Orçamento e Agendar pelo WhatsApp", link_whatsapp, use_container_width=True)
else:
    st.warning("⚠️ Por favor, preencha seu *Nome* e *Telefone* no topo da página para liberar o botão de agendamento.")