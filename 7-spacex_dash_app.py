# Import required libraries
import dash
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Pie chart
df_piechart = spacex_df.groupby(["Launch Site"], as_index=False)["class"].sum()

pie_chart = px.pie(
    data_frame=df_piechart,
    values="class",
    names="Launch Site",
    title="Total Success Launches by Site",
    color="Launch Site",
    hover_data=["class"],
)

# Scatterplot
scatterplot = px.scatter(
    data_frame=spacex_df,
    x="Payload Mass (kg)",
    y="class",
    color="Booster Version Category",
    title="Payload Mass vs Outcome for all Sites",
)

# Create a dash application
app = Dash()

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        # dcc.Dropdown(id='site-dropdown',...)
        html.Label("Select the launch site:"),
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"},
                {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
                {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
            ],
            value="ALL",  # Valor inicial
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart", figure=pie_chart)),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        # dcc.RangeSlider(id='payload-slider',...)
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            marks={0: "0", 10000: "10000"},
            value=[min_payload, max_payload],
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="success-payload-scatter-chart", figure=scatterplot)),
    ]
)


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output("success-pie-chart", "figure"), Input("site-dropdown", "value"))
def update_piechart(site):
    if site == "ALL":
        piechart_updated = pie_chart
    else:
        df_site = spacex_df[spacex_df["Launch Site"] == site]
        piechart_updated = px.pie(
            data_frame=df_site,
            names="class",
            title=f"Total Success Launches for site {site}",
            hover_data=["class"],
        )
    return piechart_updated


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [Input("site-dropdown", "value"), Input("payload-slider", "value")],
)
def update_scatterplot(site, range):
    low, high = range
    df_filtered = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= low)
        & (spacex_df["Payload Mass (kg)"] <= high)
    ]

    if site == "ALL":
        scatter_updated = px.scatter(
            data_frame=df_filtered,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Payload Mass vs Outcome for all Sites",
        )
    else:
        df_site_filtered = df_filtered[df_filtered["Launch Site"] == site]
        scatter_updated = px.scatter(
            data_frame=df_site_filtered,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title=f"Payload Mass vs Outcome for Site {site}",
        )

    return scatter_updated


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
