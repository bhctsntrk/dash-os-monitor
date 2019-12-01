import datetime

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_daq as daq

from getOsInfo import getCpuTemp, getGpuTemp, getCpuUsage, getMemUsage, getEverything

# Define the app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server
# app.config.suppress_callback_exceptions = True

# Font and background colors associated with each theme
headerColor = {"dark": "#2D3038", "light": "#FFFFFF"}
backgroundColor = {"dark": "#23262E", "light": "#F6F6F7"}
gridColor = {"dark": "#53555B", "light": "#969696"}
textColor = {"dark": "#95969A", "light": "#595959"}
cardColor = {"dark": "#2D3038", "light": "#FFFFFF"}
lightColor = {"dark": "#00ff55", "light": "#45fffd"}
bckLightColor = {"dark": "#072611", "light": "#032b2a"}

theme = "light"

tempDict = {"cpu": [], "gpu": [], 'time': []}

usageDict = {"cpu": [], "mem": [], 'time': []}


def bodyLayoutGen():
    global theme

    bodyLayout = html.Div(id="body", children=[
        html.Div(id="tempSection", style={"backgroundColor": cardColor[theme]}, children=[
            html.H5("System Temprature"),
            dcc.Interval(
                id='tempInterval',
                interval=1*1000,  # in milliseconds
                n_intervals=0
            ),
            html.Div(
                id="tempGraphSection",
                className="seven columns",
                style={"backgroundColor": cardColor[theme]},
                children=[
                    html.Div(
                        id="tempLedDispSection",
                        style={
                            "backgroundColor": backgroundColor[theme],
                            "color": textColor[theme],
                        },
                        children=[
                            daq.LEDDisplay(
                                id="cpuTempLiveLed",
                                label="Cpu Temp",
                                value=0,
                                color=lightColor[theme],
                            ),
                            daq.LEDDisplay(
                                id="gpuTempLiveLed",
                                label="Gpu Temp",
                                value=0,
                                color=lightColor[theme],
                            ),
                        ]
                    ),
                    dcc.Graph(id="tempLiveGraph", style={"width": "100%"}),
                ]
            ),
            html.Div(
                id="tempControlSection",
                className="two columns",
                style={"backgroundColor": backgroundColor[theme]},
                children=[
                    html.Button("Reset Graph",
                                id="tempDataResetButton", n_clicks=0, style={"color": textColor[theme]}),
                    daq.PowerButton(
                        id="tempStopButton",
                        color=lightColor[theme],
                        on=True,
                        size=120,
                    ),
                ]
            )
        ]),
        html.Div(id="usageSection", style={"backgroundColor": cardColor[theme]}, children=[
            html.H5("System Usage"),
            dcc.Interval(
                id='usageInterval',
                interval=5*1000,  # in milliseconds
                n_intervals=0
            ),
            html.Div(
                id="usageGraphSection",
                className="seven columns",
                style={"backgroundColor": cardColor[theme]},
                children=[
                    html.Div(
                        id="usageGaugeDispSection",
                        style={
                            "backgroundColor": backgroundColor[theme],
                            "color": textColor[theme],
                        },
                        children=[
                            daq.Gauge(
                                id='cpuUsageLiveGauge',
                                min=0,
                                value=0,
                                max=100,
                                label="Cpu Usage",
                                color=lightColor[theme],
                            ),
                            daq.Gauge(
                                id='memUsageLiveGauge',
                                min=0,
                                value=0,
                                label="Mem Usage",
                                max=100,
                                color=lightColor[theme],
                            ),
                        ]
                    ),
                    dcc.Graph(id="usageLiveGraph", style={"width": "100%"}),
                ]
            ),
            html.Div(
                id="usageControlSection",
                className="two columns",
                style={"backgroundColor": backgroundColor[theme]},
                children=[
                    html.Button("Reset Graph",
                                id="usageDataResetButton", n_clicks=0, style={"color": textColor[theme]}),
                    daq.PowerButton(
                        id="usageStopButton",
                        color=lightColor[theme],
                        on=True,
                        size=120,
                    ),
                ]
            )
        ])
    ])

    if theme == "dark":
        return daq.DarkThemeProvider(children=bodyLayout)
    if theme == "light":
        return bodyLayout


app.layout = html.Div(
    id="mainPage",
    className="container",
    style={"backgroundColor": backgroundColor[theme]},
    children=[
        html.Div(
            id="header",
            style={
                "backgroundColor": headerColor[theme],
                "color": textColor[theme],
            },
            children=[
                html.Img(
                    src=app.get_asset_url("logo-mini.png"),
                    className="logo three columns",
                ),
                html.H6("Dash System Monitor",
                        className="title six columns"),
                html.Div(
                    className="three columns",
                    style={"float": "left"},
                    children=[
                        daq.ToggleSwitch(
                            id="toggleTheme",
                            label=["Light", "Dark"],
                            style={
                                "margin": "auto",
                                "width": "65%",
                                "color": textColor[theme],
                            },
                            value=False,
                            size=35,
                        )
                    ],
                ),
            ],
        ),
        html.P(id="summary", className="mono retro line-1",
               children=getEverything()),
        html.Div(
            id="bodySection",
            children=bodyLayoutGen(),
            className="flex-display",
            style={"backgroundColor": backgroundColor[theme], "padding": "2%"},
        ),
    ],
)

