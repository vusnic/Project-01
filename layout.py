import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import random

# Inicializando o app
app = dash.Dash(__name__)

# Layout do app
app.layout = html.Div(style={
    'background': 'linear-gradient(135deg, #1f1f2e, #2c3e50)',
    'font-family': 'Arial'
}, children=[

    # Barra de Pesquisa e Título
    html.Div([
        dcc.Input(id='search-bar', type='text', placeholder='Buscar índice...', style={
            'padding': '10px', 'width': '300px', 'fontSize': '18px', 'border': 'none',
            'border-radius': '4px', 'background-color': '#27293d', 'color': '#FFFFFF'
        }),
        html.H1('Painel de Monitoramento de Índices', style={'textAlign': 'center', 'color': '#FFFFFF'}),
    ], style={'padding': '10px', 'backgroundColor': '#27293d', 'textAlign': 'center'}),

    # Linha de ticker tape
    html.Div(id='ticker-tape', style={
        'overflow': 'hidden', 'whiteSpace': 'nowrap', 'padding': '10px', 'position': 'relative',
        'animation': 'ticker-scroll 30s linear infinite', 'display': 'inline-block', 'width': '100%',
        'color': '#FFFFFF'
    }),

    # Divisão principal em 2 colunas
    html.Div([

        # Coluna 1 - Lista de índices com valor, gráfico e percentual de variação
        html.Div(id='index-list', children=[], style={
            'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top',
            'backgroundColor': '#27293d', 'padding': '20px', 'color': '#FFFFFF',
            'overflowY': 'scroll', 'height': '500px'
        }),

        # Coluna 2 - Gráfico do Índice Selecionado
        html.Div([
            html.H2('Gráfico do Índice Selecionado', style={'color': '#FFFFFF'}),
            dcc.Graph(id='index-graph')
        ], style={'width': '75%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),

    ]),

    dcc.Interval(id='interval-component', interval=5*60*1000, n_intervals=0)  # Atualização a cada 5 minutos
])

# CSS para animação do ticker-tape
app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Dash Finance App</title>
            <style>
                @keyframes ticker-scroll {
                0% { transform: translateX(100%); }
                100% { transform: translateX(-100%); }
                }
                .ticker-container {
                display: inline-block;
                white-space: nowrap;
                animation: ticker-scroll 30s linear infinite;
                }
            </style>
        </head>
        <body>
            <div id="root">
                {%app_entry%}
            </div>
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''

# Callback para atualizar o ticker-tape com informações dinâmicas
@app.callback(
    Output('ticker-tape', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_ticker_tape(n_intervals):
    # Exemplo de dados simulados
    stocks = ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN']
    ticker_elements = []

    for stock in stocks:
        # Simulando valores e variações aleatórias
        last_close = round(random.uniform(100, 1500), 2)
        percent_change = round(random.uniform(-5, 5), 2)
        color = '#16a085' if percent_change > 0 else '#e74c3c'
        symbol_display = f"{stock} {last_close} ({percent_change}%)"
        ticker_elements.append(html.Span(symbol_display, style={'color': color, 'padding': '0 15px'}))

    return html.Div(ticker_elements, className="ticker-container")


# Rodando o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
