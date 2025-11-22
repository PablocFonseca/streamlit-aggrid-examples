"""
AG-Grid Server Side Row Model Example with PolarsServerService

Demonstrates server-side operations with 10 million transaction records.
Features: infinite scrolling, sorting, filtering, grouping with lazy-loaded parquet file.
"""

import streamlit as st
from st_aggrid import AgGrid, JsCode
from st_aggrid.polars_server_service import PolarsServerService
import polars as pl
import time

st.set_page_config(page_title="Server Side Row Model - 10M Rows", layout="wide")


@st.cache_resource
def get_data_and_start_service():
    """Lazy load parquet file and start server-side service."""
    df = pl.scan_parquet("/Users/pablofonseca/dev/streamlit-aggrid/streamlit-aggrid-examples/backserver/dummy_data.parquet").collect()
    service = PolarsServerService(df, port=8000)
    time.sleep(1)
    return service, df.height


service, total_rows = get_data_and_start_service()

st.title("AG-Grid Server Side Row Model - 10 Million Rows")

st.markdown(f"""
### High-Performance Server-Side Grid
- **{total_rows:,} transaction records** loaded from parquet
- **Server-side operations**: sorting, filtering, grouping
- **Infinite scrolling** with 100-row blocks
- **Embedded FastAPI server** - Self-contained service

The `PolarsServerService` handles all data operations efficiently.
""")

datasource_js = JsCode("""
{
    getRows: function(params) {
        console.log('getRows: params = ', params);

        var request = {
            startRow: params.request.startRow,
            endRow: params.request.endRow,
            filterModel: params.request.filterModel,
            sortModel: params.request.sortModel,
            rowGroupCols: params.request.rowGroupCols || [],
            valueCols: params.request.valueCols || [],
            pivotCols: params.request.pivotCols || [],
            pivotMode: params.request.pivotMode || false,
            groupKeys: params.request.groupKeys || []
        };

        fetch('http://localhost:8000/getData', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(request)
        })
        .then(function(response) { return response.json(); })
        .then(function(data) {
            console.log('Received data:', data);
            var successParams = {
                rowData: data.rows,
                rowCount: data.lastRow
            };

            // If pivot result fields are returned, add them to the success params
            if (data.pivotResultFields && data.pivotResultFields.length > 0) {
                successParams.pivotResultFields = data.pivotResultFields;
            }

            params.success(successParams);
        })
        .catch(function(error) {
            console.error('Error:', error);
            params.fail();
        });
    }
}
""")

