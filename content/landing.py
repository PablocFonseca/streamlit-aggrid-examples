"""
AG Grid Finance Demo - Streamlit Implementation
Adapted from: https://github.com/ag-grid/ag-grid-demos/blob/main/finance/typescript/src/main.ts
"""

import streamlit as st
from st_aggrid import AgGrid, JsCode

# Import financial data from shared assets
from assets.finance_data import get_financial_data

# Configuration constants
DEFAULT_UPDATE_INTERVAL = 90  # milliseconds
PERCENTAGE_CHANGE = 20  # maximum percentage for price fluctuations

st.set_page_config(page_title="AG Grid Finance Demo", layout="wide")

# Number formatter JavaScript code
number_formatter = JsCode("""
function(params) {
    if (params.value == null) return '';
    const formatter = new Intl.NumberFormat('en-US', {
        style: 'decimal',
        maximumFractionDigits: 2,
    });
    return formatter.format(params.value);
}
""")

# P&L Value Getter
pl_value_getter = JsCode("""
function(params) {
    if (!params.data) return null;
    return params.data.quantity * (params.data.price / params.data.purchasePrice);
}
""")

# Total Value Getter
total_value_getter = JsCode("""
function(params) {
    if (!params.data) return null;
    return params.data.quantity * params.data.price;
}
""")

# Sparkline tooltip renderer
sparkline_tooltip_renderer = JsCode("""
function(params) {
    return {
        title: params.datum.x,
        content: params.yValue.toFixed(2)
    };
}
""")

# Ticker cell renderer with company logo
ticker_cell_renderer = JsCode("""
class TickerCellRenderer {
    init(params) {
        this.eGui = document.createElement('div');
        this.eGui.style.display = 'flex';
        this.eGui.style.alignItems = 'center';
        this.eGui.style.gap = '8px';

        if (params.data) {
            // Company logo
            const imgElement = document.createElement('img');
            imgElement.src = `https://www.ag-grid.com/example/finance/logos/${params.data.ticker}.png`;
            imgElement.style.width = '20px';
            imgElement.style.height = '20px';
            imgElement.style.borderRadius = '32px';
            imgElement.onerror = function() {
                // Fallback if image doesn't exist
                this.style.display = 'none';
            };
            this.eGui.appendChild(imgElement);

            // Ticker symbol
            const tickerElement = document.createElement('b');
            tickerElement.className = 'custom-ticker';
            tickerElement.textContent = params.data.ticker;
            this.eGui.appendChild(tickerElement);

            // Company name
            const nameElement = document.createElement('span');
            nameElement.className = 'ticker-name';
            nameElement.style.color = '#888';
            nameElement.style.marginLeft = '4px';
            nameElement.textContent = params.data.name;
            this.eGui.appendChild(nameElement);
        }
    }

    getGui() {
        return this.eGui;
    }

    refresh(params) {
        return false;
    }
}
""")

# Real-time price update function
update_prices_function = JsCode(f"""
function(params) {{
    const PERCENTAGE_CHANGE = {PERCENTAGE_CHANGE};
    const UPDATE_INTERVAL = {DEFAULT_UPDATE_INTERVAL};

    setInterval(() => {{
        const gridApi = params.api;
        let rowData = [];

        // Get only leaf nodes (non-grouped rows)
        gridApi.forEachLeafNode(node => rowData.push(node.data));

        // Update 10% of rows randomly
        const updatedData = rowData.map(item => {{
            const isRandomChance = Math.random() < 0.1;

            if (!isRandomChance) {{
                return item;
            }}

            const rnd = (Math.random() * PERCENTAGE_CHANGE) / 100;
            const change = Math.random() > 0.5 ? 1 - rnd : 1 + rnd;
            let price = item.price < 10
                ? item.price * change
                : Math.random() > 0.1 ? item.price * change : Math.random() * 40 + 10;

            // Update timeline array (sliding window)
            const timeline = item.timeline.slice(1).concat(Number(price.toFixed(2)));

            return {{
                ...item,
                price: price,
                timeline: timeline
            }};
        }});

        // Apply transaction to update grid
        gridApi.applyTransactionAsync({{
            update: updatedData
        }});
    }}, UPDATE_INTERVAL);
}}
""")

