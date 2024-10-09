import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State, ALL
import plotly.graph_objs as go
from utils import get_stock_variation, create_graph, get_index_info, indexes, get_popular_stocks, index_names

def register_callbacks(app):

    @app.callback(
        Output('ticker-tape', 'children'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_ticker_tape(n_intervals):
        popular_stocks = get_popular_stocks()  # Ações populares
        ticker_elements = []

        for stock in popular_stocks:
            last_close, percent_change = get_stock_variation(stock)
            if last_close is not None and percent_change is not None:
                color = '#16a085' if percent_change > 0 else '#e74c3c'
                symbol_display = f"{stock} {last_close:.2f} ({percent_change:.2f}%)"
                ticker_elements.append(html.Span(symbol_display, style={'color': color, 'padding': '0 15px'}))

        return html.Div(ticker_elements, className="ticker-container")

    @app.callback(
        [Output('index-list', 'children'), Output('index-graph', 'figure')],
        [Input('interval-component', 'n_intervals'),
         Input({'type': 'index-item', 'index': ALL}, 'n_clicks')],
        [State({'type': 'index-item', 'index': ALL}, 'id')]
    )
    def update_graph_and_list(n_intervals, n_clicks, ids):
        ctx = dash.callback_context

        # Variáveis para a lista de índices e o gráfico a ser exibido
        index_elements = []
        selected_index = '^GSPC'  # Índice padrão a ser exibido no gráfico
        figure = create_graph(selected_index)  # Gráfico padrão (S&P 500)

        # Se um índice for clicado
        if any(n_clicks):
            clicked_id = [id for id, n_click in zip(ids, n_clicks) if n_click][0]  # Identificar qual índice foi clicado
            selected_index = clicked_id['index']  # Atualizar o índice selecionado
            figure = create_graph(selected_index)  # Atualizar o gráfico com o índice clicado

        # Gerar a lista de índices com mini gráficos e destacar o selecionado
        for index in indexes:
            last_close, percent_change, data = get_index_info(index)
            if last_close is not None and percent_change is not None:
                color = '#16a085' if percent_change > 0 else '#e74c3c'
                index_name = index_names.get(index, index)  # Obter o nome completo do índice

                # Mini gráfico do índice (pequena linha de tendência)
                mini_graph = dcc.Graph(
                    figure={
                        'data': [go.Scatter(x=data.index, y=data['Close'], mode='lines', line=dict(color=color), showlegend=False)],
                        'layout': go.Layout(
                            margin=dict(l=0, r=0, t=0, b=0),
                            height=40,
                            xaxis={'visible': False},
                            yaxis={'visible': False},
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)'
                        )
                    },
                    config={'displayModeBar': False}
                )

                # Adicionar destaque para o índice selecionado
                style = {
                    'padding': '10px',
                    'borderBottom': '1px solid #444',
                    'marginBottom': '10px'
                }
                if index == selected_index:
                    style['backgroundColor'] = '#1f1f2e'

                # Adicionar índice à lista
                index_elements.append(html.Div([
                    html.Div(f"{index_name}", style={'fontWeight': 'bold'}),  # Nome completo do índice
                    html.Div(f"{index}", style={'color': '#888888'}),  # Código do índice
                    html.Div([mini_graph], style={'height': '50px'}),  # Mini gráfico
                    html.Div(f"${last_close:.2f}", style={'fontSize': '18px'}),  # Valor do índice
                    html.Div(f"{percent_change:.2f}%", style={'color': color, 'fontSize': '14px'}),  # Variação percentual
                ], style=style, id={'type': 'index-item', 'index': index}))

        return index_elements, figure
