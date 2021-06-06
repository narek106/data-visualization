import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

df = pd.read_csv('Life Expectancy Data.csv')
df.columns = [i.strip() for i in df.columns]

df_world = df.copy()
excluded = ['Country', 'Year', "Status", "Population"]
for col in df_world.columns:
    if col not in excluded:
        df_world[col] = df_world[col]*df_world['Population']
        
df_world = df_world.groupby('Year').sum()
for col in df_world.columns:
    if col not in excluded:
        df_world[col] = df_world[col]/df_world['Population']
df_world['Year'] = df_world.index
df_world['Country'] = "All"

years = sorted(list(df.Year.unique())) + ["All"]
num_features = list(df.select_dtypes(include='number').columns[1:])

years = [{'label': i, 'value': i} for i in years]
num_features = [{'label': i, 'value': i} for i in num_features]
countries = [{'label': i, 'value': i} for i in df.Country.unique()]
countries_with_all = [{'label': i, 'value': i} for i in df.Country.unique()]
countries_with_all.insert(0, {'label': "All", 'value': "All"})


corr_matrix = df.corr()
figure = px.imshow(np.abs(corr_matrix), 
    title='Correlation Heatmap')

app = dash.Dash(external_stylesheets = external_stylesheets)

app.layout = html.Div([
            html.Div([html.H1('Life Expectancy Data Analisys')], className = 'row'),

            html.Div([dcc.Dropdown(id = 'years_input',
                                    options = years, 
                                    value = years[0]['value'], 
                                    className='six columns'),
                        dcc.Dropdown(id = 'features_input',
                                    options = num_features, 
                                    value = num_features[0]['value'], 
                                    className='six columns')],
                    className = 'twelve columns'),
             html.Div([
                   html.Div([dcc.Graph(id='Fig1')], className = 'twelve columns'),
            ], className = 'row'),

            html.Div([dcc.Dropdown(id = 'features1_input',
                                    options = num_features, 
                                    value = num_features[0]['value'], 
                                    className='six columns')],
                    className = 'twelve columns'),
             html.Div([
                   html.Div([dcc.Graph(id='Fig2')], className = 'twelve columns'),
            ], className = 'row'),

            html.Div([
                   html.Div([dcc.Graph(figure=figure)], className = 'twelve columns'),
            ], className = 'row'),

            html.Div([dcc.Dropdown(id = 'country1_inp',
                                    options = countries, 
                                    value = countries[0]['value'], 
                                    className='four columns'),
                        dcc.Dropdown(id = 'country2_inp',
                                    options = countries_with_all, 
                                    value = countries_with_all[0]['value'], 
                                    className='four columns'),
                        dcc.Dropdown(id = 'features2_input',
                                    options = num_features, 
                                    value = num_features[0]['value'], 
                                    className='four columns')],
                    className = 'twelve columns'),
             html.Div([
                   html.Div([dcc.Graph(id='Fig3')], className = 'twelve columns'),
            ], className = 'row'),

            html.Div([dcc.Dropdown(id = 'features3_input',
                                    options = num_features, 
                                    value = num_features[0]['value'], 
                                    className='six columns'),
                        dcc.Dropdown(id = 'features4_input',
                                    options = num_features, 
                                    value = num_features[1]['value'], 
                                    className='six columns')],
                    className = 'twelve columns'),
             html.Div([
                   html.Div([dcc.Graph(id='Fig4')], className = 'twelve columns'),
            ], className = 'row'),

            html.Div([dcc.Dropdown(id = 'features5_input',
                                    options = num_features, 
                                    value = num_features[0]['value'], 
                                    className='six columns')],
                    className = 'twelve columns'),
             html.Div([
                   html.Div([dcc.Graph(id='Fig5')], className = 'twelve columns'),
            ], className = 'row')

             ], className = 'container')


@app.callback(
       Output(component_id = 'Fig1', component_property = 'figure'),
       
        [Input(component_id = 'years_input', component_property = 'value'),
         Input(component_id = 'features_input', component_property = 'value')]         
)
def update_hist(year, feat):
    if(year != 'All'):
        part_df = df[df['Year'] == int(year)]
        title = 'Histogram of {} in year {}'.format(feat, year)
    else:
        part_df = df
        title = 'Histogram of {} on all years'.format(feat)
    figure = px.histogram(part_df, x=feat, title=title, nbins=20)
    return figure



@app.callback(
       Output(component_id = 'Fig2', component_property = 'figure'),
        [Input(component_id = 'features1_input', component_property = 'value')]         
)
def update_hist_animation(feat):
    title = 'Animated histogram for {}'.format(feat)
    rev_df = df.reindex(index=df.index[::-1])
    figure = px.histogram(rev_df, x=feat, title=title, animation_frame='Year')
    return figure



@app.callback(
       Output(component_id = 'Fig3', component_property = 'figure'),
       
        [Input(component_id = 'country1_inp', component_property = 'value'),
         Input(component_id = 'country2_inp', component_property = 'value'),
         Input(component_id = 'features2_input', component_property = 'value')]         
)
def update_bar_chart(country1, country2, feat):
    if country2 == "All":
        df1 = df.drop("Status", axis=1)
        df1 = df1[df1['Country'] == country1]
        part_df = pd.concat([df1, df_world])
        title = "Barchart comparison {} and other word with {}".format(country1, feat)
    else:
        part_df = df.loc[(df['Country'] == country1) | (df['Country'] == country2)]
        title = "Barchart comparison {} and {} with {}".format(country1, country2, feat)

    figure = px.bar(part_df, x='Year', y=feat, color='Country', barmode='group', title=title)
    return figure


@app.callback(
       Output(component_id = 'Fig4', component_property = 'figure'),
        [Input(component_id = 'features3_input', component_property = 'value'),
         Input(component_id = 'features4_input', component_property = 'value')]         
)
def update_scatter(feat1, feat2):
    title = "Scatter plot {} and {} colored by status".format(feat1, feat2)
    figure = px.scatter(df, x=feat1, y=feat2, color="Status", title=title)
    return figure

@app.callback(
       Output(component_id = 'Fig5', component_property = 'figure'),
        [Input(component_id = 'features5_input', component_property = 'value')]         
)
def update_stacked_histogram(feat):
    title = "Stacked histogram for {} colored by status".format(feat)
    figure = px.histogram(df, x=feat, color="Status", barmode='overlay', title=title)
    return figure

if __name__ == '__main__':
    app.run_server(debug = True)