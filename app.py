import dash
from dash import Dash, html, dcc, callback #adding the component to be able to add the graphs/tables
import plotly.express as px
import pandas as pd

import dash_bootstrap_components as dbc
from dash import dash_table

from dash.dependencies import Input, Output, State


df = pd.read_csv('./final_data3.csv')

col_drop = ['good_avg_sum','good_rain_sum','good_vis_sum','sunscreen_needed_sum']

df.drop(columns=col_drop, inplace=True)

month_mapping = {
    'may': '05_May',
    'june': '06_June',
    'july': '07_July',
    'august': '08_August',
    'september': '09_September',
    'october': '10_October'
}

for month, prefixed_month in month_mapping.items():
    df['month_of_year'] = df['month_of_year'].str.replace(month, prefixed_month)

df.columns = ['City','Country','Month','Days with good temperature','Non-rainy days','Wind','Latitude','Longitude']

df = df.sort_values(by=['City', 'Month'])

df_berlin = df[df['City'] == 'Berlin']
df_berlin = df_berlin.sort_values(by='Month', ignore_index=True)

df_copenhagen = df[df['City'] == 'Copenhagen']
df_copenhagen = df_copenhagen.sort_values(by='Month', ignore_index=True)

df_katowice = df[df['City'] == 'Katowice']
df_katowice = df_katowice.sort_values(by='Month', ignore_index=True)

df_tokyo = df[df['City'] == 'Tokyo']
df_tokyo = df_tokyo.sort_values(by='Month', ignore_index=True)

df_la = df[df['City'] == 'Los Angeles']
df_la = df_la.sort_values(by='Month', ignore_index=True)

color_discrete_map = {'Berlin': '#7FC97F',  # Green
                      'Copenhagen': '#BEAED4',  # Purple
                      'Katowice': '#FDC086',  # Orange
                      'Tokyo': '#FFFF99',  # Yellow
                      'Los Angeles': '#386CB0'}  # Blue

fig1 = px.bar(df, 
             x='Month', 
             y='Days with good temperature',  
             color='City',
             barmode='group',
             height=300, title = "Good temperature for sailing by Month",)

fig1 = fig1.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", 
    #margin=dict(l=20, r=20, t=0, b=20)
)
    

graph1 = dcc.Graph(figure=fig1)

fig2 = px.bar(df, 
             x='Month', 
             y='Non-rainy days',  
             color='City',
             barmode='group',
             height=300, title = "Non-rainy days by Month",)

fig2 = fig2.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", 
    #margin=dict(l=20, r=20, t=0, b=20)
)
    

graph2 = dcc.Graph(figure=fig2)

fig3 = px.bar(df, 
             x='Month', 
             y='Wind',  
             color='City',
             barmode='group',
             height=300, title = "Days with good wind for sailing by Month",)

fig3 = fig3.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white", 
    #margin=dict(l=20, r=20, t=0, b=20)
)
    

graph3 = dcc.Graph(figure=fig3)

fig4 = px.imshow(df.pivot_table(index='City', columns='Month', values='Wind'), 
                x=list(df['Month'].unique()), 
                y=list(df['City'].unique()))

# Update layout
fig4.update_layout(
    title='Good wind for sailing by month and city',
    xaxis=dict(title='Month'),
    yaxis=dict(title='City'),
    plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"  # Background color  # Font color
)

# Show the plot
graph4 = dcc.Graph(figure=fig4)

fig6 = px.scatter_geo(df, lat='Latitude', lon='Longitude', color='Wind',
                      hover_name='City', size='Days with good temperature', projection='natural earth',
                      animation_frame='Month')

fig6.update_geos(showcountries=True, countrycolor="Black", showland=True, landcolor="Black",
                 showocean=True, oceancolor="Black", showlakes=True, lakecolor="Black",
                 showrivers=True, rivercolor="Black")

fig6.update_layout(title='City Metrics by Month',
                   plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white",
                   width=1000, height=600)  # Set width and height here

graph6 = dcc.Graph(figure=fig6)

