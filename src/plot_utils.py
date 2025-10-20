import pandas as pd
import plotly.express as px
from ipywidgets import VBox, HBox, Output, Layout
from IPython.display import display, clear_output
import pandas as pd

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

