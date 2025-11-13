# 📊 Dashboard de Vendas - AdventureWorks

Dashboard interativo para análise de dados de vendas da AdventureWorks, desenvolvido como parte de um projeto de SQL e Python. A aplicação permite filtrar e visualizar dados de vendas por período, localização e produto.

**Autor:** Fernando Papa Ribeiro

---

## 🚀 Visão Geral do Projeto

O projeto consiste em três etapas principais:
1.  **Extração de Dados:** Uma consulta SQL otimizada extrai e agrega dados de vendas do banco de dados AdventureWorks no SQL Server.
2.  **Processamento e Análise:** A biblioteca Pandas é utilizada para carregar, tratar e filtrar os dados.
3.  **Visualização Interativa:** Um dashboard web criado com Streamlit apresenta os dados através de KPIs e gráficos interativos gerados com Plotly.

---

## 🛠️ Tecnologias Utilizadas

*   **Linguagem:** Python 3.9+
*   **Banco de Dados:** Microsoft SQL Server (usando o banco de dados de exemplo `AdventureWorks2022`)
*   **Bibliotecas Python:**
    *   `streamlit`
    *   `pandas`
    *   `plotly-express`
    *   `sqlalchemy`
    *   `pyodbc`

---

## 📋 Pré-requisitos

Antes de começar, garanta que você tem os seguintes pré-requisitos instalados e configurados:

1.  **Python 3.9 ou superior.**
2.  **Microsoft SQL Server** com o banco de dados de exemplo **AdventureWorks2022** restaurado e acessível.
3.  **Microsoft ODBC Driver for SQL Server** instalado no seu sistema operacional. Você pode baixá-lo [aqui](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server ).

---

## ⚙️ Instruções para Rodar o Projeto

Siga os passos abaixo para configurar e executar o projeto localmente.

### 1. Clone o Repositório

Abra um terminal e clone este repositório para a sua máquina:
```bash
git clone https://github.com/fernandopaparibeiro/dashboard-vendas-adventureworks.git
cd dashboard-vendas-adventureworks
```

### 2. Crie um Ambiente Virtual (Recomendado )

É uma boa prática isolar as dependências do projeto.
```bash
# Cria o ambiente virtual
python -m venv venv

# Ativa o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate
```

### 3. Instale as Dependências

Instale todas as bibliotecas necessárias usando o arquivo `requirements.txt`.
```bash
pip install -r requirements.txt
```

### 4. Configure a Conexão com o Banco de Dados

Abra o arquivo `dashboard.py` e **edite as credenciais de conexão** para que correspondam à sua configuração do SQL Server:

```python
# dashboard.py

# --- Detalhes da Conexão com o SQL Server ---
DB_SERVER = 'SEU_SERVIDOR'  # Ex: 'localhost' ou 'NOME_DA_INSTANCIA'
DB_DATABASE = 'AdventureWorks2022'
DB_USERNAME = 'SEU_USUARIO' # Ex: 'sa'
DB_PASSWORD = 'SUA_SENHA'
```

### 5. Execute a Aplicação

Com o ambiente virtual ativado e as dependências instaladas, execute o seguinte comando no terminal:

```bash
streamlit run dashboard.py
```

A aplicação será aberta automaticamente no seu navegador padrão.
