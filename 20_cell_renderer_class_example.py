import datetime

import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode, GridUpdateMode


now = int(datetime.datetime.now().timestamp())
start_ts = now - 3 * 30 * 24 * 60 * 60


@st.cache_data()
def make_data():
    df = pd.DataFrame(
        {
            "timestamp": np.random.randint(start_ts, now, 20),
            "side": [np.random.choice(["buy", "sell"]) for i in range(20)],
            "base": [np.random.choice(["JPY", "GBP", "CAD"]) for i in range(20)],
            "quote": [np.random.choice(["EUR", "USD"]) for i in range(20)],
            "amount": list(
                map(
                    lambda a: round(a, 2),
                    np.random.rand(20) * np.random.randint(1, 1000, 20),
                )
            ),
            "price": list(
                map(
                    lambda p: round(p, 5),
                    np.random.rand(20) * np.random.randint(1, 10, 20),
                )
            ),
            "clicked": [""] * 20,
        }
    )
    df["cost"] = round(df.amount * df.price, 2)
    df.insert(
        0,
        "datetime",
        df.timestamp.apply(lambda ts: datetime.datetime.fromtimestamp(ts)),
    )

    return df.sort_values("timestamp").drop("timestamp", axis=1)


# an example based on https://www.ag-grid.com/javascript-data-grid/component-cell-renderer/#simple-cell-renderer-example
jsfnc = """
class BtnCellRenderer {
    init(params) {
        this.params = params;
        this.eGui = document.createElement('div');
        this.eGui.innerHTML = `
         <span>
            <button id='click-button' 
                class='btn-simple' 
                style='color: ${this.params.color}; background-color: ${this.params.background_color}'>Click!</button>
         </span>
        `;
        this.eButton = this.eGui.querySelector('#click-button');
        this.btnClickedHandler = this.btnClickedHandler.bind(this);
        this.eButton.addEventListener('click', this.btnClickedHandler);
    }

    getGui() {
        return this.eGui;
    }

    refresh() {
        return true;
    }

    destroy() {
        if (this.eButton) {
            this.eGui.removeEventListener('click', this.btnClickedHandler);
        }
    }

    btnClickedHandler(event) {
        if (confirm('Are you sure you want to CLICK?') == true) {
            if(this.params.getValue() == 'clicked') {
                this.refreshTable('');
            } else {
                this.refreshTable('clicked');
            }
                console.log(this.params);
                console.log(this.params.getValue());
            }
        }

    refreshTable(value) {
        this.params.setValue(value);
    }
};
"""
BtnCellRenderer = JsCode(jsfnc)

df = make_data()
gb = GridOptionsBuilder.from_dataframe(df)

gb.configure_default_column(editable=True)
grid_options = gb.build()

grid_options["columnDefs"].append(
    {
        "field": "clicked",
        "headerName": "Clicked",
        "cellRenderer": BtnCellRenderer,
        "cellRendererParams": {
            "color": "red",
            "background_color": "black",
        },
    }
)

st.title("Custom cellRenderer Class Example")

st.markdown(
    f"""
This example uses a custom class `BtnCellRenderer`, that implements [ICellRendererComp](https://www.ag-grid.com/javascript-data-grid/component-cell-renderer/#custom-components) interface.
"""
)

with st.expander("*BtnCellRenderer* implementation", expanded=False):
    st.markdown(
        f"""
    ```javascript
    {jsfnc}
    ```
    """
    )


st.markdown(
    """
The custom renderer is then added as an extra column on gridOptions:

```python
grid_options['columnDefs'].append({
    "field": "clicked",
    "headerName": "Clicked",
    "cellRenderer": BtnCellRenderer
})
```
clicked cells will appear in the response dataframe
"""
)

tabs = st.tabs(["AgGrid", "Response Data"])

with tabs[0]:
    response = AgGrid(
        df,
        theme="streamlit",
        key="table1",
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        reload_data=False,
        try_to_convert_back_to_original_types=False,
    )
with tabs[1]:
    st.write(response.data)

st.markdown("#### Clicked rows:")

clicked = response.data[response.data.clicked == "clicked"]

if clicked.empty:
    st.write("Nothing was clicked")
else:
    st.write(clicked)
