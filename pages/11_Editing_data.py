import streamlit as st
from st_aggrid import AgGrid
import pandas as pd


@st.cache_data
def get_data():
    return pd.read_json("https://www.ag-grid.com/example-assets/olympic-winners.json")


df = get_data()

try:
    st.set_page_config(layout="wide")
except:
    pass

st.markdown("## Making cells editable")

st.markdown("""
You can make the grid editable by setting `'editable':True` on [gridOptions.columnDefs](https://ag-grid.com/javascript-data-grid/cell-editing/).  
Easiest way is to pass it as an argument to AgGrid call:   
            
```python 
AgGrid(df, editable=True)
```
The component is smart enough to know that editable is a property that should be applied to all columns, so under the hood it infers the [gridOptions](https://ag-grid.com/javascript-data-grid/grid-options/) as:
            
```json
gridOptions = {
    defaultColDef : {
        editable:true
    }
    ...
}
```

if you want to make only some columns editable, you'll need to manually create the gridOptions and set `'editable': True` on individual columns.  
""")

st.info("""
### ⚠ Grid behaviour when editing data.
If the grid has a fixed key, it will update whenever underlying dataframe updates.
However, if the grid is "dirty" (any data has been edited) it will __stop updating and ignore any change on data__.   
Return object will now only hold the modified data. 
To 'clean' the grid again, it needs to be destroied and recreated, by changing the key parameter or reloading the page.""")

st.markdown("""
On the example below the grid is fully editable. Modified data is returned on `grid_return.data`.
Clicking the buttom samples 50 rows from the data set to simulate data refreshing. Once edited, grid will ignore further data changes
""")


tabs = st.tabs(
    ["Grid", "Underlying Data", "Infered GridOptions", "Returned AgGrid Data"]
)

with tabs[0]:
    st.button("Update underlying data.", key="b1")
    data = df.sample(50)
    grid_return = AgGrid(data, editable=True, key="grid1")

with tabs[1]:
    st.button("Update underlying data.", key="b2")
    st.write(data)

with tabs[2]:
    st.write(grid_return.grid_options)

with tabs[3]:
    st.write(grid_return.data)
