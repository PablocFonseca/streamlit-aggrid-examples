"""
Data Input with Server Wins Strategy
=====================================

This example demonstrates using AgGrid as a data input control with the 'server_wins'
strategy for validation and calculated columns. The server maintains control over
data integrity while allowing user edits.

Features
--------
* Real-time validation of user inputs
* Automatic calculations for derived columns
* Server-side control ensures data integrity
* Session persistence maintains state across reruns

See Also
--------
* :doc:`AgGrid API Reference <../api/aggrid>`
* :doc:`GridOptionsBuilder <../api/grid_options_builder>`
"""

import streamlit as st
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid


st.set_page_config(layout="wide", page_title="Product Order Entry")

st.title("Product Order Entry System")
st.markdown("""
This example shows how to use AgGrid with **server_wins** strategy for data input:

* **Real-time validation** of user inputs
* **Automatic calculations** for derived columns
* **Server-side control** ensures data integrity
* **Session persistence** maintains state across reruns
""")

# Initialize the order entry dataframe
if "order_data" not in st.session_state:
    num_rows = 5
    st.session_state.order_data = pd.DataFrame(
        {
            "product_name": pd.Series([None] * num_rows, dtype="string"),
            "quantity": pd.Series([pd.NA] * num_rows, dtype="Int64"),
            "unit_price": pd.Series([pd.NA] * num_rows, dtype="Float64"),
            "total_price": pd.Series([0.0] * num_rows, dtype="Float64"),
            "discount_pct": pd.Series([0] * num_rows, dtype="Int64"),
            "final_price": pd.Series([0.0] * num_rows, dtype="Float64"),
        }
    )

if "validation_errors" not in st.session_state:
    st.session_state.validation_errors = []


def validate_and_calculate(args):
    """
    Callback function that validates user input and calculates derived columns.
    This runs on the server side after each edit, ensuring data integrity.

    Parameters
    ----------
    args : AgGridReturn
        The return object from AgGrid containing the updated data
    """
    data = args.data.copy()
    errors = []

    # Remove internal columns that AgGrid may add
    columns_to_remove = [col for col in data.columns if col.startswith("::")]
    if columns_to_remove:
        data = data.drop(columns=columns_to_remove)

    # Validation: Check for negative quantities
    if "quantity" in data.columns:
        negative_qty = data["quantity"] < 0
        if negative_qty.any():
            errors.append(
                f"WARNING: Negative quantities found in {negative_qty.sum()} row(s)"
            )
            # Correct negative values
            data.loc[negative_qty, "quantity"] = 0

    # Validation: Check for negative or zero unit prices
    if "unit_price" in data.columns:
        invalid_price = data["unit_price"] <= 0
        if invalid_price.any():
            errors.append(
                f"WARNING: Invalid unit prices found in {invalid_price.sum()} row(s)"
            )
            # Correct invalid prices
            data.loc[invalid_price, "unit_price"] = pd.NA

    # Validation: Check discount range (0-100%)
    if "discount_pct" in data.columns:
        invalid_discount = (data["discount_pct"] < 0) | (data["discount_pct"] > 100)
        if invalid_discount.any():
            errors.append(
                f"WARNING: Invalid discount percentage (must be 0-100) in {invalid_discount.sum()} row(s)"
            )
            # Correct invalid discounts
            data.loc[data["discount_pct"] < 0, "discount_pct"] = 0
            data.loc[data["discount_pct"] > 100, "discount_pct"] = 100

    # Calculate total_price = quantity × unit_price
    data["total_price"] = pd.to_numeric(data["quantity"], errors="coerce").fillna(
        0
    ) * pd.to_numeric(data["unit_price"], errors="coerce").fillna(0)

    # Calculate final_price with discount applied
    discount_multiplier = 1 - (
        pd.to_numeric(data["discount_pct"], errors="coerce").fillna(0) / 100
    )
    data["final_price"] = data["total_price"] * discount_multiplier

    # Round prices to 2 decimal places
    data["total_price"] = data["total_price"].round(2)
    data["final_price"] = data["final_price"].round(2)

    # Update session state
    st.session_state.order_data = data
    st.session_state.validation_errors = errors


# Configure grid options
grid_options = GridOptionsBuilder.from_dataframe(st.session_state.order_data)

# Configure editable columns
grid_options.configure_column(
    "product_name", header_name="Product Name", editable=True
)
grid_options.configure_column(
    "quantity", header_name="Quantity", editable=True,  type=["numericColumn"]
)
grid_options.configure_column(
    "unit_price",
    header_name="Unit Price ($)",
    editable=True,
    type=["numericColumn", "numberColumnFilter"],
    valueFormatter="value ? '$' + value.toFixed(2) : ''",
)
grid_options.configure_column(
    "discount_pct",
    header_name="Discount (%)",
    editable=True,
    type=["numericColumn"],
)

# Configure read-only calculated columns
grid_options.configure_column(
    "total_price",
    header_name="Total Price ($)",
    editable=False,
    type=["numericColumn"],
    valueFormatter="'$' + value.toFixed(2)",
    cellStyle={"backgroundColor": "#f0f0f0"},
)
grid_options.configure_column(
    "final_price",
    header_name="Final Price ($)",
    editable=False,
    
    type=["numericColumn"],
    valueFormatter="'$' + value.toFixed(2)",
    cellStyle={"backgroundColor": "#e8f5e9", "fontWeight": "bold"},
)

