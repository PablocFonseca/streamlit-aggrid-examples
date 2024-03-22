from code_editor import code_editor
from st_aggrid import AgGrid, JsCode
from st_aggrid.shared import JsCodeEncoder

import streamlit as st
import json
import pandas as pd

try:
    st.set_page_config(layout="wide")
except:
    pass

gridOptions = {
    "columnTypes": {
        "date": {"valueFormatter": "new Date(value).toLocaleDateString()"},
    },
    "columnDefs": [
        {
            "field": "athlete",
            "minWidth": 150,
            "headerCheckboxSelection": True,
            "checkboxSelection": True,
            "pinned": "left",
        },
        {
            "field": "age",
            "maxWidth": 90,
            "cellStyle": {"fontWeight": "bold"},
        },
        {
            "field": "Birth Year",
            "valueGetter": "data.year - data.age",
        },
        {"field": "country", "minWidth": 150},
        {"field": "year", "maxWidth": 90},
        {"field": "date", "minWidth": 150, "type": "date"},
        {"field": "sport", "minWidth": 150},
        {"field": "gold", "type": "numericColumn"},
        {"field": "silver"},
        {"field": "bronze"},
        {"field": "total"},
    ],
    "defaultColDef": {
        "flex": 1,
        "minWidth": 100,
        "filter": True,
        "enableRowGroup": True,
        "enablePivot": True,
        "enableValue": True,
    },
    "enableRangeSelection": True,
    "pagination": True,
    "rowSelection": "multiple",
    "suppressRowClickSelection": True,
    "suppressColumnMoveAnimation": True,
    "statusBar": {
        "statusPanels": [
            {"statusPanel": "agTotalAndFilteredRowCountComponent"},
            {"statusPanel": "agTotalRowCountComponent"},
            {"statusPanel": "agFilteredRowCountComponent"},
            {"statusPanel": "agSelectedRowCountComponent"},
            {"statusPanel": "agAggregationComponent"},
        ]
    },
    "sideBar": {
        "toolPanels": [
            {
                "id": "columns",
                "labelDefault": "Columns",
                "labelKey": "columns",
                "iconKey": "columns",
                "toolPanel": "agColumnsToolPanel",
                "minWidth": 225,
                "maxWidth": 225,
                "width": 225,
            },
            {
                "id": "filters",
                "labelDefault": "Filters",
                "labelKey": "filters",
                "iconKey": "filter",
                "toolPanel": "agFiltersToolPanel",
                "minWidth": 180,
                "maxWidth": 400,
                "width": 250,
            },
        ],
        "position": "left",
        "defaultToolPanel": "filters",
    },
    "getContextMenuItems": JsCode(
        """function(params){
                                return [
                                    ...(params.defaultItems || []),
                                    "separator",
                                    "chartRange",
                                    "separator",
                                    {
                                    "name": "Shout this row!",
                                    "action": function(params) { console.dir(params); alert(`${params.node.data.athlete} won ${params.node.data.total} medal(s) at age ${params.node.data.age}! \\nClicked Cell Value: ${params.value}`)},
                                    "icon": '<img src="https://cdn-icons-png.flaticon.com/128/77/77519.png" width="16" height="16">'
                                  }
                                ]}"""
    ),
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

options = {
    "displayIndentGuides": False,
    "highlightIndentGuides": True,
    "wrap": "free",
    "foldStyle": "markbegin",
    "enableLiveAutocompletion": True,
}


@st.cache_data()
def getData():
    import pathlib

    path = pathlib.Path(__file__).parent / "olympic-winners.json"
    data = pd.read_json(path)
    return data


data = getData()

if st.button("Reverse"):
    data = data.sort_values("year")

cols = st.columns([2, 3])

with cols[0]:
    tab = st.tabs(["GridOptions", "Data"])

with tab[0]:
    response_dict = code_editor(
        json.dumps(gridOptions, indent=2, cls=JsCodeEncoder, ensure_ascii=True),
        lang="json",
        buttons=custom_buttons,
        options=options,
    )

with tab[1]:
    grid0 = AgGrid(
        data,
        height=400,
        key="grid0",
        editable=True,
        suppressMovableColumns=True,
        filter=True,
        sortable=False,
        autoSizeStrategy=dict(type="fitCellContents",  )
    )


with cols[1]:
    opt = response_dict["text"] or gridOptions
    tabs = st.tabs(["Grid", "Received Data ", "Response"])

with tabs[0]:
    grid1 = AgGrid(
        grid0.data,
        opt,
        height=800,
        update_on=["stateChanged"],
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        key="fix3",
    )

with tabs[1]:
    st.markdown("#### Data Sample (top 100 records)")
    st.json(data.head(100).to_json(orient="records"), expanded=False)
    st.markdown("#### Data Description")
    st.markdown(data.describe().to_html(), unsafe_allow_html=True)

with tabs[2]:
    st.write(grid1.grid_response)
