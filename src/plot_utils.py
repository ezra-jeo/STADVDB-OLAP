import pandas as pd
import plotly.express as px
from ipywidgets import VBox, HBox, Output, Layout
from IPython.display import display, clear_output
import pandas as pd


# TODO replace return fig instead if going for web app.

TEMPLATE = "plotly_white"

def make_interactive_query(engine, query, param_config, plot_func, title=None):
    """
    General utility to make SQL queries interactive using ipywidgets and Plotly.
    Regenerates the plot whenever a widget changes.
    """

    widgets = {}
    for name, cfg in param_config.items():
        widgets[name] = cfg["widget"]

    out = Output()

    def run_query(_=None):
        params = {}
        for name, cfg in param_config.items():
            val = widgets[name].value
            if "transform" in cfg:
                val = cfg["transform"](val)
            params[name] = val

        with out:
            clear_output(wait=True)
            df = pd.read_sql(query, engine, params=params)
            if df.empty:
                print("No data found for the current selection.")
            else:
                fig = plot_func(df)

                # Improve figure sizing and prevent clipping
                fig.update_layout(
                    autosize=True,
                    height=600,
                    margin=dict(l=40, r=40, t=60, b=140),
                    title=title or "",
                )

                fig.update_yaxes(dtick=0.5)

                # Use display(fig) for proper ipywidgets integration
                display(fig)

    # Attach listeners
    for w in widgets.values():
        w.observe(run_query, names="value")

    # Split widgets into multiple rows for better layout
    widget_items = list(widgets.values())
    midpoint = len(widget_items) // 2
    row1 = HBox(widget_items[:midpoint], layout=Layout(flex_flow="row wrap", justify_content="flex-start"))
    row2 = HBox(widget_items[midpoint:], layout=Layout(flex_flow="row wrap", justify_content="flex-start"))

    # Initial run
    run_query()

    # Proper layout display
    display(VBox([row1, row2, out]))


# def make_interactive_query(
#     engine,
#     query: str,
#     param_config: dict,
#     plot_func,
#     title: str = "Interactive Visualization"
# ):
#     """
#     General-purpose interactive SQL query runner and Plotly visualizer.

#     Parameters
#     ----------
#     engine : sqlalchemy.Engine
#         The SQLAlchemy database connection engine.
#     query : str
#         SQL query with parameter placeholders (e.g. :topN, :year1, etc.).
#     param_config : dict
#         Configuration defining widgets and parameter mappings.
#     plot_func : callable
#         Function that takes a DataFrame and returns a Plotly figure.
#     title : str
#         Optional title for display.
#     """

#     # Build widgets dynamically from config
#     widgets_dict = {name: config["widget"] for name, config in param_config.items()}

#     # Core update logic
#     def update(**kwargs):
#         params = {}
#         for name, config in param_config.items():
#             value = kwargs[name]
#             # Optional transform, e.g., join lists
#             if "transform" in config and callable(config["transform"]):
#                 value = config["transform"](value)
#             params[name] = value

#         df = pd.read_sql(text(query), engine, params=params)

#         if df.empty:
#             print("⚠️ No data for selected filters.")
#             return

#         fig = plot_func(df)
#         fig.update_layout(title=title, height=600)
#         fig.show()

#     # Link widgets to update function
#     out = interactive_output(update, widgets_dict)
#     display(VBox([w for w in widgets_dict.values()]), out)


# def plot_histogram(df: pd.DataFrame, column: str, bins: int = 30, title: str = None):
#     """Create a histogram for a numeric column."""
#     fig = px.histogram(df, x=column, nbins=bins, title=title or f"Histogram of {column}", template=TEMPLATE)
#     fig.update_layout(bargap=0.1)
#     fig.show()


# def plot_scatter(df: pd.DataFrame, x: str, y: str, color: str = None, size: str = None, title: str = None):
#     """Create a scatter plot."""
#     fig = px.scatter(df, x=x, y=y, color=color, size=size, title=title or f"{y} vs {x}", template=TEMPLATE)
#     fig.update_traces(marker=dict(opacity=0.7, line=dict(width=0)))
#     fig.show()


# def plot_box(df: pd.DataFrame, x: str, y: str, color: str = None, title: str = None):
#     """Box plot for distributions."""
#     fig = px.box(df, x=x, y=y, color=color, title=title or f"Distribution of {y} by {x}"   , template=TEMPLATE)
#     fig.show()