# Hide the internal auto_unique_id column
grid_options.configure_column("::auto_unique_id::", hide=True)

# Enable features
grid_options.configure_selection(selection_mode="multiple", use_checkbox=True)
grid_options.configure_grid_options(domLayout="normal", rowHeight=40)

# Display validation errors if any
if st.session_state.validation_errors:
    for error in st.session_state.validation_errors:
        st.warning(error)

# Render the grid
st.subheader("Order Entry Grid")
st.markdown(
    "*Edit the Product Name, Quantity, Unit Price, and Discount. Total and Final Price are calculated automatically.*"
)

grid_result = AgGrid(
    st.session_state.order_data,
    gridOptions=grid_options.build(),
    key="order_grid",
    callback=validate_and_calculate,
    server_sync_strategy="server_wins",
    try_to_convert_back_to_original_types=False,
    height=300,
    theme="streamlit",
    allow_unsafe_jscode=True,
)

# Display current data types
with st.expander("Data Types Information"):
    st.code(st.session_state.order_data.dtypes)

with st.expander("Show code", expanded=False):
    st.code("""
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import pandas as pd
import streamlit as st

# Initialize session state with order data
if "order_data" not in st.session_state:
    num_rows = 5
    st.session_state.order_data = pd.DataFrame({
        "product_name": pd.Series([None] * num_rows, dtype="string"),
        "quantity": pd.Series([pd.NA] * num_rows, dtype="Int64"),
        "unit_price": pd.Series([pd.NA] * num_rows, dtype="Float64"),
        "total_price": pd.Series([0.0] * num_rows, dtype="Float64"),
        "discount_pct": pd.Series([0] * num_rows, dtype="Int64"),
        "final_price": pd.Series([0.0] * num_rows, dtype="Float64"),
    })

# Define callback for automatic calculations
def validate_and_calculate(response):
    if response and response.data is not None:
        df = response.data
        # Calculate total_price = quantity * unit_price
        df["total_price"] = df["quantity"].fillna(0) * df["unit_price"].fillna(0)
        # Calculate final_price with discount
        df["final_price"] = df["total_price"] * (1 - df["discount_pct"].fillna(0) / 100)
        st.session_state.order_data = df

# Build grid options
grid_options = GridOptionsBuilder.from_dataframe(st.session_state.order_data)

# Configure editable columns
grid_options.configure_column("product_name", editable=True, header_name="Product Name")
grid_options.configure_column("quantity", editable=True, type=["numericColumn"])
grid_options.configure_column("unit_price", editable=True, type=["numericColumn"])
grid_options.configure_column("total_price", editable=False, type=["numericColumn"])
grid_options.configure_column("discount_pct", editable=True, type=["numericColumn"])
grid_options.configure_column("final_price", editable=False, type=["numericColumn"])

# Configure selection
grid_options.configure_selection(selection_mode="multiple", use_checkbox=True)

# Display the grid
grid_result = AgGrid(
    st.session_state.order_data,
    gridOptions=grid_options.build(),
    key="order_grid",
    callback=validate_and_calculate,
    server_sync_strategy="server_wins",
    height=300,
    allow_unsafe_jscode=True
)
""", language="python")

st.divider()

# Action buttons
col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    if st.button("Add Row"):
        new_row = pd.DataFrame(
            {
                "product_name": [None],
                "quantity": [pd.NA],
                "unit_price": [pd.NA],
                "total_price": [0.0],
                "discount_pct": [0],
                "final_price": [0.0],
            }
        )
        st.session_state.order_data = pd.concat(
            [st.session_state.order_data, new_row], ignore_index=True
        )
        st.rerun()

with col2:
    if st.button("Reset"):
        num_rows = 5
        st.session_state.order_data = pd.DataFrame(
            {
                "product_name": pd.Series([None] * num_rows, dtype="string"),
                "quantity": pd.Series([pd.NA] * num_rows, dtype="Int64"),
                "unit_price": pd.Series([pd.NA] * num_rows, dtype="Float64"),
                "total_price": pd.Series([0.0] * num_rows, dtype="Float64"),
                "discount_pct": pd.Series([0] * num_rows, dtype="Int64"),
                "final_price": pd.Series([0.0] * num_rows, dtype="Float64"),
            }
        )
        st.session_state.validation_errors = []
        st.rerun()


# Display summary statistics
st.subheader("Order Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_items = st.session_state.order_data["quantity"].sum()
    st.metric("Total Items", f"{total_items if pd.notna(total_items) else 0:.0f}")

with col2:
    subtotal = st.session_state.order_data["total_price"].sum()
    st.metric("Subtotal", f"${subtotal:.2f}")

with col3:
    total_discount = subtotal - st.session_state.order_data["final_price"].sum()
    st.metric("Total Discount", f"${total_discount:.2f}")

with col4:
    grand_total = st.session_state.order_data["final_price"].sum()
    st.metric("Grand Total", f"${grand_total:.2f}") 

# Display the current data
with st.expander("View Raw Data"):
    st.dataframe(st.session_state.order_data, use_container_width=True)
