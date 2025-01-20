import streamlit as st
import json
import pandas as pd

import st_aggrid
from st_aggrid import AgGrid, JsCode
import importlib

importlib.invalidate_caches()
importlib.reload(st_aggrid)

st.set_page_config(layout="wide")


with st.expander("# st.column_config.Column"):
    data_df = pd.DataFrame(
        {
            "widgets": ["st.selectbox", "st.number_input", "st.text_area", "st.button"],
        }
    )

    column_config = {
        "widgets": st.column_config.Column(
            "Streamlit Widgets",
            help="Streamlit **widget** commands 🎈",
            width="large",
            required=True,
        )
    }

    st.data_editor(
        data_df,
        column_config=column_config,
        hide_index=True,
        num_rows="dynamic",
    )

    grid_options = {
        "columnDefs": [
            dict(
                width=34,
                cellRenderer="agCheckboxCellRenderer",
                resizable=False,
                editable=True,
                cellEditor="agCheckboxCellEditor",
                field="data.selected",
                valueGetter="data.selected ?? false",
            ),
            st_aggrid.column_factory.convert_st_column("widgets", column_config["widgets"]),
        ]
    }

    AgGrid(data_df, gridOptions=grid_options, allow_unsafe_jscode=True)

data_df = pd.DataFrame(
    {
        "price": [20, 950, 250, 500],
    }
)

column_config = {
        "price": st.column_config.NumberColumn(
            "Price (in USD)",
            help="The price of the product in USD",
            min_value=0,
            max_value=1000,
            step=1,
            format="$%d",
        )}

st.data_editor(
    data_df,
    column_config=column_config,
    hide_index=True,
)


grid_options = {
    "columnDefs": [
        st_aggrid.column_factory.convert_st_NumberColumn("price", column_config["price"]),
    ]
}

grid_options

# st.markdown(
#     unsafe_allow_html=True,
#     body="""<div class="st-emotion-cache-1clt8w9 e2wxzia1"><div data-testid="stElementToolbarButton"><div data-testid="stTooltipHoverTarget" class="stTooltipHoverTarget" id="bui15__anchor" style="display: flex; flex-direction: row; justify-content: flex-end;"><button kind="elementToolbar" data-testid="stBaseButton-elementToolbar" aria-label="Download as CSV" class="st-emotion-cache-bmpq5o ef3psqc0"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" data-testid="stElementToolbarButtonIcon" class="eyeqlp53 st-emotion-cache-jl9d4a ex0cdmw0"><rect width="24" height="24" fill="none"></rect><path d="M18 15v3H6v-3H4v3c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2v-3h-2zm-1-4l-1.41-1.41L13 12.17V4h-2v8.17L8.41 9.59 7 11l5 5 5-5z"></path></svg></button></div></div><div data-testid="stElementToolbarButton"><div data-testid="stTooltipHoverTarget" class="stTooltipHoverTarget" id="bui16__anchor" style="display: flex; flex-direction: row; justify-content: flex-end;"><button kind="elementToolbar" data-testid="stBaseButton-elementToolbar" aria-label="Search" class="st-emotion-cache-bmpq5o ef3psqc0"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" data-testid="stElementToolbarButtonIcon" class="eyeqlp53 st-emotion-cache-jl9d4a ex0cdmw0"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"></path></svg></button></div></div><div data-testid="stElementToolbarButton"><div data-testid="stTooltipHoverTarget" class="stTooltipHoverTarget" id="bui17__anchor" style="display: flex; flex-direction: row; justify-content: flex-end;" aria-describedby="bui17"><button kind="elementToolbar" data-testid="stBaseButton-elementToolbar" aria-label="Fullscreen" class="st-emotion-cache-bmpq5o ef3psqc0"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" data-testid="stElementToolbarButtonIcon" class="eyeqlp53 st-emotion-cache-jl9d4a ex0cdmw0"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"></path></svg></button></div></div></div>""",
# )


AgGrid(data_df, gridOptions=grid_options, allow_unsafe_jscode=True)






st.stop()


st.cache_data()


def get_data():
    with open("streamlit-aggrid-examples/sparkline_data.json", "r") as f:
        return json.load(f)


data = pd.read_json("streamlit-aggrid-examples/sparkline_data.json")


grid_options = {
    "columnDefs": [
        {"field": "symbol", "maxWidth": 120},
        {"field": "name", "minWidth": 250},
        {
            "field": "change",
            "cellRenderer": "agSparklineCellRenderer",
            "cellRendererParams": {
                "sparklineOptions": {
                    "type": "area",
                    "fill": "rgba(216, 204, 235, 0.3)",
                    "line": {
                        "stroke": "rgb(119,77,185)",
                    },
                    "highlightStyle": {
                        "fill": "rgb(143,185,77)",
                    },
                    "axis": {
                        "stroke": "rgb(204, 204, 235)",
                    },
                },
            },
        },
        {
            "field": "volume",
            "type": "numericColumn",
            "maxWidth": 140,
        },
    ],
    "defaultColDef": {
        "flex": 1,
        "minWidth": 100,
    },
}

