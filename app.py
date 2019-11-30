import numpy as np
from textwrap import dedent
import datetime

import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_daq as daq

from getOsInfo import getCpuTemp, getGpuTemp

# Define the app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server
app.config.suppress_callback_exceptions = True

# Font and background colors associated with each theme
banner_color = {"dark": "#23262e", "light": "#ffffff"}
bkg_color = {"dark": "#23262e", "light": "#f6f6f7"}
grid_color = {"dark": "#53555B", "light": "#969696"}
text_color = {"dark": "#95969A", "light": "#595959"}
card_color = {"dark": "#2D3038", "light": "#FFFFFF"}
accent_color = {"dark": "#FFD15F", "light": "#ff9827"}

theme = "light"

app.layout = html.Div(
    html.Div([
        html.H4('OS Monitoring Application'),
        daq.LEDDisplay(
            id="cpuTempLiveLed",
            label="Cpu Temp",
            value=0,
            color=accent_color[theme],
        ),
        daq.LEDDisplay(
            id="gpuTempLiveLed",
            label="Gpu Temp",
            value=0,
            color=accent_color[theme],
        ),
        dcc.Graph(id='tempLiveGraph'),
        dcc.Interval(
            id='intervalCounter',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)

@app.callback(Output('cpuTempLiveLed', 'value'),
              [Input('intervalCounter', 'n_intervals')])
def updateCpuTempLiveLed(n):
    cpuTemp = getCpuTemp()
    return cpuTemp

@app.callback(Output('gpuTempLiveLed', 'value'),
              [Input('intervalCounter', 'n_intervals')])
def updateGpuTempLiveLed(n):
    gpuTemp = getGpuTemp()
    return gpuTemp

# Multiple components can update everytime interval gets fired.
@app.callback(Output('tempLiveLed', 'value'),
              [Input('intervalCounter', 'n_intervals')],
              [State('cpuTempLiveLed', 'value'),
               State('gpuTempLiveLed', 'value')])
def updateTempLiveGraph(n, cpuTemp, gpuTemp):
    data = {
        'cpuTemp': [],
        'gpuTemp': [],
        'time': []
    }

    # Collect some data
    for i in range(180):
        time = datetime.datetime.now() - datetime.timedelta(seconds=i*20)
        cpuTemp = getCpuTemp()
        gpuTemp = getGpuTemp()
        data['cpuTemp'].append(cpuTemp)
        data['gpuTemp'].append(gpuTemp)
        data['time'].append(time)

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': data['time'],
        'y': data['cpuTemp'],
        'name': 'Cpu temp',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['time'],
        'y': data['gpuTemp'],
        'text': data['time'],
        'name': 'Gpu Temp',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)