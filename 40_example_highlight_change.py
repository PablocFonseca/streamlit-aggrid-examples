import streamlit as st
import numpy as np
import pandas as pd

from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode


@st.cache_data()
def get_data_ex7():
    df = pd.DataFrame(
        np.random.randint(0, 100, 100).reshape(-1, 5), columns=list("abcde")
    )
    return df


data = get_data_ex7()

gb = GridOptionsBuilder.from_dataframe(data)
# make all columns editable
gb.configure_columns(list("abcde"), editable=True)


js = JsCode(
    """
function(e) {
    let api = e.api;
    let rowIndex = e.rowIndex;
    let col = e.column.colId;
    
    console.log(e);
    let rowNode = api.getDisplayedRowAtIndex(rowIndex);
    api.flashCells({
      rowNodes: [rowNode],
      columns: [col],
      flashDelay: 10000000000
    });

};
"""
)

gb.configure_grid_options(onCellValueChanged=js)
go = gb.build()
st.markdown(
    """
### JsCode injections
Cell editions are highlighted here by attaching to ```onCellValueChanged``` of the grid, using JsCode injection
```python
js = JsCode(...)
gb.configure_grid_options(onCellValueChanged=js) 
ag = AgGrid(data, gridOptions=gb.build(),  key='grid1', allow_unsafe_jscode=True)
```
"""
)

tabs = st.tabs(["AgGrid", "gridOptions","Response Data"])

with tabs[0]:
    ag = AgGrid(
        data, gridOptions=go, key="grid1", allow_unsafe_jscode=True
    )

with tabs[1]:
    st.dataframe(ag["data"])

with tabs[2]:
    st.write(go)
