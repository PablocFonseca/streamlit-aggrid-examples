import streamlit as st
import os

try:
    st.set_page_config(layout="wide")
except:
    pass

root = os.path.join(os.path.dirname(__file__), "..")

dashboards = {
    "Custom Cell Rendererers": os.path.join(root, "20_cell_renderer_class_example.py"),
    "Websockets": os.path.join(root, "websockets.py"),
    "Virtual Columns": os.path.join(root, "30_virtual_columns.py"),
    "Highlight Editions": os.path.join(root, "40_example_highlight_change.py"),
    "Themes & Pre-Selection": os.path.join(root, "50_themes_and_pre_selection.py"),
    "Rich Cell Editor": os.path.join(root, "60_rich_cell_editor.py"),
    "Nested Grids": os.path.join(root, "70_nested_grids.py"),
    "Columns State": os.path.join(root, "80_saving_columns_state.py"),
    "Tooltips": os.path.join(root, "81_Tooltips.py"),
    "Grid Events": os.path.join(root, "82_Handling_Grid_events.py"),
    "Real Time Updates": os.path.join(root, "83_fetching_real_time_data.py"),
    "Custom Tooltip": os.path.join(root, "custom_tooltip.py"),
    "Classic Example": os.path.join(root, "90_main_example.py"),
}

index = 0
choice_from_url = query_params = st.query_params.get("example", None)
if choice_from_url:
    index = list(dashboards.keys()).index(choice_from_url)

choice = st.sidebar.radio("Cookbook examples", list(dashboards.keys()), index=index)

path = dashboards[choice]

with open(path, encoding="utf-8") as code:
    c = code.read()
    exec(c, globals())

    with st.expander("Code for this example:"):
        st.markdown(f"""``` python
{c}```""")
