#importing the modules
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.offline as pyo

import matplotlib.pyplot as plt
import seaborn as sns


import plotly.graph_objs as go
import pandas as pd
import numpy as np

#loading and cleaning data
balls = pd.read_csv('IPL Ball-by-Ball 2008-2020.csv')
matches = pd.read_csv('IPL Matches 2008-2020.csv')


df = pd.merge(left=matches, right=balls, on='id', how='right')
df['date'] = pd.to_datetime(df['date'])
df['year'] = pd.DatetimeIndex(df['date']).year


# #dashboard layout
app = dash.Dash()

year_options = []
for year in df['year'].unique():
    year_options.append({'label':str(year), 'value':year})
    
team_options = []
for team in df['batting_team'].unique():
    team_options.append({'label':str(team), 'value':team})

app.layout = html.Div([
                        html.Div(
                            [dcc.Dropdown(id='year-picker', options=year_options, value=df['year'].min())], 
                            style={'display':'inline-block', 'width':'30%'}
                            ),
                        html.Div(
                             [dcc.Dropdown(id='team-picker', options=team_options, value='team')],
                             style={'display':'inline-block', 'width':'70%'}
                             ),
                        html.Hr(),
                        html.Div(
                            [dcc.Graph(id='runs_by_year')],
                            style={'display':'inline-block', 'width':'50%'}
                            ),
                        html.Div(
                            [dcc.Graph(id='runs_by_match')],
                            style={'display':'inline-block', 'width':'50%'}
                            ),
                        html.Hr(),
                        html.Div(
                            'Developed by Nitesh Halai.'
                            ),
                        html.Div(
                            'Mobile/Whatsapp: +254 715 977 346.'
                            ),
                        html.Div(
                            'Email: nitesh.dataviz@gmail.com'
                            ),
                        ])
                       


@app.callback(Output('runs_by_match', 'figure'),
              [
               Input('year-picker','value'),
               Input('team-picker','value')
               ])


def update_figure(selected_year, selected_team):
    filtered_df=df[df['year']==selected_year]
    filtered_df=filtered_df[filtered_df['batting_team']==selected_team]
    
    #Runs by match distribution data
    runs_by_match = filtered_df.groupby(by='id').sum()
    runs_by_match = pd.DataFrame(runs_by_match[['total_runs']])
    runs_by_match.reset_index(inplace=True)
    
    #creating a plot to use in the dashboard
    runs_by_match = go.Histogram(
                        x=runs_by_match['total_runs']
                        )
    
    data2 = [runs_by_match]
    
    layout2 = go.Layout(title=selected_team+': IPL year '+str(selected_year)+' runs distribution match wise',
                      xaxis = dict(title='Runs'))
    
    return {'data':data2,'layout':layout2}

@app.callback(Output('runs_by_year', 'figure'),
              [
               Input('team-picker','value')
               ])

def update_figure2(selected_team):
    filtered_df2=df[df['batting_team']==selected_team]
    
    runs_by_years = filtered_df2.groupby(by='year').sum()['total_runs']
    runs_by_years = pd.DataFrame(runs_by_years)
    runs_by_years.reset_index(inplace=True)

    total_runs = go.Scatter(
                    x=runs_by_years['year'],
                    y=runs_by_years['total_runs'],
                    mode='lines',
                    name='runs')

    data3 = [total_runs]
    
    layout3 = go.Layout(title=selected_team+': Runs scored by year',
                      xaxis = dict(title='Year'),
                      yaxis = dict(title='Runs'))
    
    return {'data':data3,'layout':layout3}

    

if __name__ == '__main__':
    app.run_server()