total_points_df = df.groupby(['City', 'Month'])[['Wind', 'Days with good temperature', 'Non-rainy days']].sum().reset_index()
total_points_df['Total Points'] = total_points_df[['Wind', 'Days with good temperature', 'Non-rainy days']].sum(axis=1)
total_points_df = total_points_df.sort_values(by='Total Points', ascending=False)
total_points_df.head(10)

fig7 = px.bar(
    total_points_df,
    x='Month',
    y='Total Points',
    color='City',
    color_discrete_map=color_discrete_map,
    barmode='group',
    height=400,
    title='Total Points by Month and City'
)

# Update layout
fig7.update_layout(
    xaxis_title='Month and City',
    yaxis_title='Total Points',
    plot_bgcolor="#222222",  # Background color
    paper_bgcolor="#222222",  # Paper color
    font_color="#FFFFFF"  # Font color
)

# Create the graph component for total points
graph7 = dcc.Graph(figure=fig7)

graph = dcc.Graph()
countries =df['City'].unique().tolist() 

app =dash.Dash(external_stylesheets=[dbc.themes.SLATE])
server= app.server

dropdown = dcc.Dropdown(
    options=[
        {'label': 'Berlin', 'value': 'Berlin'},
        {'label': 'Copenhagen', 'value': 'Copenhagen'},
        {'label': 'Katowice', 'value': 'Katowice'},
        {'label': 'Tokyo', 'value': 'Tokyo'},
        {'label': 'Los Angeles', 'value': 'Los Angeles'}
    ],
    value=['Berlin', 'Copenhagen', 'Katowice', 'Tokyo', 'Los Angeles'],  # Pass as a list
    clearable=False,
    multi=True,
    style={'paddingLeft': '30px', "backgroundColor": "#222222", "color": "#222222"}
)

variables_dropdown = dcc.Dropdown(
    id='variable-dropdown-heatmap',
    options=[
        {'label': 'Wind', 'value': 'Wind'},
        {'label': 'Days with good temperature', 'value': 'Days with good temperature'},
        {'label': 'Non-rainy days', 'value': 'Non-rainy days'}
    ],
    value='Wind',  # Default value
    clearable=False,
    style={'paddingLeft': '30px', "backgroundColor": "#222222", "color": "#222222"}
)

total_points_dropdown = dcc.Dropdown(
    id='total-points-variable-dropdown',
    options=[
        {'label': 'Wind', 'value': 'Wind_Score'},
        {'label': 'Days with good temperature', 'value': 'Temperature_Score'},
        {'label': 'Non-rainy days', 'value': 'Non_rainy_days_Score'}
    ],
    value='Wind_Score',  # Default value
    clearable=False,
    style={'width': '50%', 'paddingLeft': '30px', 'backgroundColor': '#222222', 'color': '#FFFFFF'}
)

app.layout = html.Div([html.H1('What is the best time and location for our sailing event?', style={'textAlign': 'center', 'color': '#636EFA'}), 
                       html.H2('Let''s explore the 5 locations of our offices', style ={'paddingLeft': '40px'}),
                       html.Div(html.P("Graphs"), 
                                style={'marginLeft': 50, 'marginRight': 25}),
                       html.Div([html.Div( 
                                          style={'backgroundColor': '#636EFA', 'color': 'white', 
                                                 'width': '900px', 'marginLeft': 'auto', 'marginRight': 'auto'}),
                                 dropdown,graph1, graph2,  graph3, graph7,variables_dropdown,graph4, graph6])

                      ])

@callback(
    Output(graph1, "figure"), 
    Input(dropdown, "value"))

def update_bar_chart(selected_cities):
    if not selected_cities:
        selected_cities = ['Berlin', 'Copenhagen', 'Katowice', 'Tokyo', 'Los Angeles']
    mask = df["City"].isin(selected_cities)
    fig = px.bar(
        df[mask], 
        x='Month', 
        y='Days with good temperature',
        color='City',
        color_discrete_map = {'Berlin': '#7FC97F',  # Green
                      'Copenhagen': '#BEAED4',  # Purple
                      'Katowice': '#FDC086',  # Orange
                      'Tokyo': '#FFFF99',  # Yellow
                      'Los Angeles': '#386CB0'},  # Blue
        barmode='group',
        height=300,
        title="Good temperatures for sailing by cities",
    )
    fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
    return fig


