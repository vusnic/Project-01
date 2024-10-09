
import dash
from dash.dependencies import Input, Output, State
from layout import app_layout
from callbacks import register_callbacks

# Iniciar o app Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.layout = app_layout

# Registrar os callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
