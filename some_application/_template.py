# type hint
from dash.development.base_component import Component

# application
from dash import Dash
import webbrowser

# callback
from dash import Output, Input, State, no_update, callback_context
from dash.exceptions import PreventUpdate

# components
from my_components import html, dbc, dcc

# graph
import pandas as pd
import plotly.express as px


# ===== contents =====
df = pd.DataFrame(dict(
    x=[0, 1, 2, 3],
    y=[0, 1, 4, 9],
))
fig = px.scatter(df)


# ===== components =====
dummy = html.Div(id=(ID_DUMMY := 'dummy'))
graph = dcc.Graph(id=(ID_MAIN_GRAPH := 'main-graph'), figure=fig)
data = dcc.Store(id=(ID_MAIN_DATA := 'main-data'), data=df.to_json(date_format='iso', orient='split'))
interval = dcc.Interval(id=(ID_INTERVAL := 'interval'), interval=1000)


# ===== layout =====
layout: Component = html.Div(
    [
        html.Div([dummy, data, interval]),
        html.Div([
            dbc.Container(dbc.Row(dbc.Col(graph))),
        ]),
    ],
)


# ===== main app =====
app = Dash(__name__)


# ===== callback =====
# noinspection PyUnresolvedReferences
@app.callback(
    Output(graph.id, graph.Prop.figure),
    Output(interval.id, interval.Prop.disabled),
    Input(dummy.id, dummy.Prop.children),
    Input(interval.id, interval.Prop.n_intervals),
    State(data.id, data.Prop.data),
)
def add_callback(
        dummy_children,
        n_intervals,
        df_json,
):
    ret = {
        (graph_figure := 1): no_update,
        (disable_interval := 2): no_update,
    }

    print(callback_context.triggered_id)  # None
    print(callback_context.inputs)  # {'dummy.children': None, 'interval.n_intervals': None}
    print(callback_context.states)  # {'main-data.data': '{"columns":["x","y"],"index":[0,1,2,3],"data":[[0,0],[1,1],[2,4],[3,9]]}'}
    print(callback_context.outputs_list)      # [{'id': 'main-graph', 'property': 'figure'}, {'id': 'interval', 'property': 'disabled'}]
    print(callback_context.outputs_grouping)  # [{'id': 'main-graph', 'property': 'figure'}, {'id': 'interval', 'property': 'disabled'}]

    if callback_context.triggered_id is None:
        raise PreventUpdate

    ret[disable_interval] = True

    return tuple(ret.values())


def main():
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.layout = layout
    webbrowser.open('http://localhost:8050')
    app.run(debug=False)


def debug():
    app.layout = layout
    webbrowser.open('http://localhost:8050')
    app.run(debug=True)


if __name__ == '__main__':
    debug()
