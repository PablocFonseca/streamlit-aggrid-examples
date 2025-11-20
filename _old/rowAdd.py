import streamlit as st
from st_aggrid import AgGrid, JsCode
import json
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Sample JSON data
data = [
    # {"id": "1", "name": "Alice", "age": "25"},
    {"id": 2, "name": "Bob", "age": 30},
    # {"id": 3, "name": "Charlie", "age": 35},
    # {"id": 4, "name": "David", "age": 40},
    # {"id": 5, "name": "Eve", "age": 22},
    # {"id": 6, "name": "Frank", "age": 28},
    # {"id": 7, "name": "Grace", "age": 33},
    # {"id": 8, "name": "Hannah", "age": 27},
    # {"id": 9, "name": "Ivy", "age": 29},
    # {"id": 10, "name": "Jack", "age": 31},
]

vf = JsCode("""
function vf(params){
    function isEmptyPinnedCell({node, value}){
        return (node.rowPinned !== undefined && value == null) ||
            (node.rowPinned !== undefined && value == '')
    };
    function createPinnedCellPlaceholder({ colDef }) {
        return colDef.field[0].toUpperCase() + colDef.field.slice(1) + '...';
    };
    if (isEmptyPinnedCell(params) && (params.column.colDef.editable)) {
        return createPinnedCellPlaceholder(params);
    }
    return undefined;
    console.log(params)
    
}
""")
# Create grid options as a plain dictionary
grid_options = {
    "columnDefs": [
        {"field": "id", "headerName": "ID", "valueFormatter": vf},
        {"field": "name", "headerName": "Name", "valueFormatter": vf, "editable": True},
        {"field": "age", "headerName": "Age", "valueFormatter": vf, "editable": True},
    ],
    "pinnedBottomRowData": [{}],
}

# Streamlit app
st.title("Basic AgGrid Example")

# Render AgGrid
AgGrid(json.dumps(data), gridOptions=grid_options, allow_unsafe_jscode=True)
