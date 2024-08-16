import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Hello, Dash!"),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Option 1', 'value': 'option1'},
            {'label': 'Option 2', 'value': 'option2'}
        ],
        value='option1'
    ),
    html.Div(id='output-div')
])

# Define a callback function
@app.callback(
    Output('output-div', 'children'),
    [Input('dropdown', 'value')])
def update_output(value):
    return f'You selected: {value}'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)