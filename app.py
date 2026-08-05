import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Read output file
df = pd.read_csv("output.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Sort by date
df = df.sort_values("date")

app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        "Soul Foods Pink Morsel Sales Dashboard",
        id="header"
    ),

    dcc.RadioItems(
        id="region-filter",
        options=[
            {"label": "All", "value": "all"},
            {"label": "North", "value": "north"},
            {"label": "East", "value": "east"},
            {"label": "South", "value": "south"},
            {"label": "West", "value": "west"},
        ],
        value="all",
        inline=True
    ),

    dcc.Graph(id="sales-chart")
])

@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_graph(region):

    if region == "all":
        filtered = df
    else:
        filtered = df[df["region"].str.lower() == region]

    fig = px.line(
        filtered,
        x="date",
        y="Sales",
        color="region",
        title="Pink Morsel Sales Over Time",
        markers=True
    )

    return fig

if __name__ == "__main__":
    app.run(debug=True)