AgGrid(data, gridOptions=grid_options)


c = st.column_config.Column(label="aa")

import st_aggrid.column_factory
from st_aggrid.grid_options import ColumnDefinition


class ColumnDef(dict):
    def __init__(self, field):
        self["field"] = field

    @classmethod
    def from_st_column_config(cls, field: str, column_config: dict):
        c = ColumnDef(field=field)

        if label := column_config.get("label", None):
            c["headerName"] = label

        if width := column_config.get("width", None):
            # l 432, m 232, s 107
            match width:
                case "large":
                    c["width"] = 432
                case "medium":
                    c["width"] = 232
                case "small":
                    c["width"] = 107
                case _:
                    pass

        if help := column_config.get("help", None):
            c["tooltipValueGetter"] = JsCode(f"function(){{return `{help}`}}")

        if (disabled := column_config.get("disabled", None)) is not None:
            c["editable"] = not disabled

        if (required := column_config.get("required", None)) is not None:
            # TODO:implement requiredCellEditor https://plnkr.co/edit/qT2fOz7L5mzG846K?preview
            pass

        if (default := column_config.get("default", None)) is not None:
            # TODO: implement behavior for when num_rows = dynamic https://blog.ag-grid.com/add-new-rows-using-a-pinned-row-at-the-top-of-the-grid/
            pass

        if (max_chars := column_config.get("max_chars", None)) is not None:
            # TODO: implement behavior to limit max char, inherit cell editor on react side.?
            pass

        if (validate := column_config.get("validate", None)) is not None:
            # TODO: implement behavior custom cell editor to validate input.
            pass

        """
        st.column_config.NumberColumn:
          format (str or None)
          min_value (int, float, or None)
          max_value (int, float, or None)
          step (int, float, or None)

          st.column_config.CheckboxColumn

          st.column_config.SelectboxColumn:
          options (Iterable of str or None): The options that can be selected during editing. If None (default), this will be inferred from the underlying dataframe column if its dtype is "category"

          st.column_config.DatetimeColumn:
          format
          min_value
          max_value
          step
          timezone
        """

        return c




data_df = pd.DataFrame(
    {
        "widgets": ["st.selectbox", "st.number_input", "st.text_area", "st.button"],
    }
)

zz = {
    "widgets": st.column_config.Column(
        "Streamlit Widgets",
        help="Streamlit **widget** commands 🎈",
        width="small",
        required=True,
        disabled=False,
    )
}

yy = ColumnDef.from_st_column_config("widgets", zz["widgets"])

st.write(yy)
st.data_editor(
    data_df,
    column_config=zz,
    hide_index=True,
    num_rows="dynamic",
)


st.write(type(zz["widgets"]))


import pandas as pd
import streamlit as st

data_df = pd.DataFrame(
    {
        "category": [
            "📊 Data Exploration",
            "📈 Data Visualization",
            "🤖 LLM",
            "📊 Data Exploration",
        ],
    }
)

st.data_editor(
    data_df,
    column_config={
        "category": st.column_config.SelectboxColumn(
            "App Category",
            help="The category of the app",
            width="medium",
            options=[
                "📊 Data Exploration",
                "📈 Data Visualization",
                "🤖 LLM",
            ],
            required=True,
        )
    },
    hide_index=True,
)


st.stop()
"""var TextCellEditorInput = class {
  getTemplate() {
    return (
      /* html */
      `<ag-input-text-field class="ag-cell-editor" data-ref="eInput"></ag-input-text-field>`
    );
  }
  getAgComponents() {
    return [AgInputTextFieldSelector];
  }
  init(eInput, params) {
    this.eInput = eInput;
    this.params = params;
    if (params.maxLength != null) {
      eInput.setMaxLength(params.maxLength);
    }
  }
  getValue() {
    const value = this.eInput.getValue();
    if (!_exists(value) && !_exists(this.params.value)) {
      return this.params.value;
    }
    return this.params.parseValue(value);
  }
  getStartValue() {
    const formatValue = this.params.useFormatter || this.params.column.getColDef().refData;
    return formatValue ? this.params.formatValue(this.params.value) : this.params.value;
  }
  setCaret() {
    const value = this.eInput.getValue();
    const len = _exists(value) && value.length || 0;
    if (len) {
      this.eInput.getInputElement().setSelectionRange(len, len);
    }
  }
};"""
