import dash
# import dash_core_components as dcc
from dash import dcc 
#import dash_core_components as dcc
# import dash_html_components as html
from dash import html
from dash.dependencies import Input, Output
# from stockstats import StockDataFrame as Sdf
import dash_bootstrap_components as dbc
# import dash_table as dt
from dash import Dash, dcc, html, dash_table
# import yahoo_fin.stock_info as yf
import plotly.graph_objs as go
# from datetime import datetime, timedelta
# import pickle
# import random
# import copy
import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings('ignore')


# defining style color
colors = {"background": "#0b1b49", "text": "#ffFFFF"}

external_stylesheets = [dbc.themes.SLATE]

df = pd.read_csv("final_df.csv")
df_grouped_by_source = df.groupby('source')['page_views','visit_time'].sum().sort_values(ascending=False,by=['page_views','visit_time']).reset_index()
df_grouped_by_source.rename(columns={'source':'Source','page_views':'Page Views','visit_time':'Visit Time'},inplace=True)
df_grouped_by_article_id = df.groupby('article_id')['page_views','visit_time'].sum().sort_values(ascending=False,by=['page_views','visit_time']).reset_index()
df_grouped_by_article_id.rename(columns={'article_id':'Article Title','page_views':'Page Views','visit_time':'Visit Time'},inplace=True)
df_live = df.groupby('minute')['page_views'].sum().reset_index()
df_live_copy = df_live[df_live['minute']<'2022-05-20 16:59:40']
df_live = df_live[df_live['minute']>'2022-05-20 16:59:40']
# df_live_copy['page_views'] = df_live['page_views']-(np.random.randint(0,200))
total_page_views = f'{df.page_views.sum():,}'
total_visit_times = f'{df.visit_time.sum():,}'
tabs_style = {"top":"50%","left":"50%","color":"#0b1b49","backgroundColor": "#0b1b49",'margin': " 0% 0% "}


def generate_table(dataframe, max_rows=50):
    return dash_table.DataTable(
            data=dataframe.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in dataframe.columns],
            sort_action='native',
            page_size=10,  # we have less data in this example, so setting to 20
             style_cell_conditional=[
                    {
                        'if': {'column_id': c},
                        'textAlign': 'left'
                    } for c in ['Article Title', 'Page Views','Visit Time','Source']
                ],
                style_data={
                    'color': 'black',
                    'backgroundColor': 'white',
                    'border': '1px solid #0b1b49',
                    'height':'100%'
                },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(220, 220, 220)',
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'border': '1px solid #0b1b49'
                }
        )

def table_type(df_column):
    if df_column == 'Page Views' or df_column == 'Visit Time':
        return 'numeric'
    else :
        return 'text'