# Get row ID function
get_row_id = JsCode("""
function(params) {
    return params.data.ticker;
}
""")


def main():
    # Hero Section
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem 0 3rem 0;">
            <h1 style="font-size: 3.5rem; font-weight: 700; line-height: 1.2; margin-bottom: 1rem;">
                The World's Best Grid,<br>in your Streamlit Apps.
            </h1>
            <p style="font-size: 1.5rem; color: #666; margin-top: 1rem;">
                Wrap in AG Grid. Skip the boilerplate. Impress your users.
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Load data
    df = st.cache_data(get_financial_data)()

    # Define column definitions as a list of dictionaries (matching TypeScript structure)
    column_defs = [
        {
            "field": "ticker",
            "headerName": "Ticker",
            "cellRenderer": ticker_cell_renderer,
            "minWidth": 350,
            "initialWidth": 350,
        },
        {
            "field": "timeline",
            "headerName": "Timeline",
            "sortable": False,
            "filter": False,
            "cellRenderer": "agSparklineCellRenderer",
            "cellRendererParams": {
                "sparklineOptions": {
                    "type": "bar",
                    "direction": "vertical",
                    "axis": {
                        "strokeWidth": 0,
                    },
                    "tooltip": {
                        "renderer": sparkline_tooltip_renderer,
                    },
                }
            },
            "minWidth": 300,
        },
        {
            "field": "instrument",
            "headerName": "Instrument",
            "cellDataType": "text",
            "type": "rightAligned",
            "minWidth": 100,
            "initialWidth": 100,
            "enableRowGroup": True,
        },
        {
            "field": "quantity",
            "headerName": "Quantity",
            "valueFormatter": number_formatter,
            "type": "rightAligned",
        },
        {
            "field": "purchasePrice",
            "headerName": "Purchase Price",
            "valueFormatter": number_formatter,
            "type": "rightAligned",
        },
        {
            "field": "price",
            "headerName": "Price",
            "valueFormatter": number_formatter,
            "type": "rightAligned",
            "cellRenderer": "agAnimateShowChangeCellRenderer",
        },
        {
            "colId": "p&l",
            "headerName": "P&L",
            "cellDataType": "number",
            "filter": "agNumberColumnFilter",
            "type": "rightAligned",
            "cellRenderer": "agAnimateShowChangeCellRenderer",
            "valueGetter": pl_value_getter,
            "valueFormatter": number_formatter,
            "aggFunc": "sum",
            "minWidth": 140,
            "initialWidth": 140,
        },
        {
            "colId": "totalValue",
            "headerName": "Total Value",
            "type": "rightAligned",
            "cellDataType": "number",
            "filter": "agNumberColumnFilter",
            "valueGetter": total_value_getter,
            "cellRenderer": "agAnimateShowChangeCellRenderer",
            "valueFormatter": number_formatter,
            "aggFunc": "sum",
            "minWidth": 160,
            "initialWidth": 160,
        },
    ]

    # Build grid options as a dictionary (matching TypeScript structure)
    grid_options = {
        "columnDefs": column_defs,
        "defaultColDef": {
            "flex": 1,
            "filter": True,
            "enableValue": True,
        },
        "onFirstDataRendered": update_prices_function,
        "cellSelection": True,
        "enableCharts": True,
        "animateRows": True,
        "rowGroupPanelShow": "always",
        "groupDefaultExpanded": -1,

    "statusBar": {
    "statusPanels": [
      { "statusPanel": "agTotalRowCountComponent" },
      { "statusPanel": "agTotalAndFilteredRowCountComponent" },
      { "statusPanel": "agFilteredRowCountComponent" },
      { "statusPanel": "agSelectedRowCountComponent" },
      { "statusPanel": "agAggregationComponent" },
    ],
  },
    }

    AgGrid(
        df,
        gridOptions=grid_options,
        height=400,
        theme="alpine",
        allow_unsafe_jscode=True,
        enable_enterprise_modules="enterprise+AgCharts",
        update_mode="NO_UPDATE",
        use_json_serialization=True,
    )


if __name__ == "__main__":
    main()