# ======= Dark/light themes callbacks =======


@app.callback(
    [Output("bodySection", "style"),
     Output("bodySection", "children")],
    [Input("toggleTheme", "value")],
    [State("bodySection", "style")],
)
def page_style(value, style_dict):
    """update the theme of the app"""
    global theme
    if value:
        theme = "dark"
    else:
        theme = "light"

    style_dict["color"] = textColor[theme]
    style_dict["backgroundColor"] = backgroundColor[theme]
    return style_dict, bodyLayoutGen()


@app.callback(
    Output("header", "style"),
    [Input("toggleTheme", "value")],
    [State("header", "style")],
)
def header_style(value, style_dict):
    """update the theme of header"""
    global theme
    if value:
        theme = "dark"
    else:
        theme = "light"

    style_dict["color"] = textColor[theme]
    style_dict["backgroundColor"] = headerColor[theme]
    return style_dict


@app.callback([Output('gpuTempLiveLed', 'value'),
               Output('cpuTempLiveLed', 'value')],
              [Input('tempInterval', 'n_intervals')],
              [State('tempStopButton', 'on')])
def getTempData(n, stop):
    if not stop:
        return 0, 0

    cpuTemp = getCpuTemp()
    tempDict["cpu"].append(cpuTemp)

    gpuTemp = getGpuTemp()
    tempDict["gpu"].append(gpuTemp)

    time = datetime.datetime.now()
    tempDict["time"].append(time)

    return gpuTemp, cpuTemp


@app.callback(Output('tempDataResetButton', 'n_clicks_timestamp'),
              [Input('tempDataResetButton', 'n_clicks')])
def resetTempData(n_clicks):
    if n_clicks == 0 or n_clicks is None:
        PreventUpdate()

    global tempDict
    tempDict = {"cpu": [], "gpu": [], 'time': []}
    return 0


@app.callback(Output('tempLiveGraph', 'figure'),
              [Input('tempInterval', 'n_intervals')])
def updateTempLiveGraph(n):
    data = [
        {
            'x': tempDict['time'],
            'y': tempDict['cpu'],
            'name': 'Cpu temp',
            'mode': 'lines',
            'type': 'scatter'
        },
        {
            'x': tempDict['time'],
            'y': tempDict['gpu'],
            'name': 'Gpu Temp',
            'mode': 'lines',
            'type': 'scatter'
        }
    ]
    figure = {
        "data": data,
        "layout": dict(
            paper_bgcolor=bckLightColor[theme],
            plot_bgcolor=bckLightColor[theme],
            automargin=True,
            font=dict(color=textColor[theme], size=12),
            xaxis={
                "color": lightColor[theme],
                "gridcolor": lightColor[theme],
            },
            yaxis={
                "color": lightColor[theme],
                "gridcolor": lightColor[theme],
            },
        ),
    }

    return figure


@app.callback([Output('memUsageLiveGauge', 'value'),
               Output('cpuUsageLiveGauge', 'value')],
              [Input('usageInterval', 'n_intervals')],
              [State('usageStopButton', 'on')])
def getUsageData(n, stop):
    if not stop:
        return 0, 0

    cpuUsage = getCpuUsage()
    usageDict["cpu"].append(cpuUsage)

    memUsage = getMemUsage()
    usageDict["mem"].append(memUsage)

    time = datetime.datetime.now()
    usageDict["time"].append(time)

    return memUsage, cpuUsage


@app.callback(Output('usageDataResetButton', 'n_clicks_timestamp'),
              [Input('usageDataResetButton', 'n_clicks')])
def resetUsageData(n_clicks):
    if n_clicks == 0 or n_clicks is None:
        PreventUpdate()

    global usageDict
    usageDict = {"cpu": [], "mem": [], 'time': []}
    return 0


@app.callback(Output('usageLiveGraph', 'figure'),
              [Input('usageInterval', 'n_intervals')])
def updateUsageLiveGraph(n):
    data = [
        {
            'x': usageDict['time'],
            'y': usageDict['cpu'],
            'name': 'Cpu usage',
            'mode': 'lines',
            'type': 'scatter'
        },
        {
            'x': usageDict['time'],
            'y': usageDict['mem'],
            'name': 'Mem Usage',
            'mode': 'lines',
            'type': 'scatter'
        }
    ]
    figure = {
        "data": data,
        "layout": dict(
            paper_bgcolor=bckLightColor[theme],
            plot_bgcolor=bckLightColor[theme],
            automargin=True,
            font=dict(color=textColor[theme], size=12),
            xaxis={
                "color": lightColor[theme],
                "gridcolor": lightColor[theme],
            },
            yaxis={
                "color": lightColor[theme],
                "gridcolor": lightColor[theme],
            },
        ),
    }

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
