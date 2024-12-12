#Load necessary libraries
import dash
from dash import Input,Output,dcc,html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

# Load the CSV file
df = pd.read_csv("C:/Users/ASUS/Desktop/work_sql/UAB_capstone/kpi_csvs/wallet_count_summary/user_kyc_status_alltime_v3.csv")

#initialize dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

#user type selection card
controls = dbc.Card([
    html.Div([
        dbc.Label("Select User Type"),
        dcc.Dropdown(
            id = 'usertype_description',
            options = [{'label':utd,'value':utd} for utd in df['usertype_description'].unique()],
            value= 'uabpay',
            multi = True,
        ),
    ])
])

#creating app layout
app.layout = dbc.Container([
    html.H1('User Count by User Type'),
    html.Hr(),
    dbc.Row([
        dbc.Col(controls,lg=4,sm=12),
        dbc.Col(dcc.Graph(id='graph-usercount'),lg=8,sm=12)
    ],align="center"),
])


#update bar chart callback function
@app.callback(Output('graph-usercount', 'figure'), Input('usertype_description', 'value'))
def make_usercount_graph(usertype_list):
    # Ensure usertype_list is a list
    if not isinstance(usertype_list, list):
        usertype_list = [usertype_list]

    # Filter data by selected user types
    dff = df[df.usertype_description.isin(usertype_list)]
    
    # Group by usertype_description and sum the user_count
    grouped_df = dff.groupby('usertype_description', as_index=False)['user_count'].sum()

    # Initialize figure
    fig = go.Figure()

    # Add a bar trace for each usertype_description
    fig.add_trace(
        go.Bar(
            x=grouped_df['usertype_description'],
            y=grouped_df['user_count'],
            name='User Count'
        )
    )

    # Update layout with title and axis labels
    fig.update_layout(
        title="Total User Count by User Type",
        xaxis_title="User Type Description",
        yaxis_title="User Count",
        xaxis_tickfont_size=10
    )

    return fig



    
if __name__ == "__main__":
    app.run_server(debug = True)
