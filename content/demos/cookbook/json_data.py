import streamlit as st
import numpy as np
import pandas as pd

from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder

st.title("Loading JSON Data and GridOptions")

st.markdown("""
This example demonstrates loading both data and grid configuration directly from JSON files.
AgGrid can accept file paths for both the `data` parameter and `gridOptions` parameter,
making it easy to work with external JSON data sources.
""")

data_file = "./json_data.json"
gridOptions_file = "./json_data_gridOptions.json"

AgGrid(
    data_file, gridOptions=gridOptions_file, try_to_convert_back_to_original_types=False, height=400
)

with st.expander("Show code", expanded=False):
    st.code("""
from st_aggrid import AgGrid

# Load data and gridOptions from JSON files
data_file = "./json_data.json"
gridOptions_file = "./json_data_gridOptions.json"

# Display grid with JSON data and config
AgGrid(
    data_file,
    gridOptions=gridOptions_file,
    try_to_convert_back_to_original_types=False,
    height=400
)
""", language="python")
