import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# from app import app

import dash
import plotly.graph_objs as go

from data import df_merged, countries, color_lookup, stats

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=True),
    html.Div(id='page-content')
])

server = app.server

graphcontainer_layout = html.Div([
    html.Div([html.H1("Times Higher Education - World University Rankings")], style={'textAlign': "center"}),
    html.Div([html.Div([dcc.Dropdown(id='country-selected', options=[{"label": i, 'value': i} for i in countries],
                                     value=["France"], multi=True)],
                       style={"display": "block", "width": "60%", "float": "left"}),
              html.Div([dcc.Dropdown(id='col-selected', options=[{"label": i, 'value': v} for v,i in stats.items()],
                                     value='scores_overall', multi=False)],
                       style={"display": "block", "width": "30%", "float": "right"}),
              ],
             style={"height": "40px"},
             className="row"),
    dcc.Graph(id="my-graph")], className="container")


@app.callback(Output('page-content', 'children'),[Input('url', 'pathname')])
def display_page(pathname):
    return graphcontainer_layout


plot_layout = go.Layout(
    autosize=False,
    width=1100,
    height=len(df_merged)*20,
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        side='top'
        # showticklabels = False,
        # domain=[0, 1]
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        autorange='reversed'
        # showticklabels=False
    ),
    # paper_bgcolor='rgb(248, 248, 255)',
    # plot_bgcolor='rgb(248, 248, 255)',
    margin=dict(
        l=400,
        r=10,
        t=50,
        b=80
    ),
    showlegend=False,
)


@app.callback(Output("my-graph", "figure"), [Input("country-selected", "value"), Input("col-selected", "value")])
def update_graph(country_selected, col_selected):
    dropdown = {i:i for i in countries}
    ctx = dash.callback_context
    trace = []
    if len(country_selected)>0:
        df_updated = df_merged.loc[df_merged['location'].isin(country_selected)]
    else:
        df_updated = df_merged
    # for value in selected:
    #     trace.append(go.Bar(x=df_merged[value], y=df_merged.index,
    #                             orientation='h',
    #                             # marker={"opacity": 0.7, 'size': 5, 'line': {'width': 0.5, 'color': 'white'}},
    #                             name=dropdown[value]),
    #                             )
    marker = {
        'color': list(map(lambda loc: color_lookup[loc], df_updated['location'])),
    }
    trace = [go.Bar(x=df_updated[col_selected], y=df_updated.index,
                        orientation='h',
                        name=col_selected,
                        marker=marker)]
    plot_layout['height'] = len(df_updated)*20
    figure = {"data": trace, "layout": plot_layout}
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
