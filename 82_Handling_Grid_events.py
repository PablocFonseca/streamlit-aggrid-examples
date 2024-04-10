import streamlit as st
from st_aggrid import AgGrid, JsCode, GridOptionsBuilder
import pandas as pd


@st.cache_data
def get_data():
  r = pd.read_json("https://www.ag-grid.com/example-assets/olympic-winners.json")
  return r

df = get_data()


#reference to onCellClicked handling functions here: https://ag-grid.com/javascript-data-grid/grid-events/#reference-selection-cellDoubleClicked
#This example function logs the params to the console and alerts which row/column was clicked.
onCellDoubleClickedHandler = JsCode(r"""
    function (params){
      console.log(params);
      let clickedColumn = params.column.colId;
      let clickedRowIndex = params.rowIndex;
      let clickedValue = params.node.data[clickedColumn];
                                    
      let msg = `You double clicked on row ${clickedRowIndex}, column ${clickedColumn}, value is ${clickedValue}`;
                                    
      alert(msg);                                      
    }
""")

st.markdown("""
  In the example below, we use JsCode to attach the `onCellDoubleClickedHandler` function using the `onCellDoubleClicked` option in gridOptions.
  
  ```javascript
      onCellDoubleClickedHandler = function (params){
        console.log(params);
        let clickedColumn = params.column.colId;
        let clickedRowIndex = params.rowIndex;
        let clickedValue = params.node.data[clickedColumn];
                                      
        let msg = `You double clicked on row ${clickedRowIndex}, column ${clickedColumn}, value is ${clickedValue}`;
                                      
        alert(msg);                                      
    }
  ```
            
  ```python
  
  gd = GridOptionsBuilder().from_dataframe(df)
  gd.configure_grid_options(onCellDoubleClicked=onCellDoubleClickedHandler)
  go = gd.build()

  AgGrid(df, go, allow_unsafe_jscode=True)
    ```
""")


gd = GridOptionsBuilder().from_dataframe(df)

gd.configure_grid_options(onCellDoubleClicked=onCellDoubleClickedHandler)

go = gd.build()

AgGrid(df, go, allow_unsafe_jscode=True)