import openai
import yfinance as yf
import time
import pandas as pd
import plotly.graph_objs as go

# Configuração da API da OpenAI
openai.api_key = 'sua-api-key-aqui'

# Cache para armazenar dados temporariamente
cache = {}

# Dicionário com nomes completos dos índices
index_names = {
    '^GSPC': 'S&P 500',
    '^DJI': 'Dow Jones Industrial',
    '^IXIC': 'Nasdaq Composite',
    '^RUI': 'Russell 1000',
    '^RUA': 'Russell 3000',
    '^FTSE': 'FTSE 100',
    '^GDAXI': 'DAX',
    '^FCHI': 'CAC 40',
    '^N225': 'Nikkei 225',
    '000001.SS': 'Shanghai Composite',
    '^HSI': 'Hang Seng',
    '^BSESN': 'Sensex',
    'ME00000000': 'Merval',
    '^BVSP': 'Ibovespa'
}

# Lista de índices a serem monitorados
indexes = ['^GSPC', '^DJI', '^IXIC', '^RUI', '^RUA', '^FTSE', '^GDAXI', '^FCHI', '^N225', '000001.SS', '^HSI', '^BSESN', 'ME00000000', '^BVSP']

# Função para monitorar e logar o tempo de resposta
def log_request_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Request to {func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

# Função para obter dados de um índice usando yfinance com cache
@log_request_time
def get_index_data(index, period="1d"):
    if index in cache:
        return cache[index]
    try:
        data = yf.download(index, period=period, interval="5m")
        cache[index] = data
        return data
    except KeyError:
        print(f"Erro ao baixar dados para {index}")
        return pd.DataFrame()

# Função para gerar o valor atual e variação percentual
@log_request_time
def get_index_info(index):
    data = get_index_data(index)
    if len(data) > 1:
        last_close = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2]
        percent_change = (last_close - prev_close) / prev_close * 100
        return last_close, percent_change, data
    return None, None, pd.DataFrame()

# Função para obter dados de uma ação usando yfinance com cache e tratamento de erro
def get_stock_data(symbol, period="5d"):
    if symbol in cache:
        return cache[symbol]
    try:
        data = yf.download(symbol, period=period)
        if data.empty:
            raise KeyError(f"No data found for symbol: {symbol}")
        cache[symbol] = data
        return data
    except KeyError as e:
        print(f"Erro ao baixar dados para {symbol}: {e}")
        return pd.DataFrame()

# Função para buscar as ações mais populares
def get_popular_stocks():
    return ['AAPL', 'AMZN', 'TSLA', 'GOOGL', 'MSFT']

# Função para obter variação percentual de uma ação
def get_stock_variation(symbol):
    data = get_stock_data(symbol)
    if len(data) > 1:
        last_close = data['Close'].iloc[-1]
        prev_close = data['Close'].iloc[-2]
        percent_change = (last_close - prev_close) / prev_close * 100
        return last_close, percent_change
    return None, None

# Função para gerar o gráfico de um índice
@log_request_time
def create_graph(index):
    data = get_index_data(index)
    if 'Close' in data.columns:
        return {
            'data': [go.Scatter(x=data.index, y=data['Close'], mode='lines', name=index)],
            'layout': go.Layout(
                title=f'Histórico de {index}',
                xaxis={'title': 'Data'},
                yaxis={'title': 'Preço de Fechamento'},
                plot_bgcolor='#1f1f2e',
                paper_bgcolor='#1f1f2e',
                font={'color': '#FFFFFF'},
            )
        }
    else:
        return {
            'data': [],
            'layout': go.Layout(
                title=f'No data available for {index}',
                plot_bgcolor='#1f1f2e',
                paper_bgcolor='#1f1f2e',
                font={'color': '#FFFFFF'},
            )
        }