@callback(
    Output(graph2, "figure"), 
    Input(dropdown, "value"))

def update_bar_chart(selected_cities):
    if not selected_cities:
        selected_cities = ['Berlin', 'Copenhagen', 'Katowice', 'Tokyo', 'Los Angeles']
    mask = df["City"].isin(selected_cities)
    fig = px.bar(
        df[mask], 
        x='Month', 
        y='Non-rainy days',
        color='City',
        color_discrete_map = {'Berlin': '#7FC97F',  # Green
                      'Copenhagen': '#BEAED4',  # Purple
                      'Katowice': '#FDC086',  # Orange
                      'Tokyo': '#FFFF99',  # Yellow
                      'Los Angeles': '#386CB0'},  # Blue
        barmode='group',
        height=300,
        title="Non-rainy days by Month",
    )
    fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
    return fig

@callback(
    Output(graph3, "figure"), 
    Input(dropdown, "value"))

def update_bar_chart(selected_cities):
    if not selected_cities:
        selected_cities = ['Berlin', 'Copenhagen', 'Katowice', 'Tokyo', 'Los Angeles']
    mask = df["City"].isin(selected_cities)
    fig = px.bar(
        df[mask], 
        x='Month', 
        y='Wind',
        color='City',
        color_discrete_map = {'Berlin': '#7FC97F',  # Green
                      'Copenhagen': '#BEAED4',  # Purple
                      'Katowice': '#FDC086',  # Orange
                      'Tokyo': '#FFFF99',  # Yellow
                      'Los Angeles': '#386CB0'},  # Blue
        barmode='group',
        height=300,
        title="Days with good wind for sailing by Month",
    )
    fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
    return fig

@callback(
    Output(graph7, "figure"), 
    Input(dropdown, "value"))

def update_bar_chart(selected_cities):
    if not selected_cities:
        selected_cities = ['Berlin', 'Copenhagen', 'Katowice', 'Tokyo', 'Los Angeles']
    mask = total_points_df["City"].isin(selected_cities)
    fig = px.bar(
        total_points_df[mask], 
        x='Month',
        y='Total Points',
        color='City',
        color_discrete_map = {'Berlin': '#7FC97F',  # Green
                      'Copenhagen': '#BEAED4',  # Purple
                      'Katowice': '#FDC086',  # Orange
                      'Tokyo': '#FFFF99',  # Yellow
                      'Los Angeles': '#386CB0'},  # Blue
        barmode='group',
        height=300,
        title="Total scores",
    )
    fig = fig.update_layout(
        plot_bgcolor="#222222", paper_bgcolor="#222222", font_color="white"
    )
    return fig


@callback(
    Output(graph4, "figure"), 
    Input(dropdown, "value"),
    Input('variable-dropdown-heatmap', 'value')  # Add input for the heatmap dropdown
)
def update_heatmap(selected_cities, variable):
    if not selected_cities:
        selected_cities = ['Berlin', 'Copenhagen', 'Katowice', 'Tokyo', 'Los Angeles']
    mask = df["City"].isin(selected_cities)
    filtered_df = df[mask]
    
    # Ensure the selected variable is numeric
    if variable not in filtered_df.columns:
        return {}
    
    # Create the pivot table based on the selected variable
    pivot_df = filtered_df.pivot_table(index='City', columns='Month', values=variable, aggfunc='mean')

    # Create the heatmap
    fig = px.imshow(pivot_df, labels=dict(x='Month', y='City', color=variable))

    # Update layout
    fig.update_layout(
        title=f'{variable} by Month and City',
        plot_bgcolor="#222222",  # Background color
        paper_bgcolor="#222222",  # Paper color
        font_color="#FFFFFF"  # Font color
    )

    return fig



if __name__ == '__main__':
     app.run_server()