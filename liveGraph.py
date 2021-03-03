from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.express as px
from dash.dependencies import Input, Output
import serialSim
import pandas as pd
import time

# pip install pyorbital
# from pyorbital.orbital import Orbital
# satellite = Orbital('TERRA')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('SEM Dashboard'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Graph(id='live-update-graph2'),
        dcc.Interval(
            id='interval-component',
            interval=1000, # in milliseconds
            n_intervals=0
        )
    ])
)


time_list = []
speed_list = []
voltage_list = []
HORIZON = 10

# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
            Output('live-update-graph2', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    global time_list
    global speed_list
    global voltage_list

    if len(time_list) > HORIZON:
        time_list = time_list[1:]
        speed_list = speed_list[1:]
        voltage_list = voltage_list[1:]

    rpm = serialSim.generateRandomRPM()
    speed_list.append(rpm)

    v = serialSim.generateRandomCellVoltage()
    voltage_list.append(v)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S:%f")
    time_list.append(current_time)

    data = {
        'time': time_list,
        'speed': speed_list,
        'voltage_list': voltage_list
    }

    df = pd.DataFrame(data)

    # Create the graph with subplots
    fig = px.line(df, x='time', y='speed')
    fig.update_layout(yaxis = dict(range= [0, serialSim.MAX_RPM]))
    fig.update_xaxes(tickvals=time_list)

    f2 = px.line(df, x='time', y='voltage_list')
    f2.update_layout(yaxis = dict(range= [serialSim.CELL_MIN_VOLATGE, serialSim.CELL_MAX_VOLTAGE]))
    f2.update_xaxes(tickvals=time_list)

    return fig, f2


# serialSim.startDataGen()


if __name__ == '__main__':
    app.run_server(debug=True) 