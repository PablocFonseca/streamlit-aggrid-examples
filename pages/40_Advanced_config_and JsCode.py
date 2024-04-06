import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import pandas as pd

@st.cache_data
def get_data():
  return  pd.read_json("https://www.ag-grid.com/example-assets/olympic-winners.json")

df = get_data()

try:
  st.set_page_config(layout='wide')
except:
  pass

st.markdown(
"""
### Injecting JsCode
Some properties on gridOptions receive javascript functions. You can inject JavaScript code by using the JsCode object.  
For instance the [documentation](https://ag-grid.com/javascript-data-grid/cell-styles/#reference-styling-cellStyle) of `cellStyle` columnOption
tell us that it can be set to either a CellStyle string or a *CellStyleFunc* function.  
On the example below we use a custom function to format the cell, based on the number of gold medals earned, if more than 3 row will be gold.  
```python
from st_aggrid import JsCode
cellStyle = JsCode(
    r\"\"\"
    function(cellClassParams) {
         if (cellClassParams.data.gold > 3) {
            return {'background-color': 'gold'}
         }
         return {};
        }
   \"\"\")

grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_options = grid_builder.build()

grid_options['defaultColDef']['cellStyle'] = cellStyle

AgGrid(data=df, gridOptions=grid_options, allow_unsafe_jscode=True, key='grid1')
```
"""
)

st.info(
""" 
##### ⚠ Note! 
When using JsCode you need to call AgGrid with `allow_unsafe_jscode=True`.""")

cellStyle = JsCode(
   r"""
    function(cellClassParams) {
         if (cellClassParams.data.gold > 3) {
            return {'backgroundColor': 'gold'}
         }
         return {};
        }
   """)

grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_options = grid_builder.build()

grid_options['defaultColDef']['cellStyle'] = cellStyle

tabs = st.tabs(['Grid', 'gridOptions'])

with tabs[0]:
    AgGrid(data=df, gridOptions=grid_options, allow_unsafe_jscode=True, key='grid1')

with tabs[1]:
   st.write(grid_options)