columnDefs = [
    {
        "field": "transaction_id",
        "headerName": "Transaction ID",
        "filter": "agTextColumnFilter",
        "sortable": True,
        "width": 150
    },
    {
        "field": "seller",
        "headerName": "Seller",
        "filter": "agSetColumnFilter",
        "filterParams": {
            "buttons": ["reset", "apply"],
            "values": JsCode("""
                function(params) {
                    fetch('http://localhost:8000/getUniqueValues/seller')
                        .then(response => response.json())
                        .then(data => params.success(data.values))
                        .catch(error => params.success([]));
                }
            """)
        },
        "sortable": True,
        "width": 200
    },
    {
        "field": "product",
        "headerName": "Product",
        "filter": "agSetColumnFilter",
        "filterParams": {
            "buttons": ["reset", "apply"],
            "values": JsCode("""
                function(params) {
                    fetch('http://localhost:8000/getUniqueValues/product')
                        .then(response => response.json())
                        .then(data => params.success(data.values))
                        .catch(error => params.success([]));
                }
            """)
        },
        "sortable": True,
        "width": 200
    },
    {
        "field": "category",
        "headerName": "Category",
        "filter": "agSetColumnFilter",
        "filterParams": {
            "buttons": ["reset", "apply"],
            "values": ["Electronics", "Clothing", "Food & Beverage", "Home & Garden",
                      "Sports & Outdoors", "Automotive", "Health & Beauty", "Books & Media",
                      "Toys & Games", "Office Supplies"]
        },
        "sortable": True,
        "enableRowGroup": True,
        "enablePivot": True,
        "width": 150
    },
    {
        "field": "customer_name",
        "headerName": "Customer",
        "filter": "agTextColumnFilter",
        "sortable": True,
        "width": 150
    },
    {
        "field": "country",
        "headerName": "Country",
        "filter": "agSetColumnFilter",
        "filterParams": {
            "buttons": ["reset", "apply"],
            "values": ["USA", "UK", "Canada", "Germany", "France", "Japan",
                      "Australia", "Brazil", "India", "China"]
        },
        "sortable": True,
        "enableRowGroup": True,
        "enablePivot": True,
        "width": 120
    },
    {
        "field": "region",
        "headerName": "Region",
        "filter": "agSetColumnFilter",
        "filterParams": {
            "buttons": ["reset", "apply"],
            "values": JsCode("""
                function(params) {
                    fetch('http://localhost:8000/getUniqueValues/region')
                        .then(response => response.json())
                        .then(data => params.success(data.values))
                        .catch(error => params.success([]));
                }
            """)
        },
        "sortable": True,
        "enableRowGroup": True,
        "enablePivot": True,
        "width": 150
    },
    {
        "field": "city",
        "headerName": "City",
        "filter": "agTextColumnFilter",
        "sortable": True,
        "width": 150
    },
    {
        "field": "quantity",
        "headerName": "Qty",
        "filter": "agNumberColumnFilter",
        "sortable": True,
        "enableValue": True,
        "aggFunc": "sum",
        "width": 100
    },
    {
        "field": "unit_price",
        "headerName": "Unit Price",
        "filter": "agNumberColumnFilter",
        "sortable": True,
        "enableValue": True,
        "aggFunc": "avg",
        "width": 120,
        "valueFormatter": JsCode("function(params) { return params.value ? '$' + params.value.toFixed(2) : ''; }")
    },
    {
        "field": "discount_percent",
        "headerName": "Discount %",
        "filter": "agSetColumnFilter",
        "filterParams": {
            "buttons": ["reset", "apply"],
            "values": [0, 5, 10, 15, 20, 25]
        },
        "sortable": True,
        "width": 120
    },
    {
        "field": "total_value",
        "headerName": "Total Value",
        "filter": "agNumberColumnFilter",
        "sortable": True,
        "enableValue": True,
        "aggFunc": "sum",
        "width": 130,
        "valueFormatter": JsCode("function(params) { return params.value ? '$' + params.value.toFixed(2) : ''; }")
    },
    {
        "field": "transaction_date",
        "headerName": "Date",
        "filter": "agDateColumnFilter",
        "sortable": True,
        "width": 150
    },
    {
        "field": "payment_method",
        "headerName": "Payment",
        "filter": "agSetColumnFilter",
        "filterParams": {
            "buttons": ["reset", "apply"],
            "values": ["Credit Card", "Debit Card", "PayPal", "Bank Transfer", "Cash"]
        },
        "sortable": True,
        "enableRowGroup": True,
        "enablePivot": True,
        "width": 140
    },
    {
        "field": "status",
        "headerName": "Status",
        "filter": "agSetColumnFilter",
        "filterParams": {
            "buttons": ["reset", "apply"],
            "values": ["Completed", "Pending", "Cancelled", "Refunded"]
        },
        "sortable": True,
        "enableRowGroup": True,
        "enablePivot": True,
        "width": 120
    },
    {
        "field": "shipping_cost",
        "headerName": "Shipping",
        "filter": "agNumberColumnFilter",
        "sortable": True,
        "enableValue": True,
        "aggFunc": "sum",
        "width": 120,
        "valueFormatter": JsCode("function(params) { return params.value ? '$' + params.value.toFixed(2) : ''; }")
    },
    {
        "field": "customer_rating",
        "headerName": "Rating",
        "filter": "agSetColumnFilter",
        "filterParams": {
            "buttons": ["reset", "apply"],
            "values": [1, 2, 3, 4, 5]
        },
        "sortable": True,
        "enableValue": True,
        "aggFunc": "avg",
        "width": 100
    },
    {
        "field": "is_repeat_customer",
        "headerName": "Repeat",
        "filter": "agSetColumnFilter",
        "filterParams": {
            "buttons": ["reset", "apply"],
            "values": [True, False]
        },
        "sortable": True,
        "width": 100
    },
    {
        "field": "is_gift",
        "headerName": "Gift",
        "filter": "agSetColumnFilter",
        "filterParams": {
            "buttons": ["reset", "apply"],
            "values": [True, False]
        },
        "sortable": True,
        "width": 90
    },
]

