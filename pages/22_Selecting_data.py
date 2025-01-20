import streamlit as st
import pandas as pd
import json

from st_aggrid import AgGrid
from code_editor import code_editor


@st.cache_data
def get_data():
    return pd.read_json("https://www.ag-grid.com/example-assets/olympic-winners.json")


df = get_data()

try:
    st.set_page_config(layout="wide")
except:
    pass

st.markdown("## Selecting Data")
st.markdown("""
Configure row selection with the following properties:  
            
- `rowSelection`: Type of row selection, set to either 'single' or 'multiple' to enable selection. 'single' will use single row selection, such that when you select a row, any previously selected row gets unselected. 'multiple' allows multiple rows to be selected.  
- `rowMultiSelectWithClick`: Set to true to allow multiple rows to be selected with clicks. For example, if you click to select one row and then click to select another row, the first row will stay selected as well. Clicking a selected row in this mode will deselect the row. This is useful for touch devices where ^ Ctrl and ⇧ Shift clicking is not an option.  
- `suppressRowDeselection`: Set to true to prevent rows from being deselected if you hold down ^ Ctrl and click the row (i.e. once a row is selected, it remains selected until another row is selected in its place). By default the grid allows deselection of rows.  
- `suppressRowClickSelection`: If true, rows won't be selected when clicked. Use, for example, when you want checkbox selection or your managing selection from a custom component and don't want to select the row when the row is clicked.  
""")


editor_options = {
    "displayIndentGuides": False,
    "wrap": "free",
    "foldStyle": "markbegin",
    "enableLiveAutocompletion": True,
    "showGutter": True,
}

custom_buttons = [
    {
        "name": "Save",
        "feather": "Save",
        "hasText": True,
        "commands": ["save-state", ["response", "saved"]],
        "response": "saved",
        "style": {"bottom": "calc(50% - 4.25rem)", "right": "0.4rem"},
    },
    {
        "name": "Run",
        "feather": "Play",
        "primary": True,
        "hasText": True,
        "showWithIcon": True,
        "commands": ["submit"],
        "style": {"bottom": "0.44rem", "right": "0.4rem"},
    },
    {
        "name": "Command",
        "feather": "Terminal",
        "primary": True,
        "hasText": True,
        "commands": ["openCommandPallete"],
        "style": {"bottom": "3.5rem", "right": "0.4rem"},
    },
]


groupby = st.checkbox("Group by country and age", False)

gridOptions = {
    "rowSelection": {"mode": "multiRow"},
    "groupSelectsChildren": True,
    "autoGroupColumnDef": {
        "headerName": "My Group",
        "minWidth": 220,
        "cellRendererParams": {
            "suppressCount": False,
            "checkbox": True,
        },
    },
    "columnDefs": [
        {
            "field": "athlete",
            "minWidth": 150,
        },
        {"field": "country", "minWidth": 150, "rowGroup": groupby, "hide": groupby},
        {"field": "age", "maxWidth": 90, "rowGroup": groupby, "hide": groupby},
        {"field": "year", "maxWidth": 90},
        {"field": "date", "minWidth": 150},
        {"field": "sport", "minWidth": 150},
        {"field": "gold"},
        {"field": "silver"},
        {"field": "bronze"},
        {"field": "total"},
    ],
    "defaultColDef": {
        "flex": 1,
        "minWidth": 100,
    },
}
tabs = st.tabs(
    [
        "Grid",
        "GridOptions",
        "AgGridReturn.selected_data",
        "AgGridReturn.selected_groupedData",
    ]
)

with tabs[0]:
    response = AgGrid(df, gridOptions, key="grid1")

with tabs[1]:
    text = code_editor(
        json.dumps(gridOptions, indent=4),
        lang="json",
        props={"readOnly": False, "setOptions": editor_options},
        buttons=custom_buttons,
        height="300px",
    ).get("text", "")

    if text != "":
        gridOptions = json.loads(text)


with tabs[2]:
    selected_data = response.selected_data

    if selected_data is None:
        st.write("Nothing was selected!")
    else:
        st.write(response.selected_data)

with tabs[3]:
    selected_dataGroups = response.selected_dataGroups

    if not selected_dataGroups:
        st.write("Nothing was selected!")
    else:
        st.text("Showing first 10 groups: {")

        for i in response.selected_dataGroups[:10]:
            for k, v in i.items():
                cols = st.columns([4, 10])
                with cols[0]:
                    st.text(f"{tuple(k)}\t:")

                with cols[1]:
                    st.dataframe(v)

        st.text("...")
        st.text("}")