# def plot_timeseries(df: pd.DataFrame, x: str, y: str, color: str = None, title: str = None):
#     """Time series line plot."""
#     fig = px.line(df, x=x, y=y, color=color, title=title or f"{y} over time", template=TEMPLATE)
#     fig.update_xaxes(rangeslider_visible=True)
#     fig.show()


# def plot_bar(df: pd.DataFrame, x: str, y: str, color: str = None, title: str = None):
#     """Bar plot."""
#     fig = px.bar(df, x=x, y=y, color=color, title=title or f"{y} by {x}", template=TEMPLATE)
#     fig.update_layout(bargap=0.2)
#     fig.show()


# def plot_interactive_histogram(df: pd.DataFrame, column: str, color: str = None, bins: int = 30, title: str = None):
#     """Interactive histogram with hover and dynamic bin sizing."""
#     fig = px.histogram(
#         df,
#         x=column,
#         color=color,
#         nbins=bins,
#         title=title or f"Histogram of {column}",
#         marginal="box",  # shows box plot above
#         hover_data=df.columns,
#         template=TEMPLATE
#     )
#     fig.update_layout(bargap=0.1)
#     fig.show()


# def plot_interactive_scatter(df: pd.DataFrame, x: str, y: str, color: str = None, size: str = None, title: str = None):
#     """Interactive scatter plot with hover info."""
#     fig = px.scatter(
#         df,
#         x=x,
#         y=y,
#         color=color,
#         size=size,
#         hover_data=df.columns,
#         title=title or f"{y} vs {x}",
#         template=TEMPLATE
#     )
#     fig.update_traces(marker=dict(opacity=0.8, line=dict(width=0.5, color="white")))
#     fig.update_layout(legend=dict(itemsizing="constant"))
#     fig.show()


# def plot_interactive_timeseries(df: pd.DataFrame, x: str, y: str, color: str = None, title: str = None):
#     """Interactive time series with range slider and selector."""
#     fig = px.line(
#         df,
#         x=x,
#         y=y,
#         color=color,
#         title=title or f"{y} over time",
#         template=TEMPLATE
#     )
#     fig.update_xaxes(
#         rangeslider_visible=True,
#         rangeselector=dict(
#             buttons=list([
#                 dict(count=7, label="1w", step="day", stepmode="backward"),
#                 dict(count=1, label="1m", step="month", stepmode="backward"),
#                 dict(count=3, label="3m", step="month", stepmode="backward"),
#                 dict(step="all")
#             ])
#         )
#     )
#     fig.show()


# def plot_interactive_bar(df: pd.DataFrame, x: str, y: str, color: str = None, title: str = None):
#     """Interactive bar chart with hover tooltips and animation for temporal data."""
#     fig = px.bar(
#         df,
#         x=x,
#         y=y,
#         color=color,
#         hover_data=df.columns,
#         title=title or f"{y} by {x}",
#         template=TEMPLATE
#     )
#     fig.update_layout(bargap=0.2)
#     fig.show()


# def plot_interactive_heatmap(df: pd.DataFrame, corr_method: str = "pearson", title: str = "Correlation Heatmap"):
#     """Interactive correlation heatmap."""
#     corr = df.corr(method=corr_method)
#     fig = px.imshow(
#         corr,
#         text_auto=True,
#         color_continuous_scale="RdBu_r",
#         title=title,
#         template=TEMPLATE
#     )
#     fig.update_layout(
#         xaxis=dict(tickangle=45),
#         yaxis=dict(autorange="reversed"),
#     )
#     fig.show()

# def parametered_histogram(df: pd.DataFrame, columns : list, title: str = "Histogram"):
#     # Create base figure with first column
#     fig = go.Figure()

#     # Add one histogram per column (we'll toggle visibility)
#     for i, col in enumerate(columns):
#         fig.add_trace(
#             go.Histogram(
#                 x=df[col],
#                 name=col,
#                 visible=True if i == 0 else False,
#                 opacity=0.75
#             )
#         )

#     # Add dropdown menu
#     fig.update_layout(
#         title=title,
#         updatemenus=[
#             dict(
#                 buttons=[
#                     dict(
#                         label=col,
#                         method="update",
#                         args=[
#                             {"visible": [i == j for j in range(len(columns))]},
#                             {"title": f"Distribution of {col}"}
#                         ]
#                     ) for i, col in enumerate(columns)
#                 ],
#                 direction="down",
#                 showactive=True,
#                 x=0.5,
#                 xanchor="center",
#                 y=1.15,
#                 yanchor="top"
#             )
#         ],
#         template="plotly_white"
#     )

#     fig.show()