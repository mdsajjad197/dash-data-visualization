import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
from pathlib import Path


# ==============================
# Read CSV File
# ==============================

required_columns = {"Sales", "date", "region"}
csv_files = [Path("output.csv"), *sorted(
    Path(".").glob("output_*.csv"),
    key=lambda path: path.stat().st_mtime,
    reverse=True
)]

df = None

for csv_file in csv_files:
    if not csv_file.exists():
        continue

    candidate_df = pd.read_csv(csv_file)
    candidate_df.columns = candidate_df.columns.str.strip()

    if required_columns.issubset(candidate_df.columns) and not candidate_df.empty:
        df = candidate_df
        print(f"Loaded data from {csv_file}")
        break

if df is None:
    raise FileNotFoundError(
        "No valid sales output CSV found. Run process_data.py and close output.csv if it is open."
    )


# ==============================
# Clean Column Names
# ==============================

df.columns = df.columns.str.strip()


# Check columns
print("CSV Columns:", df.columns)


# ==============================
# Convert Date Column
# ==============================

df["date"] = pd.to_datetime(df["date"])


# Sort data by date

df = df.sort_values("date")



# ==============================
# Create Dash App
# ==============================

app = Dash(__name__)



# ==============================
# Dashboard Layout
# ==============================

app.layout = html.Div([

    html.H1(
        "Soul Foods Pink Morsel Sales Dashboard",
        id="header"
    ),


    dcc.RadioItems(

        id="region-filter",

        options=[
            {
                "label": "All",
                "value": "all"
            },

            {
                "label": "North",
                "value": "north"
            },

            {
                "label": "East",
                "value": "east"
            },

            {
                "label": "South",
                "value": "south"
            },

            {
                "label": "West",
                "value": "west"
            }
        ],

        value="all",

        inline=True
    ),


    html.Br(),


    dcc.Graph(
        id="sales-chart"
    )


])



# ==============================
# Update Graph
# ==============================

@app.callback(

    Output(
        "sales-chart",
        "figure"
    ),

    Input(
        "region-filter",
        "value"
    )

)


def update_graph(region):


    if region == "all":

        filtered_df = df


    else:

        filtered_df = df[
            df["region"]
            .str.lower()
            .str.strip()
            == region
        ]



    fig = px.line(

        filtered_df,

        x="date",

        y="Sales",

        color="region",

        markers=True,

        title="Pink Morsel Sales Over Time"

    )


    fig.update_layout(

        xaxis_title="Date",

        yaxis_title="Sales",

        template="plotly_white"

    )


    return fig




# ==============================
# Run App
# ==============================

if __name__ == "__main__":

    app.run(

        debug=True,

        use_reloader=False

    )
