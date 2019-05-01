import dash
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    #html.Div(dcc.Input(id='input-box', type='text')),
    html.Button('Refresh', id='button'),
    html.Div(id='container-button-basic',
             children='submit to grab data')

])


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])
    #[dash.dependencies.State('input-box', 'value')])
def update_output(n_clicks):
    return 'The button has been clicked {} times'.format(
        #value,
        n_clicks
    )


if __name__ == '__main__':
    app.run_server(debug=True)
