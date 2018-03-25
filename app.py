import base64
from io import BytesIO

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objs as go
from PIL import Image
from dash.dependencies import Output, Input

from utils import get_map


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


def build_graph_by_image(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        image = Image.open(BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'Произошла ошибка при обработке файла.'
        ])

    data_new = [    
        go.Surface(
            z=np.matrix(get_map(image))
        )
    ]
    lo.title = filename

    return html.Div([
        dcc.Graph(
            id='graph',
            figure={
                'data': data_new,
                'layout': lo
            }
        )
    ])


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
    html.Div(id='output-data-upload'),
])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_output(contents, filename):
    if contents is not None:
        children = build_graph_by_image(contents, filename)
        return children


if __name__ == '__main__':
    app.run_server(debug=True)
