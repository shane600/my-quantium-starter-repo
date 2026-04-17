import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go

df = pd.read_csv("data/output.csv", parse_dates=["date"])
df = df.sort_values("date")

daily = df.groupby(["date", "region"])["sales"].sum().reset_index()

regions = ["north", "south", "east", "west"]
colours = {"north": "#636EFA", "south": "#EF553B", "east": "#00CC96", "west": "#FFA15A"}

price_increase_date = pd.Timestamp("2021-01-15")

fig = go.Figure()

for region in regions:
    subset = daily[daily["region"] == region]
    fig.add_trace(go.Scatter(
        x=subset["date"],
        y=subset["sales"],
        mode="lines",
        name=region.capitalize(),
        line=dict(color=colours[region])
    ))

fig.add_vline(
    x=price_increase_date.timestamp() * 1000,
    line_width=2,
    line_dash="dash",
    line_color="grey",
    annotation_text="Price increase, 15 Jan 2021",
    annotation_position="top left",
    annotation_font_size=12,
    annotation_font_color="grey"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Sales ($)",
    legend_title="Region",
    plot_bgcolor="white",
    paper_bgcolor="white",
    xaxis=dict(showgrid=True, gridcolor="#eeeeee"),
    yaxis=dict(showgrid=True, gridcolor="#eeeeee"),
    margin=dict(t=20, l=60, r=20, b=60)
)

app = Dash(__name__)

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "maxWidth": "1100px", "margin": "0 auto", "padding": "24px"},
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={"textAlign": "center", "marginBottom": "8px", "color": "#222222"}
        ),
        html.P(
            "Daily sales by region. The dashed line marks the price increase on 15 January 2021.",
            style={"textAlign": "center", "color": "#555555", "marginBottom": "24px"}
        ),
        dcc.Graph(figure=fig, style={"height": "520px"})
    ]
)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
