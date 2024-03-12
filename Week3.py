# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_site = sorted(spacex_df["Launch Site"])

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div([
                                    html.Label("select sites"),
                                    dcc.Dropdown(id = 'site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'ALL'}, 
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                    searchable = True,
                                    value='ALL',
                                    placeholder="Select Launch Site")]),

                                    html.Br(),

                                    # TASK 2:
                                    html.Div(dcc.Graph(id = "sucess-pie-chart")),
                                    html.Br(),

                                    html.P("Payload range (kg): "),

                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id = 'payload-slider',
                                    min = 0, max = 10000, step = 1000,
                                    marks = {0:'0', 2000:'2000', 4000:'4000', 6000: '6000', 8000:'8000', 10000:'10000'},
                                    value = [min_payload, max_payload]),

                                    html.Div(dcc.Graph(id = 'success-payload-scatter-chart')), ])

                                # Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
                                # Function decorator to specify function input and output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))
            
def get_pie_chart(entered_site):
    #filtered_df = spacex_df.groupby("Launch Site").mean()
    if entered_site == 'ALL':
        df_all = spacex_df[spacex_df["class" == 1]]
        fig = px.pie(df_all, values='success', 
        names='Launch site', 
        title='Total success lanches by site')
        return fig
    else:
        site_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        site_df_group = site_df.groupby()
        fig = px.pie(filtered_df[filtered_df["Launch Site"]==entered_site])
        names = entered_site
        title = 'Success launches by site'
        return fig

@app.callback(Output(component_id = 'sucess-payload-scatter-chart', component_property = 'figure'),
             [Input(component_id = 'site-dropdown', component_property = 'value'),
             Input(component_id = 'payload-slider', component_property = 'value')])

def update_chart_scatter(entered_site, payload_val):
  payload_low, payload_high = payload_val
  if entered_site == 'ALL':
    fig = px.scatter(spacex_df, x = "Payload mass (kg)", y = 'class', color = "Booster Version Category")
    fig.update_layout(title = "Payload Mass and the Outcome from all launche sites")
    return fige
  else:
    site_df = spacex_df[spacex_df["Launch Site"] == entered_site]
    site_df = site_df[(site_df["Payload Mass (kg)"] > payload_low) & (site_df["Payload Mass (kg)"] < payload_high)]
    fig = px.scatter(site_df, x = "Payload mass (kg)", y = 'class', color = "Booster Version Category")
    fig.update_layout(title = "Success possibility when launch site is " + entered_site + " and " + "payload Mass from " + str(payload_low) + "kg" + " to " + str(payload_high) + "kg")
    return fig
    
          
# Run the app
if __name__ == '__main__':
    app.run_server()
     
