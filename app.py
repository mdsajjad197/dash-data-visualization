import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Read the processed data
df = pd.read_csv("output.csv")

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Sort data by date
df = df.sort_values("date")

# Create the line chart
fig = px.line(
    df,
    x="date",
    y="Sales",
    color="region",
    title="Pink Morsel Sales Over Time"
)

# Axis labels
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales"
)

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        "Soul Foods Sales Visualizer",
        style={"textAlign": "center"}
    ),

    dcc.Graph(
        figure=fig
    )
])

# Run the app
if __name__ == "__main__":
    app.run(debug=True)