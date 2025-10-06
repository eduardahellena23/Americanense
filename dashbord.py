import pandas as pd
import plotly.express as px
import os
import webbrowser

# --- CONFIGURAÇÕES ---
HTML_OUTPUT = 'apresentacao_tributaria.html'
# --------------------

def formatar_br(valor, tipo='moeda'):
    """Formata números para o padrão brasileiro (R$ e %)"""
    if pd.isna(valor):
        return ""
    if tipo == 'moeda':
        # Formata como moeda (separador de milhar ponto, separador decimal vírgula)
        return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    elif tipo == 'porcentagem':
        # Formata como porcentagem
        return f'{valor*100:.2f}%'.replace('.', ',')
    return str(valor)

def generate_static_dashboard():
    # 1. Dados Fixos para a Apresentação (Seus dados da planilha)
    # A Alíquota Efetiva está aqui como Decimal (ex: 0.1129)
    data = {
        'Regime': [
            'Simples Nacional Atual', 
            'Simples Nacional RTC DAS', 
            'Simples Nacional RTC Híbrido', 
            'Lucro Presumido'
        ],
        'Valor_Imposto': [
            15043.17, 
            42058.26, 
            68672.45, 
            103422.83
        ],
        'Aliquota_Efetiva': [
            0.112968, 
            0.1682, 
            0.274635, 
            0.413610
        ]
    }
    df = pd.DataFrame(data)

    # Adicionar coluna para a cor dos gráficos (destaque no menor valor)
    menor_imposto = df['Valor_Imposto'].min()
    df['Destaque'] = df['Valor_Imposto'].apply(lambda x: 'Menor Imposto' if x == menor_imposto else 'Outros Regimes')

    # 2. Criação dos Gráficos Interativos (Plotly)

    # Gráfico 1: Comparativo do Valor Total de Impostos
    fig_valor = px.bar(
        df,
        x='Regime',
        y='Valor_Imposto',
        color='Destaque',
        color_discrete_map={'Menor Imposto': '#28a745', 'Outros Regimes': '#007bff'},
        title='Comparativo do Valor Total de Impostos (R$)',
        text=df['Valor_Imposto'].apply(lambda x: formatar_br(x, 'moeda')),
        template='plotly_white'
    )
    fig_valor.update_traces(textposition='outside')
    fig_valor.update_layout(yaxis_title="Valor do Imposto (R$)", xaxis_title=None, showlegend=False)

    # Gráfico 2: Comparativo da Alíquota Efetiva
    fig_aliquota = px.bar(
        df,
        x='Regime',
        y='Aliquota_Efetiva',
        color='Destaque',
        color_discrete_map={'Menor Imposto': '#28a745', 'Outros Regimes': '#007bff'},
        title='Comparativo da Alíquota Efetiva (%)',
        text=df['Aliquota_Efetiva'].apply(lambda x: formatar_br(x, 'porcentagem')),
        template='plotly_white'
    )
    fig_aliquota.update_traces(textposition='outside')
    fig_aliquota.update_layout(yaxis_title="Alíquota Efetiva", xaxis_title=None, yaxis_tickformat=".2%", showlegend=False)

    # 3. Geração do Arquivo HTML Final (com CSS para layout)

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard Comparativo Tributário - Apresentação</title>
    <meta charset="utf-8">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ font-family: 'Arial', sans-serif; margin: 0; background-color: #f0f2f5; }}
        .header {{ background-color: #007bff; color: white; padding: 25px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        h1 {{ margin: 0; font-size: 2.2em; }}
        .container {{ display: flex; flex-wrap: wrap; justify-content: space-around; padding: 20px; max-width: 1300px; margin: 30px auto; }}
        .card {{ background-color: white; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 15px; padding: 20px; flex: 1 1 45%; min-width: 450px; }}
        h2 {{ color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 0; }}
        p.intro {{ text-align: center; color: #ccf; font-size: 1.1em; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Análise Comparativa de Regimes Tributários</h1>
        <p class="intro">Simulação de Custos: Otimização Tributária</p>
    </div>

    <div class="container">
        <div class="card">
            <h2>💰 Valor Absoluto do Imposto (R$)</h2>
            <p>O custo total em Reais para cada Regime de Tributação simulado.</p>
            {fig_valor.to_html(full_html=False, include_plotlyjs='cdn')}
        </div>
        <div class="card">
            <h2>📈 Alíquota Efetiva (%)</h2>
            <p>A porcentagem real que a empresa paga em impostos sobre a Receita.</p>
            {fig_aliquota.to_html(full_html=False, include_plotlyjs='cdn')}
        </div>
    </div>
</body>
</html>
"""

    # 4. Salvar e Abrir o arquivo
    with open(HTML_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    try:
        abs_path = os.path.abspath(HTML_OUTPUT)
        webbrowser.open('file://' + abs_path, new=2)
    except Exception:
        pass 

    print(f"\n===================================================================================")
    print(f"✅ Dashboard '{HTML_OUTPUT}' gerado com sucesso!")
    print(f"Abra o arquivo '{HTML_OUTPUT}' no seu navegador para ver a apresentação.")
    print(f"===================================================================================\n")


if __name__ == "__main__":
    generate_static_dashboard()