# adding css
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div(
    style={"backgroundColor": colors["background"]},
    children=[
        html.Br(),
        html.Div(
            [  # header Div
                dbc.Row(
                    [
                        dbc.Col(
                            html.Header(
                                [
                                    html.H2(total_visit_times, style={
                                            "textAlign": "center",
                                            "color": colors["text"],
                                        },),
                                    html.P("Total Visit Times", style={
                                            "textAlign": "center",
                                            "color": colors["text"],
                                        },),
                                ]
                            )
                        ),
                          dbc.Col(
                            html.Header(
                                [
                                    html.H2(total_page_views, style={
                                            "textAlign": "center",
                                            "color": colors["text"],
                                        },),
                                    html.P("Total Page Views", style={
                                            "textAlign": "center",
                                            "color": colors["text"],
                                        },),
                                ]
                            )
                        ),
                        dbc.Col(  # button
                            dbc.Button(
                                # "Plot",
                                id="submit-button-state",
                                className="mr-1",
                                n_clicks=1,
                                style = dict(display='none')
                            ),
                            width={"size": 2},
                        ),
                    ]
                )
            ]
        ),
        html.Br(),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id="live price",
                                # config={
                                #     "displaylogo": False,
                                #     "modeBarButtonsToRemove": ["pan2d", "lasso2d"],
                                # },
                            )
                        )
                    ]
                ),
             
            ]
        ),
        html.Br(),
        dcc.Tabs([
                dcc.Tab(label='By Articles', children=[
                    dash_table.DataTable(
                        data=df_grouped_by_article_id.to_dict('records'),
                        columns=[{'id': c,'type':table_type(c), 'name': c} for c in df_grouped_by_article_id.columns],
                        sort_action='native',
                        filter_action='native',
                        page_size=15,  # we hav  # we have less data in this example, so setting to 20
                        style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Article Title', 'Page Views','Visit Time','Source']
                            ],
                            style_data={
                                'color': 'black',
                                'backgroundColor': 'white',
                                'border': '1px solid #0b1b49',
                                'height':'100%'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(220, 220, 220)',
                                }
                            ],
                            style_header={
                                'backgroundColor': 'rgb(210, 210, 210)',
                                'color': 'black',
                                'border': '1px solid #0b1b49'
                            },
                            virtualization=True,
                            page_action='none',
                     

                    )
                ]),
                dcc.Tab(label='By Source', children=[
                    dash_table.DataTable(
                        data=df_grouped_by_source.to_dict('records'),
                        columns=[{'id': c,'type':table_type(c), 'name': c} for c in df_grouped_by_source.columns],
                        sort_action='native',
                        filter_action='native',
                        page_size=15,  # we hav
                        style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Article Title', 'Page Views','Visit Time','Source']
                            ],
                            style_data={
                                'color': 'black',
                                'backgroundColor': 'white',
                                'border': '1px solid #0b1b49',
                                'height':'100%'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(220, 220, 220)',
                                }
                            ],
                            style_header={
                                'backgroundColor': 'rgb(210, 210, 210)',
                                'color': 'black',
                                'border': '1px solid #0b1b49'
                            },
                            virtualization=True,
                            page_action='none',
                            # fixed_rows={ 'headers': True, 'data': 0 },
                            # style_cell={
                            #     'whiteSpace': 'normal'
                            # },
                    )
                ]),
                dcc.Tab(label='By Category', children=[
                   dash_table.DataTable(
                        data=df_grouped_by_source.to_dict('records'),
                        columns=[{'id': c,'type':table_type(c), 'name': c} for c in df_grouped_by_source.columns],
                        sort_action='native',
                        filter_action='native',
                        page_size=15,  # we have less data in this example, so setting to 20
                        style_cell_conditional=[
                                {
                                    'if': {'column_id': c},
                                    'textAlign': 'left'
                                } for c in ['Article Title', 'Page Views','Visit Time','Source']
                            ],
                            style_data={
                                'color': 'black',
                                'backgroundColor': 'white',
                                'border': '1px solid #0b1b49',
                                'height':'100%'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(220, 220, 220)',
                                }
                            ],
                            style_header={
                                'backgroundColor': 'rgb(210, 210, 210)',
                                'color': 'black',
                                'border': '1px solid #0b1b49'
                            },
                            virtualization=True,
                            page_action='none',
                    )
                ]),
            ],style = tabs_style)
        ,html.Br(),
        html.Div(),
        html.Br(),
    ],
)

@app.callback(
    # output
    [Output("live price", "figure")],[Input("submit-button-state", "n_clicks")],

)
def graph_genrator(n_clicks):
    
            fig = go.Figure(
                data=[
                        go.Scatter(x=pd.to_datetime(df_live['minute']), y=df_live['page_views'], mode='lines',
                                                    line=dict(width=0.5, color='#2B547E'),
                                                    stackgroup='one'),
                        go.Scatter(x=pd.to_datetime(df_live_copy['minute']), y=df_live_copy['page_views'],line=dict(width=0.5, color='#728FCE'),
                                                    stackgroup='one')
                ],
                layout={
                    "showlegend": False,
                    "plot_bgcolor": colors["background"],
                    "paper_bgcolor": colors["background"],
                    "font": {"color": colors["text"]},
                },
            )
            fig.update_layout(hovermode='x unified')
            fig.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
            )
            fig.update_layout(xaxis={'visible': False, 'showticklabels': False},yaxis={'visible': False, 'showticklabels': False})
            fig.update_layout(
                xaxis=dict(rangeselector=dict(buttons=list([
                        dict(count=14,label="10M",step="minute",stepmode="todate"),
                        dict(count=1,label="1H",step="hour",stepmode="backward"),
                        dict(count=3,label="1D",step="day",stepmode="backward"),
                        # dict(count=1,label="YTD",step="year",stepmode="todate"),
                        dict(step="all") 
                        ])),type="date"))
            fig.update_xaxes(
                rangeslider_visible=False,
                range=[pd.to_datetime(df_live.minute).min(), pd.to_datetime(df_live.minute).max()],                
                rangeslider_range=[pd.to_datetime(df_live.minute).min(), pd.to_datetime(df_live.minute).max()]
            )
            fig.update_layout(
                            xaxis_rangeselector_font_color=colors["text"],
                            xaxis_rangeselector_activecolor='red',
                            xaxis_rangeselector_bgcolor=colors["background"],
                            )
         
            return [fig]

if __name__ == '__main__':
    app.run_server(debug=True)