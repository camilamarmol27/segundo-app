import pandas as pd
import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Simulador de Custos e Orçamento", page_icon="💰", layout="wide"
)

# Base de Dados Interna (Simulada)
@st.cache_data
def carregar_dados():
  data = {
      "Item": [
          "Aço Inox Especial",
          "Alumínio Estrutural",
          "Soldador Sênior",
          "Auxiliar de Produção",
          "Frete Regional",
          "Combustível Frota",
          "Eletricidade Fábrica",
          "Manutenção Preventiva",
          "Chaves e Brocas",
          "EPIs Completos",
          "Licenciamento CAD",
          "Consultoria Técnica",
      ],
      "Categoria": [
          "Matéria-Prima",
          "Matéria-Prima",
          "Mão de Obra",
          "Mão de Obra",
          "Logística",
          "Logística",
          "Energia",
          "Ferramentas",
          "Ferramentas",
          "Ferramentas",
          "Outros",
          "Mão de Obra",
      ],
      "Valor (R$)": [
          4500.0,
          3200.0,
          5000.0,
          2200.0,
          1500.0,
          800.0,
          1800.0,
          1200.0,
          600.0,
          900.0,
          2500.0,
          3000.0,
      ],
      "Prioridade": [
          "Alta",
          "Média",
          "Alta",
          "Baixa",
          "Média",
          "Baixa",
          "Alta",
          "Média",
          "Baixa",
          "Alta",
          "Média",
          "Alta",
      ],
  }
  return pd.DataFrame(data)


df = carregar_dados()

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.header("🎛️ Parâmetros do Projeto")

orcamento_total = st.sidebar.slider(
    "Orçamento Total Disponível (R$)",
    min_value=5000.0,
    max_value=50000.0,
    value=20000.0,
    step=500.0,
)

categorias_disponiveis = sorted(df["Categoria"].unique().tolist())
categorias_selecionadas = st.sidebar.multiselect(
    "Filtrar por Categoria",
    options=categorias_disponiveis,
    default=categorias_disponiveis,
)

# --- ÁREA PRINCIPAL ---
st.title("📊 Simulador de Custos e Orçamento")
st.markdown(
    "Monitore despesas em tempo real, filtre categorias e avalie a saúde"
    " financeira do seu projeto."
)
st.divider()

# Filtragem do DataFrame
if not categorias_selecionadas:
  df_filtrado = df.iloc[0:0]  # DataFrame vazio caso nada seja selecionado
else:
  df_filtrado = df[df["Categoria"].isin(categorias_selecionadas)]

gasto_filtrado = df_filtrado["Valor (R$)"].sum()
saldo_restante = orcamento_total - gasto_filtrado

# Painel de 3 Métricas
col1, col2, col3 = st.columns(3)
with col1:
  st.metric(label="Orçamento Definido", value=f"R$ {orcamento_total:,.2f}")
with col2:
  st.metric(label="Gasto Filtrado", value=f"R$ {gasto_filtrado:,.2f}")
with col3:
  st.metric(
      label="Saldo Restante",
      value=f"R$ {saldo_restante:,.2f}",
      delta=(
          f"R$ {saldo_restante:,.2f}"
          if saldo_restante >= 0
          else f"-R$ {abs(saldo_restante):,.2f}"
      ),
      delta_normal="normal" if saldo_restante >= 0 else "inverse",
  )

# Alerta Visual Condicional
if gasto_filtrado <= orcamento_total:
  st.success(
      "✅ **Meta Atingida!** O gasto atual está dentro do orçamento previsto"
      " para as categorias selecionadas."
  )
else:
  excesso = gasto_filtrado - orcamento_total
  st.error(
      f"⚠️ **Atenção!** O orçamento foi ultrapassado em R$ {excesso:,.2f} com"
      " base nos filtros aplicados."
  )

st.divider()

# Gráfico e Tabela Lado a Lado
col_chart, col_table = st.columns(2)

with col_chart:
  st.subheader("📈 Gastos por Categoria")
  if not df_filtrado.empty:
    # Agrupamento para o gráfico nativo de barras do Streamlit
    df_grouped = df_filtrado.groupby("Categoria")["Valor (R$)"].sum()
    st.bar_chart(df_grouped)
  else:
    st.info("Selecione pelo menos uma categoria para exibir o gráfico.")

with col_table:
  st.subheader("📋 Detalhamento dos Itens")
  st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
    
