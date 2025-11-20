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

customMenuItem = JsCode(
    """
class CustomMenuItem {
    init(params) {
        this.eGui = document.createElement('div');
        this.eGui.innerHTML = `
            <span class="ag-menu-option-part ag-menu-option-icon" role="presentation"></span>
            <span class="ag-menu-option-part ag-menu-option-text">${params.name}</span>
            <span class="ag-menu-option-part ag-menu-option-shortcut"><button class="alert-button">${params.buttonValue}</button></span>
            <span class="ag-menu-option-part ag-menu-option-popup-pointer">
                ${params.subMenu ? '<span class="ag-icon ag-icon-small-right" unselectable="on" role="presentation"></span>' : ''}
            </span>
        `;
        this.eButton = this.eGui.querySelector('.alert-button');
        this.eventListener = () => alert(`${params.name} clicked`);
        this.eButton.addEventListener('click', this.eventListener);
    }
    getGui() {
        return this.eGui;
    }
    configureDefaults() {
        return true;
        }
    setActive(active){}
    setExpanded(expanded){}
    select(){}
    destroy() {
        if (this.eButton) {
            this.eButton.removeEventListener('click', this.eventListener);
        }
    }                                  
}
"""
)

gridOptions = {
    "columnTypes": {
        "date": {"valueFormatter": "new Date(value).toLocaleDateString()"},
        "currency": {
            "width": 150,
            "valueFormatter": JsCode(
                """function currencyFormatter(params) {  const value = Math.floor(params.value);  if (isNaN(value)) {    return "";  }  return "£" + value.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");}"""
            ),
        },
    },
    "columnDefs": [
        {
            "field": "athlete",
            "minWidth": 150,
            "headerCheckboxSelection": True,
            "checkboxSelection": True,
        },
        {
            "field": "age",
            "maxWidth": 90,
            "cellStyle": {"fontWeight": "bold"},
        },
        {
            "field": "Prize",
            "valueGetter": "Math.random() * 100000",
            "type": "currency",
            "contextMenuItems": [
                "copy",
                "chartRange",
                "separator",
                {
                    "name": "Alert!",
                    "menuItem": customMenuItem,
                    "action": JsCode("function () {console.log('alert clicked');}"),
                },
            ],
        },
        {"field": "country", "minWidth": 150},
        {"field": "year", "maxWidth": 90},
        {"field": "date", "minWidth": 150, "type": "date"},
        {"field": "sport", "minWidth": 150},
        {"field": "gold"},
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


cols = st.columns([2, 3])

with cols[0]:
    tab = st.tabs(["GridOptions"])

with tab[0]:
    response_dict = code_editor(
        json.dumps(gridOptions, indent=2, cls=JsCodeEncoder, ensure_ascii=True),
        lang="json",
        buttons=custom_buttons,
        options=options,
    )

with cols[1]:
    opt = response_dict["text"] or gridOptions
    tabs = st.tabs(["Grid", "Data "])

with tabs[0]:
    grid1 = AgGrid(
        data,
        opt,
        height=800,
        update_on=[],
        enable_enterprise_modules=True,
        allow_unsafe_jscode=True,
        key="fix3",
    )

with tabs[1]:
    st.markdown("#### Data Sample (top 100 records)")
    st.json(data.head(100).to_json(orient="records"), expanded=False)
    st.markdown("#### Data Description")
    st.markdown(data.describe().to_html(), unsafe_allow_html=True)
