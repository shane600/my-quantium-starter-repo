import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objects as go

# load the cleaned output and sort by date
df = pd.read_csv("data/output.csv", parse_dates=["date"])
df = df.sort_values("date")

daily = df.groupby(["date", "region"])["sales"].sum().reset_index()

regions = ["north", "south", "east", "west"]
colours = {"north": "#4361ee", "south": "#f72585", "east": "#4cc9f0", "west": "#7209b7"}

# plotly needs a unix millisecond timestamp for the vline on a date axis
price_increase_ts = pd.Timestamp("2021-01-15").timestamp() * 1000

app = Dash(__name__)

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "background": "linear-gradient(135deg, #0f0c29, #302b63, #24243e)",
        "fontFamily": "'Segoe UI', Arial, sans-serif",
        "padding": "40px 24px"
    },
    children=[
        html.Div(
            style={
                "maxWidth": "1100px",
                "margin": "0 auto",
                "background": "rgba(255,255,255,0.05)",
                "borderRadius": "16px",
                "padding": "36px 40px",
                "boxShadow": "0 8px 32px rgba(0,0,0,0.4)"
            },
            children=[
                html.H1(
                    "Pink Morsel Sales Visualiser",
                    style={
                        "textAlign": "center",
                        "color": "#f72585",
                        "fontSize": "2.2rem",
                        "marginBottom": "6px",
                        "letterSpacing": "1px"
                    }
                ),
                html.P(
                    "Daily sales by region. The dashed line marks the price increase on 15 January 2021.",
                    style={
                        "textAlign": "center",
                        "color": "#bbbbcc",
                        "marginBottom": "28px",
                        "fontSize": "0.95rem"
                    }
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "center",
                        "marginBottom": "28px"
                    },
                    children=[
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"}
                            ],
                            value="all",
                            inline=True,
                            inputStyle={"marginRight": "6px", "accentColor": "#f72585"},
                            labelStyle={
                                "marginRight": "24px",
                                "color": "#ffffff",
                                "fontSize": "1rem",
                                "cursor": "pointer"
                            }
                        )
                    ]
                ),
                dcc.Graph(id="sales-chart", style={"height": "500px"})
            ]
        )
    ]
)


# redraws the chart whenever the region filter changes
@callback(Output("sales-chart", "figure"), Input("region-filter", "value"))
def update_chart(selected_region):
    fig = go.Figure()

    active_regions = regions if selected_region == "all" else [selected_region]

    for region in active_regions:
        subset = daily[daily["region"] == region]
        fig.add_trace(go.Scatter(
            x=subset["date"],
            y=subset["sales"],
            mode="lines",
            name=region.capitalize(),
            line=dict(color=colours[region], width=2)
        ))

    fig.add_vline(
        x=price_increase_ts,
        line_width=2,
        line_dash="dash",
        line_color="#aaaaaa",
        annotation_text="Price increase, 15 Jan 2021",
        annotation_position="top left",
        annotation_font_size=12,
        annotation_font_color="#aaaaaa"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales ($)",
        legend_title="Region",
        plot_bgcolor="#1a1a2e",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ddddee"),
        xaxis=dict(showgrid=True, gridcolor="#2a2a4a", color="#ddddee"),
        yaxis=dict(showgrid=True, gridcolor="#2a2a4a", color="#ddddee"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#ddddee")),
        margin=dict(t=20, l=60, r=20, b=60)
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
