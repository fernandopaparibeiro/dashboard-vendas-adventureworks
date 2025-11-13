import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, exc # Adicionado 'exc' para tratamento de erro



st.set_page_config(page_title="Dashboard de Vendas - AdventureWorks", layout="wide")

st.markdown(
    "<h1 style='text-align: center;'>📊 Dashboard de Vendas - AdventureWorks</h1>",
    unsafe_allow_html=True
)


DB_SERVER = 'localhost'
DB_DATABASE = 'AdventureWorks2022'
DB_USERNAME = 'sa'
DB_PASSWORD = '938ap404' 


# conectar ao banco e carregar os dados.
# @st.cache_data garante que a consulta SQL seja executada apenas uma vez,
# melhora a performance do dashboard após o primeiro carregamento.
@st.cache_data
def carregar_dados_vendas():
    """
    Conecta ao banco de dados AdventureWorks e executa uma consulta SQL otimizada
    para agregar os dados de vendas por data, local e produto.
    Retorna um DataFrame do Pandas.
    """
    try:
        # String de conexão usando o formato SQLAlchemy para SQL Server com pyodbc.
        connection_string = (
            f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}"
            "?driver=ODBC+Driver+17+for+SQL+Server"
        )
        engine = create_engine(connection_string)

        # A consulta SQL foi projetada para pré-agregar os dados no banco,
        # o que é muito mais eficiente do que carregar dados brutos para o Pandas.
        # Calculamos 'TotalSaleValue' e 'TotalQuantitySold' diretamente aqui.
        query = """
        SELECT
            CAST(soh.OrderDate AS DATE) AS OrderDate,
            cr.Name AS Country,
            sp.Name AS Region,
            p.Name AS ProductName,
            SUM(sod.OrderQty * sod.UnitPrice) AS TotalSaleValue,
            SUM(sod.OrderQty) AS TotalQuantitySold
        FROM
            Sales.SalesOrderHeader AS soh
        JOIN
            Sales.SalesOrderDetail AS sod ON soh.SalesOrderID = sod.SalesOrderID
        JOIN
            Production.Product AS p ON sod.ProductID = p.ProductID
        JOIN
            Person.Address AS a ON soh.ShipToAddressID = a.AddressID
        JOIN
            Person.StateProvince AS sp ON a.StateProvinceID = sp.StateProvinceID
        JOIN
            Person.CountryRegion AS cr ON sp.CountryRegionCode = cr.CountryRegionCode
        GROUP BY
            CAST(soh.OrderDate AS DATE), cr.Name, sp.Name, p.Name
        ORDER BY
            OrderDate;
        """
        df = pd.read_sql(query, engine)
        # a coluna de data para o tipo datetime
        df['OrderDate'] = pd.to_datetime(df['OrderDate'])
        return df

    except exc.SQLAlchemyError as e:
        # Tratamento de erro
        st.error(f"Erro ao conectar ou carregar dados do banco: {e}")
        return pd.DataFrame() # Retorna um DataFrame vazio para evitar que o app quebre.
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")
        return pd.DataFrame()

# Carrega os dados e armazena no DataFrame principal 'df_principal'.
df_principal = carregar_dados_vendas()

# Se o DataFrame estiver vazio (devido a um erro de carregamento), interrompe a execução.
if df_principal.empty:
    st.warning("Não foi possível carregar os dados. Verifique a conexão com o banco e as configurações.")
    st.stop()


# FILTROS(SIDEBAR)

st.sidebar.header("Filtros Interativos")

# --- Filtro de Período ---
st.sidebar.subheader("📅 Período de Análise")
df_principal['Ano'] = df_principal['OrderDate'].dt.year
anos_disponiveis = sorted(df_principal['Ano'].unique())

# Usar um slider
ano_selecionado_inicio, ano_selecionado_fim = st.sidebar.select_slider(
    "Selecione o intervalo de anos:",
    options=anos_disponiveis,
    value=(min(anos_disponiveis), max(anos_disponiveis)) # Define o intervalo completo como padrão
)

st.sidebar.subheader("🌎 Filtros Geográficos e de Produtos")

# Aplica o filtro de ano antes de popular os outros filtros,
# para que as opções (país, região, etc.) reflitam apenas o período selecionado.
df_filtrado_anos = df_principal[
    (df_principal['Ano'] >= ano_selecionado_inicio) & (df_principal['Ano'] <= ano_selecionado_fim)
]

# Filtro de Países
paises_selecionados = st.sidebar.multiselect(
    "País(es)",
    options=sorted(df_filtrado_anos['Country'].unique()),
    default=[] # Começa sem nenhum país selecionado por padrão
)

# Filtro de Regiões (dependente dos países selecionados)
if paises_selecionados:
    # Se um ou mais países foram selecionados, mostra apenas as regiões desses países.
    regioes_disponiveis = df_filtrado_anos[df_filtrado_anos['Country'].isin(paises_selecionados)]['Region'].unique()
else:
    # Se nenhum país foi selecionado, mostra todas as regiões do período.
    regioes_disponiveis = df_filtrado_anos['Region'].unique()

regioes_selecionadas = st.sidebar.multiselect(
    "Região(ões)",
    options=sorted(regioes_disponiveis),
    default=[]
)

# Filtro de Produtos
produtos_selecionados = st.sidebar.multiselect(
    "Produto(s)",
    options=sorted(df_filtrado_anos['ProductName'].unique()),
    default=[]
)


