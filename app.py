import base64
import json
from io import BytesIO

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
from PIL import Image
from dash.dependencies import Output, Input
from plotly import tools

from utils import get_map, get_avg_by_x, get_avg_by_y

lo = go.Layout(
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=65,
        r=50,
        b=65,
        t=90
    )
)


my_map = None


def build_map_by_image(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        image = Image.open(BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'Произошла ошибка при обработке файла.'
        ])

    my_map = get_map(image)
    return my_map


def build_flat_graph(x, y, my_map):
    trace1 = go.Scatter(
            x=[i for i in range(0, len(my_map[y]))],
            y=get_avg_by_y(y, 2, my_map),
            line=dict(
                shape='spline'
            )
        )
    trace2 = go.Scatter(
            x=[i for i in range(0, len(my_map))],
            y=get_avg_by_x(x, 2, my_map),
            line=dict(
                shape='spline'
            )
        )
    fig = tools.make_subplots(rows=1, cols=2,
                              subplot_titles=('Вдоль оси x', 'Вдоль оси y'))
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    return dcc.Graph(
        id='flat_graph',
        figure=fig
    )


app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='Построение графика'),

    html.Div(children='''
        Для построение графика загрузите изображение
    '''),
    dcc.Upload(
        id='upload-data',
        accept='image/*',
        children=html.Div([
            'Перетащите изображение сюда или Загрузите вручную',
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }
    ),
    dcc.Graph(
        id='graph'
    ),
    html.Div(
        id='output-flat-graph'
    ),
    html.Div(id='map-value', style={'display': 'none'})
])


@app.callback(Output('map-value', 'children'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_output(contents, filename):
    if contents is not None:
        children = json.dumps(build_map_by_image(contents, filename))
        return children


@app.callback(Output('graph', 'figure'),
              [Input('map-value', 'children')])
def update_output(children):
    if children is not None:
        my_map = json.loads(children)
        return {'data': [go.Surface(z=np.matrix(my_map))], 'layout': lo}
    return {'data': [], 'layout': lo}


@app.callback(Output('output-flat-graph', 'children'),
              [Input('graph', 'clickData'),
               Input('map-value', 'children')])
def draw_flat_graph(clickData, children):
    if clickData:
        fix_x = clickData['points'][0]['x']
        fix_y = clickData['points'][0]['y']
        my_map = json.loads(children)
        return build_flat_graph(x=fix_x, y=fix_y, my_map=my_map)


if __name__ == '__main__':
    app.run_server(debug=True)
