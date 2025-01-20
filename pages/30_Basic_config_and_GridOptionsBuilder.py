import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd


@st.cache_data
def get_data():
    return pd.read_json("https://www.ag-grid.com/example-assets/olympic-winners.json")


df = get_data()

try:
    st.set_page_config(layout="wide")
except Exception:
    pass

st.markdown(
    """
## Grid Configuration
The Grid is configured by supplying the gridOptions parameter a dictionary like object.   
A full reference to gridOptions may be found on [https://ag-grid.com/javascript-data-grid/grid-options/.](https://ag-grid.com/javascript-data-grid/grid-options/) 
and [https://ag-grid.com/javascript-data-grid/column-properties/](https://ag-grid.com/javascript-data-grid/column-properties/)

If gridOptions parameter is not supplied, stAgGrid uses the `gridOptionsBuilder.from_dataframe` to infer basic gridOptions from data.
you can use it to create a basic object and then customize it or create everything from scratch.

```python
grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_options = grid_builder.build()

grid_options['columnDefs'][0]['checkboxSelection'] = True

AgGrid(data=df, gridOptions=grid_options, key='grid1')
```

"""
)

grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_options = grid_builder.build()

grid_options["columnDefs"][0]["checkboxSelection"] = True

tabs = st.tabs(["Grid", "gridOptions"])

with tabs[0]:
    AgGrid(data=df, gridOptions=grid_options, key="grid1")

with tabs[1]:
    st.write(grid_options)

st.markdown(
    """
## GridOptionsBuilder
gridOptionsBuilder has some convenience methods to configure the grid.  
The same result for the grid below, with multiple selection, side panel and pagination enabled can be achieved by passing the raw object listed on the *gridOptions*     tab.
```python
from st_aggrid import AgGrid, GridOptionsBuilder

grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_builder.configure_selection(selection_mode="multiple", use_checkbox=True)
grid_builder.configure_side_bar(filters_panel=True, columns_panel=False)
grid_options = grid_builder.build()

AgGrid(data=df, gridOptions=grid_options, key='grid2')
```
"""
)

grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_builder.configure_selection(selection_mode="multiple", use_checkbox=True)
grid_builder.configure_side_bar(filters_panel=True, defaultToolPanel="filters")
grid_builder.configure_pagination()

grid_options = grid_builder.build()

tabs = st.tabs(["Grid", "gridOptions"])

with tabs[0]:
    AgGrid(data=df, gridOptions=grid_options, key="grid2")

with tabs[1]:
    st.markdown("*gridOptions* =")
    st.json(grid_options)


st.markdown(
    """
### GridOptionsBuilder reference:
"""
)
GridOptionsBuilder

st.markdown("### Attributes")
for p in dir(GridOptionsBuilder):
    if not p.startswith("_"):
        _ = grid_builder.__getattribute__(p)
        st.write(_)