# 4. APLICAÇÃO DOS FILTROS E CÁLCULO DOS KPIs

# Começa com o DataFrame já filtrado por ano.
df_final_filtrado = df_filtrado_anos.copy() # Usar .copy() para evitar SettingWithCopyWarning

# Aplica os filtros adicionais se alguma seleção foi feita.
if paises_selecionados:
    df_final_filtrado = df_final_filtrado[df_final_filtrado['Country'].isin(paises_selecionados)]
if regioes_selecionadas:
    df_final_filtrado = df_final_filtrado[df_final_filtrado['Region'].isin(regioes_selecionadas)]
if produtos_selecionados:
    df_final_filtrado = df_final_filtrado[df_final_filtrado['ProductName'].isin(produtos_selecionados)]

# --- Cálculo dos Indicadores Chave de Performance (KPIs) ---
total_vendas = df_final_filtrado['TotalSaleValue'].sum()
quantidade_vendida = df_final_filtrado['TotalQuantitySold'].sum()

# Calcula o valor médio por item, com cuidado para evitar divisão por zero.
if quantidade_vendida > 0:
    valor_medio_item = total_vendas / quantidade_vendida
else:
    valor_medio_item = 0

# Exibe os KPIs em colunas para uma visualização compacta.
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total de Vendas", f"${total_vendas:,.2f}")
col2.metric("📦 Itens Vendidos", f"{int(quantidade_vendida):,}")
col3.metric("💲 Valor Médio por Item", f"${valor_medio_item:,.2f}")

# Adiciona uma linha divisória para separar os KPIs dos gráficos.
st.markdown("---")


# 5. VISUALIZAÇÕES DE DADOS


st.markdown("<h3 style='text-align: center'>🌍 Panorama de Vendas por País e Região</h3>", unsafe_allow_html=True)

# Verifica se há dados para plotar após a filtragem.
if not df_final_filtrado.empty:
    col_geo1, col_geo2 = st.columns(2)

    with col_geo1:
        st.markdown("#### Vendas por País")
        vendas_pais = df_final_filtrado.groupby('Country', as_index=False)['TotalSaleValue'].sum()
        fig_pais = px.pie(
            vendas_pais, values='TotalSaleValue', names='Country',
            hole=0.4, title="Distribuição Percentual por País"
        )
        st.plotly_chart(fig_pais, use_container_width=True)

    with col_geo2:
        st.markdown("#### Top 10 Regiões com Maiores Vendas")
        vendas_regiao = df_final_filtrado.groupby('Region', as_index=False)['TotalSaleValue'].sum().nlargest(10, 'TotalSaleValue')
        fig_regiao = px.bar(
            vendas_regiao.sort_values('TotalSaleValue'), # Ordena para o gráfico ficar crescente
            x='TotalSaleValue', y='Region', orientation='h',
            text='TotalSaleValue', title="Maiores Vendas por Região"
        )
        fig_regiao.update_traces(texttemplate='%{text:,.2s}', textposition='outside')
        st.plotly_chart(fig_regiao, use_container_width=True)
else:
    st.info("Nenhum dado encontrado para os filtros selecionados. Tente uma seleção diferente.")

st.markdown("---")

# Análise de Produtos e Tempo 
st.markdown("<h3 style='text-align: center'>📈 Análise de Produtos e Evolução Temporal</h3>", unsafe_allow_html=True)

if not df_final_filtrado.empty:
  
    st.markdown("#### Top 10 Produtos Mais Vendidos")
    top_produtos = df_final_filtrado.groupby('ProductName', as_index=False)['TotalSaleValue'].sum().nlargest(10, 'TotalSaleValue')
    fig_produtos = px.bar(
        top_produtos.sort_values('TotalSaleValue'),
        x='TotalSaleValue', y='ProductName', orientation='h',
        text='TotalSaleValue', title="Performance dos Principais Produtos"
    )
    fig_produtos.update_traces(texttemplate='%{text:,.2s}')
    st.plotly_chart(fig_produtos, use_container_width=True)

    st.markdown("#### Evolução das Vendas ao Longo do Tempo")
    nivel_tempo = st.radio("Visualizar por:", ("Diário", "Mensal", "Anual"), horizontal=True, key="nivel_tempo")

    # Cria uma cópia para evitar alterar o dataframe filtrado original
    df_tempo = df_final_filtrado.copy()

    if nivel_tempo == "Diário":
        df_tempo['Periodo'] = df_tempo['OrderDate'].dt.date
    elif nivel_tempo == "Mensal":
        df_tempo['Periodo'] = df_tempo['OrderDate'].dt.to_period('M').astype(str)
    else: # Anual
        df_tempo['Periodo'] = df_tempo['OrderDate'].dt.year

    vendas_periodo = df_tempo.groupby('Periodo', as_index=False)['TotalSaleValue'].sum().sort_values('Periodo')

    fig_tempo = px.line(
        vendas_periodo, x='Periodo', y='TotalSaleValue',
        title=f"Total de Vendas ({nivel_tempo})", markers=True,
        labels={'Periodo': f'Período ({nivel_tempo})', 'TotalSaleValue': 'Total de Vendas ($)'}
    )
    st.plotly_chart(fig_tempo, use_container_width=True)

# --- Fim do Dashboard ---
st.sidebar.markdown("---") # Adiciona uma linha divisória
st.sidebar.info(
    """
    **Autor:** Fernando Luiz Papa Ribeiro\n
    Dashboard para análise de dados de vendas da AdventureWorks.
    """
)