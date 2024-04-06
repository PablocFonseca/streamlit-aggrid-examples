import streamlit as st
import numpy as np
import pandas as pd

from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder


@st.cache_data()
def get_data_ex5():
    rows = 10
    df = pd.DataFrame(
        np.random.randint(0, 100, 2 * rows).reshape(-1, 2), columns=list("ab")
    )
    return df


reload_data = False

data = get_data_ex5()
gb = GridOptionsBuilder.from_dataframe(data)

# make all columns editable
gb.configure_columns(list("abcde"), editable=True)

# Create a calculated column that updates when data is edited. Use agAnimateShowChangeCellRenderer to show changes
gb.configure_column(
    "virtual column a + b",
    valueGetter="Number(data.a) + Number(data.b)",
    cellRenderer="agAnimateShowChangeCellRenderer",
    editable="false",
    type=["numericColumn"],
)
go = gb.build()
st.markdown(
    """
### Virtual columns
it's possible to configure calculated columns an below.  
Input data only has columns a and b. column c is defined as sum of a and b.  
Finally, an agAnimateShowChangeCellRenderer is set to highlight and display changes.
``` python
gb.configure_column(  
    "virtual column a + b",  
    valueGetter="Number(data.a) + Number(data.b)" 
    cellRenderer="agAnimateShowChangeCellRenderer",
    editable="false"
    ) 
```  
The valueGetter is set without a JsCode wrapper, because AgGrid supports [expressions](https://ag-grid.com/javascript-data-grid/cell-expressions/) on some gridOptions
"""
)

tabs = st.tabs(["AgGrid", "gridOptions","Response Data"])

with tabs[0]:
    ag = AgGrid(
        data,
        gridOptions=go,
        height=400,
        fit_columns_on_grid_load=True,
        key="an_unique_key_xZs151",
        reload_data=reload_data,
    )

with tabs[1]: 
    st.write(go)

with tabs[2]:
    st.dataframe(ag.data)

