import dash
import dash_html_components as html
import dash_core_components as dcc
import time

# Local Modules
from parseData import parse


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1(children='Button testing...'),

    # button 1
    html.Button('Refresh', id='button'),
    html.Div(id='container-button-basic',children='submit to grab data'),
    
    # button 2
    html.Button('ShowTable', id='button_2'),
    html.Div(id='container-button-basic_2'),

])


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')])
def update_graph1(n_clicks):
    [x,y] = parse('sample.csv')
    
    plot_1 = html.Div(children=''),dcc.Graph(id ='line graph',
            figure={'data': [ {'x': x,'y': y,'type':'line','name':'csvFile'} ],
            'layout': {'title': 'parsedData'}}),dcc.Graph(id = 'line2',figure={'data': [ {'x': x,'y': y,'type':'line','name':'csvFile'} ],
            'layout': {'title': 'parsedData2'}})

    return plot_1

def update_graph2(n_clicks):
    [x,y] = parse('sample.csv')
    

    plot_2 = html.Div(children='plot 2'),dcc.Graph(id ='line graph1',
            figure={'data': [ {'x': x,'y': y,'type':'line','name':'csvFile1'} ],
            'layout': {'title': 'parsedData1'}})


    return plot_2

@app.callback(
        dash.dependencies.Output('container-button-basic_2', 'children'),
        [dash.dependencies.Input('button_2','n_clicks_timestamp')])
def update_output_2(time_pressed):
    humanTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_pressed))
    return 'this one was pressed at: {} '.format(humanTime)

if __name__ == '__main__':
    app.run_server(debug=True)

