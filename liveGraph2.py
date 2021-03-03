
import plotly.graph_objects as go # or plotly.express as px
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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

group_names = ['Battery Cells', 'Drive Stats', 'Saftey Systems']
group_dropdown = html.Div([
    dcc.Dropdown(
        id='group_dropdown',
        options=[{'label': x, 'value': x} for x in group_names],
        value=group_names[1]
    )])
figures_container = html.Div(id='figures_container')


app.layout = html.Div(
    html.Div([
        html.H4('SEM Dashboard'),
        group_dropdown,
        figures_container,
        dcc.Interval(
            id='interval-component',
            interval=1000, # in milliseconds
            n_intervals=0
        )
    ])
)

dropdown_selected = ""

time_list = []
speed_list = []
voltage_list = []
temperature_list = []
HORIZON = 10

# @app.callback()
# def update_output(group_name):
#     global dropdown_selected
#     dropdown_selected = group_name
#     return


# Multiple components can update everytime interval gets fired.
@app.callback(Output('figures_container', 'children'),
              Input('interval-component', 'n_intervals'),
              Input('group_dropdown', 'value'))
def update_graph_live(n, dropdown_value):

    global time_list
    global speed_list
    global voltage_list
    global temperature_list

    if len(time_list) > HORIZON:
        time_list = time_list[1:]
        speed_list = speed_list[1:]
        voltage_list = voltage_list[1:]
        temperature_list = temperature_list[1:]

    rpm = serialSim.generateRandomRPM()
    speed_list.append(rpm)

    v = serialSim.generateRandomCellVoltage()
    voltage_list.append(v)

    t = serialSim.generateRandomTemperature()
    temperature_list.append(t)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S:%f")
    time_list.append(current_time)

    data = {
        'time': time_list,
        'speed': speed_list,
        'voltage_list': voltage_list,
        'temperature_list': temperature_list
    }

    df = pd.DataFrame(data)

    num_graphs = name_to_figures(dropdown_value)

    figs = []
    ylims = [
        dict(range= [0, serialSim.MAX_RPM]),
        dict(range= [serialSim.CELL_MIN_VOLATGE, serialSim.CELL_MAX_VOLTAGE]),
        dict(range= [serialSim.BATT_TMP_MIN, serialSim.BATT_TMP_MAX])
    ]
    for i in range(num_graphs):
        columns = list(data.keys())
        columns = columns[1:]

        figi = px.line(df, x='time', y=columns[i])
        figi.update_layout(yaxis = ylims[i])
        figi.update_xaxes(tickvals=time_list)
        figs.append(dcc.Graph(figure=figi))    
    # # Create the graph with subplots
    # fig = px.line(df, x='time', y='speed')
    # fig.update_layout(yaxis = )
    # fig.update_xaxes(tickvals=time_list)    

    # f2 = px.line(df, x='time', y='voltage_list')
    # f2.update_layout(yaxis = )
    # f2.update_xaxes(tickvals=time_list)

    # f3 = px.line(df, x='time', y='temperature_list')
    # f3.update_layout(yaxis = )
    # f3.update_xaxes(tickvals=time_list)


    return figs

def name_to_figures(group_name):
    if group_name == group_names[0]:
        return 1
    elif group_name == group_names[1]:
        return 2
    elif group_name == group_names[2]:
        return 3


    # figure = go.Figure()
    # if fig_name == 'fig1':
    #     figure.add_trace(go.Scatter(y=[4, 2, 1]))
    # elif fig_name == 'fig2': 
    #     figure.add_trace(go.Bar(y=[2, 1, 3]))
    # return dcc.Graph(figure=figure)

app.run_server(debug=True, use_reloader=False)