gridOptions = {
    "columnDefs": columnDefs,
    "rowModelType": "serverSide",
    "serverSideDatasource": datasource_js,
    "defaultColDef": {
        "flex": 1,
        "minWidth": 100,
        "resizable": True,
        "sortable": True,
        "filter": True,
        "floatingFilter": True,
    },
    "rowSelection": "multiple",
    "cacheBlockSize": 100,
    "maxBlocksInCache": 20,
    "rowBuffer": 0,
    "maxConcurrentDatasourceRequests": 2,
    "animateRows": True,
    "suppressRowClickSelection": True,

    # Enable Row Grouping
    "rowGroupPanelShow": "always",
    "suppressAggFuncInHeader": False,

    # Enable Pivoting
    "pivotMode": False,
    "pivotPanelShow": "always",

    # Enable Side Bar with columns, filters, and aggregations
    "sideBar": {
        "toolPanels": [
            {
                "id": "columns",
                "labelDefault": "Columns",
                "labelKey": "columns",
                "iconKey": "columns",
                "toolPanel": "agColumnsToolPanel",
                "toolPanelParams": {
                    "suppressRowGroups": False,
                    "suppressValues": False,
                    "suppressPivots": False,
                    "suppressPivotMode": False,
                }
            },
            {
                "id": "filters",
                "labelDefault": "Filters",
                "labelKey": "filters",
                "iconKey": "filter",
                "toolPanel": "agFiltersToolPanel"
            }
        ],
        "defaultToolPanel": "columns"
    },

    # Aggregation functions available
    "aggFuncs": {
        "sum": "sum",
        "min": "min",
        "max": "max",
        "count": "count",
        "avg": "avg"
    },

    # Auto-group column configuration
    "autoGroupColumnDef": {
        "headerName": "Group",
        "minWidth": 200,
        "cellRendererParams": {
            "suppressCount": False
        }
    },

    # Server-side group configuration
    "isServerSideGroup": JsCode("function(dataItem) { return dataItem.group === true; }"),
    "getServerSideGroupKey": JsCode("""
        function(dataItem) {
            // Find the first non-metadata field (not 'group' or 'childCount')
            var keys = Object.keys(dataItem);
            for (var i = 0; i < keys.length; i++) {
                var key = keys[i];
                if (key !== 'group' && key !== 'childCount') {
                    return dataItem[key];
                }
            }
            return null;
        }
    """),

    # Row ID for selection support
    "getRowId": JsCode("""
        function(params) {
            // For group rows, use the group key as ID
            if (params.data.group) {
                var keys = Object.keys(params.data);
                for (var i = 0; i < keys.length; i++) {
                    var key = keys[i];
                    if (key !== 'group' && key !== 'childCount') {
                        return 'group_' + params.data[key];
                    }
                }
            }
            // For data rows, use transaction_id
            return params.data.transaction_id;
        }
    """)
}

st.subheader("Transaction Data Grid")

response = AgGrid(
    data=None,
    gridOptions=gridOptions,
    height=600,
    allow_unsafe_jscode=True,
    enable_enterprise_modules=True,
    key="server_side_grid",
    theme="streamlit",
    show_toolbar=True
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Rows", f"{total_rows:,}")

with col2:
    if response and response.selected_rows is not None:
        st.metric("Selected Rows", len(response.selected_rows))
    else:
        st.metric("Selected Rows", 0)

with col3:
    status = "Running" if service.is_running() else "Stopped"
    st.metric("Service Status", status)

if response and response.selected_rows is not None and len(response.selected_rows) > 0:
    st.subheader("Selected Rows")
    st.dataframe(response.selected_rows, use_container_width=True)

with st.expander("Dataset Information"):
    st.markdown("""
    ### Transaction Dataset
    - **20 columns** with diverse data types
    - **Geographic data**: Country, Region, City
    - **Financial data**: Quantity, Price, Discount, Total Value
    - **Temporal data**: Transaction dates over 2 years
    - **Categories**: 10 product categories
    - **Metadata**: Payment methods, status, ratings, flags

    Perfect for testing:
    - Complex filtering (text, number, date, set filters)
    - Multi-column sorting
    - Grouping by category, country, region
    - Aggregations (sum, avg, count)
    - Large dataset performance
    """)

with st.expander("Usage Example"):
    st.code("""
import polars as pl
from st_aggrid.polars_server_service import PolarsServerService

# Lazy load parquet file
df = pl.scan_parquet("dummy_data.parquet").collect()

# Start service (server starts automatically)
service = PolarsServerService(df, port=8000)

# Configure AG Grid with server-side model
datasource_js = JsCode(...)  # Points to http://localhost:8000/getData
gridOptions = {"rowModelType": "serverSide", "serverSideDatasource": datasource_js}
AgGrid(data=None, gridOptions=gridOptions, enable_enterprise_modules=True)
    """, language="python")
