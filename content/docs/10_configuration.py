"""
Basic AgGrid Configuration
==========================

This guide demonstrates how to configure AgGrid using GridOptionsBuilder for common use cases.
Based on the AG Grid deep dive guide: https://ag-grid.com/react-data-grid/deep-dive/
"""

import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import numpy as np

st.set_page_config(page_title="Basic Configuration", layout="wide")

# ============================================================================
# SECTION CONTROL - Set to True/False to enable/disable sections
# ============================================================================
SECTIONS = {
    'overview': True,
    'gridoptionsbuilder_basics': True,
    'default_column_configuration': True,
    'column_configuration': True,
    'selection': True,
    'pagination': True,
    'side_bar': True,
    'complete_example': True,
}

# Sidebar navigation/index
with st.sidebar:
    st.markdown('''
    <div class="sidebar-nav-section">On this page</div>
    <div class="sidebar-nav-container">
        <a href="#overview" class="sidebar-nav-link">Overview</a>
        <a href="#gridoptionsbuilder-basics" class="sidebar-nav-link">GridOptionsBuilder Basics</a>
        <a href="#default-column-configuration" class="sidebar-nav-link">Default Column Configuration</a>
        <a href="#column-configuration" class="sidebar-nav-link">Column Configuration</a>
        <a href="#selection" class="sidebar-nav-link">Selection</a>
        <a href="#pagination" class="sidebar-nav-link">Pagination</a>
        <a href="#side-bar" class="sidebar-nav-link">Side Bar</a>
        <a href="#complete-example" class="sidebar-nav-link">Complete Example</a>
    </div>
    ''', unsafe_allow_html=True)

st.title("Basic AgGrid Configuration")

st.markdown("""
This guide demonstrates how to configure AgGrid using the `GridOptionsBuilder` helper class.
GridOptionsBuilder provides a convenient Python API to build AG Grid configuration options.
""")

# Create sample data
@st.cache_data
def get_sample_data():
    np.random.seed(42)
    return pd.DataFrame({
        'Employee': ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince',
                     'Edward Norton', 'Fiona Apple', 'George Martin', 'Helen Troy'],
        'Department': ['Engineering', 'Sales', 'Engineering', 'Marketing',
                      'Sales', 'Engineering', 'Marketing', 'Sales'],
        'Age': [28, 35, 42, 31, 45, 29, 38, 33],
        'Salary': [75000, 65000, 95000, 70000, 80000, 78000, 72000, 68000],
        'Start Date': pd.date_range('2020-01-01', periods=8, freq='3M'),
        'Performance': np.random.choice(['Excellent', 'Good', 'Average'], 8)
    })

df = get_sample_data()


# ============================================================================
# SECTION FUNCTIONS
# ============================================================================

def section_overview():
    """Overview Section"""
    st.header("Overview", anchor="overview")

    st.markdown("""
    The `GridOptionsBuilder` is a helper class that simplifies creating AG Grid configurations.
    Instead of manually building dictionaries, you can use its methods to configure the grid in a more Pythonic way.

    The typical workflow is:
    1. Create a builder instance from a DataFrame
    2. Configure grid options using builder methods
    3. Build the final configuration dictionary
    4. Pass it to AgGrid
    """)


def section_gridoptionsbuilder_basics():
    """GridOptionsBuilder Basics Section"""
    st.header("GridOptionsBuilder Basics", anchor="gridoptionsbuilder-basics")

    st.markdown("""
    The most common way to start is by creating a builder from a DataFrame. This automatically
    generates column definitions based on your data types.
    """)

    with st.expander("Show code", expanded=False):
        st.code("""
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd

# Create sample data
df = pd.DataFrame({
    'Employee': ['Alice', 'Bob', 'Charlie'],
    'Department': ['Engineering', 'Sales', 'Marketing'],
    'Salary': [75000, 65000, 70000]
})

# Create builder from dataframe
gb = GridOptionsBuilder.from_dataframe(df)

# Build the options
gridOptions = gb.build()

# Display the grid
AgGrid(df, gridOptions=gridOptions)
""", language="python")

    st.markdown("**Output:**")

    gb_basic = GridOptionsBuilder.from_dataframe(df)
    gridOptions_basic = gb_basic.build()
    AgGrid(df, gridOptions=gridOptions_basic, height=250, key="basic_example")


def section_default_column_configuration():
    """Default Column Configuration Section"""
    st.header("Default Column Configuration", anchor="default-column-configuration")

    st.markdown("""
    Use `configure_default_column()` to set properties that apply to all columns by default.
    This is useful for enabling features like sorting, filtering, and resizing across all columns.
    """)

    with st.expander("Show code", expanded=False):
        st.code("""
gb = GridOptionsBuilder.from_dataframe(df)

# Configure default properties for all columns
gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=True,
    minWidth=100
)

gridOptions = gb.build()
AgGrid(df, gridOptions=gridOptions)
""", language="python")

    st.markdown("**Output:**")
    st.info("Try resizing, sorting, filtering, and editing cells in the grid below.")

    gb_default = GridOptionsBuilder.from_dataframe(df)
    gb_default.configure_default_column(
        resizable=True,
        filter=True,
        sortable=True,
        editable=True,
        minWidth=100
    )
    gridOptions_default = gb_default.build()
    AgGrid(df, gridOptions=gridOptions_default, height=250, key="default_col_example")


def section_column_configuration():
    """Column Configuration Section"""
    st.header("Column Configuration", anchor="column-configuration")

    st.markdown("""
    You can configure individual columns using `configure_column()`. This is useful for:
    - Setting custom header names
    - Formatting values
    - Making specific columns non-editable
    - Pinning columns
    - Setting column widths
    """)

    with st.expander("Show code", expanded=False):
        st.code("""
gb = GridOptionsBuilder.from_dataframe(df)

# Configure individual columns
gb.configure_column('Employee',
    header_name='Full Name',
    pinned='left',
    minWidth=150
)

gb.configure_column('Salary',
    header_name='Annual Salary',
    type=['numericColumn'],
    valueFormatter="'$' + value.toLocaleString()",
    editable=False
)

gb.configure_column('Start Date',
    type=['dateColumnFilter'],
    valueFormatter="new Date(value).toLocaleDateString()"
)

gridOptions = gb.build()
AgGrid(df, gridOptions=gridOptions)
""", language="python")

    st.markdown("**Output:**")
    st.info("Notice the 'Employee' column is pinned, 'Salary' is formatted with '$', and 'Start Date' shows as a readable date.")

    gb_column = GridOptionsBuilder.from_dataframe(df)
    gb_column.configure_column('Employee',
        header_name='Full Name',
        pinned='left',
        minWidth=150
    )
    gb_column.configure_column('Salary',
        header_name='Annual Salary',
        type=['numericColumn'],
        valueFormatter="'$' + value.toLocaleString()",
        editable=False
    )
    gb_column.configure_column('Start Date',
        type=['dateColumnFilter'],
        valueFormatter="new Date(value).toLocaleDateString()"
    )
    gridOptions_column = gb_column.build()
    AgGrid(df, gridOptions=gridOptions_column, height=250, key="column_example")


def section_selection():
    """Selection Section"""
    st.header("Selection", anchor="selection")

    st.markdown("""
    The `configure_selection()` method enables row selection with various modes:
    - **single**: Select one row at a time
    - **multiple**: Select multiple rows
    - **disabled**: No selection allowed

    You can also enable checkboxes for easier selection.
    """)

    with st.expander("Show code", expanded=False):
        st.code("""
gb = GridOptionsBuilder.from_dataframe(df)

# Configure row selection with checkboxes
gb.configure_selection(
    selection_mode='multiple',
    use_checkbox=True,
    header_checkbox=True,
    header_checkbox_filtered_only=True
)

gridOptions = gb.build()

# Get selected rows from the response
response = AgGrid(df, gridOptions=gridOptions)
selected_rows = response['selected_rows']

if len(selected_rows) > 0:
    st.write("Selected employees:", selected_rows)
""", language="python")

    st.markdown("**Output:**")
    st.info("Click checkboxes to select rows. The header checkbox selects all visible rows.")

    gb_selection = GridOptionsBuilder.from_dataframe(df)
    gb_selection.configure_default_column(minWidth=100)
    gb_selection.configure_selection(
        selection_mode='multiple',
        use_checkbox=True,
        header_checkbox=True,
        header_checkbox_filtered_only=True
    )
    gridOptions_selection = gb_selection.build()

    response_selection = AgGrid(df, gridOptions=gridOptions_selection, height=250, key="selection_example")

    if response_selection['selected_rows'] is not None and len(response_selection['selected_rows']) > 0:
        selected_df = pd.DataFrame(response_selection['selected_rows'])
        st.success(f"Selected {len(selected_df)} employee(s)")
        st.dataframe(selected_df[['Employee', 'Department', 'Salary']], use_container_width=True)


def section_pagination():
    """Pagination Section"""
    st.header("Pagination", anchor="pagination")

    st.markdown("""
    Pagination is useful for large datasets. You can enable it with `configure_pagination()`.
    AG Grid will automatically calculate the optimal page size based on grid height, or you can set a fixed page size.
    """)

    with st.expander("Show code", expanded=False):
        st.code("""
gb = GridOptionsBuilder.from_dataframe(df)

# Enable pagination with auto page size
gb.configure_pagination(
    enabled=True,
    paginationAutoPageSize=True
)

# Or set a fixed page size
# gb.configure_pagination(
#     enabled=True,
#     paginationAutoPageSize=False,
#     paginationPageSize=5
# )

gridOptions = gb.build()
AgGrid(df, gridOptions=gridOptions)
""", language="python")

    st.markdown("**Output:**")
    st.info("Use the pagination controls at the bottom to navigate between pages.")

    gb_pagination = GridOptionsBuilder.from_dataframe(df)
    gb_pagination.configure_default_column(minWidth=100)
    gb_pagination.configure_pagination(
        enabled=True,
        paginationAutoPageSize=False,
        paginationPageSize=5
    )
    gridOptions_pagination = gb_pagination.build()
    AgGrid(df, gridOptions=gridOptions_pagination, height=300, key="pagination_example")


def section_side_bar():
    """Side Bar Section"""
    st.header("Side Bar", anchor="side-bar")

    st.markdown("""
    The sidebar provides quick access to columns and filters panels. This is an **Enterprise feature**
    that requires an AG Grid license, but you can enable it with `enable_enterprise_modules=True` for testing.

    Use `configure_side_bar()` to enable the side panels.
    """)

    with st.expander("Show code", expanded=False):
        st.code("""
gb = GridOptionsBuilder.from_dataframe(df)

gb.configure_default_column(
    resizable=True,
    filter=True,
    sortable=True
)

# Configure sidebar with columns and filters panels
gb.configure_side_bar(
    filters_panel=True,
    columns_panel=True,
    defaultToolPanel=""  # Start closed
)

gridOptions = gb.build()

AgGrid(df,
       gridOptions=gridOptions,
       enable_enterprise_modules=True)
""", language="python")

    st.markdown("**Output:**")
    st.info("Click the sidebar icon (≡) in the top right to access columns and filters panels.")

    gb_sidebar = GridOptionsBuilder.from_dataframe(df)
    gb_sidebar.configure_default_column(
        resizable=True,
        filter=True,
        sortable=True,
        minWidth=100
    )
    gb_sidebar.configure_side_bar(
        filters_panel=True,
        columns_panel=True,
        defaultToolPanel=""
    )
    gridOptions_sidebar = gb_sidebar.build()
    AgGrid(df,
           gridOptions=gridOptions_sidebar,
           height=300,
           enable_enterprise_modules=True,
           key="sidebar_example")


def section_complete_example():
    """Complete Example Section"""
    st.header("Complete Example", anchor="complete-example")

    st.markdown("""
    Here's a complete example combining multiple configuration options to create a fully-featured grid:
    - Custom column configurations
    - Row selection with checkboxes
    - Pagination
    - Sidebar panels
    - Custom styling
    """)

    with st.expander("Show code", expanded=False):
        st.code("""
gb = GridOptionsBuilder.from_dataframe(df)

# Default column config
gb.configure_default_column(
    resizable=True,
    filter=True,
    sortable=True,
    editable=True,
    minWidth=100
)

# Individual column customization
gb.configure_column('Employee',
    header_name='Full Name',
    pinned='left',
    editable=False
)

gb.configure_column('Salary',
    header_name='Annual Salary',
    type=['numericColumn'],
    valueFormatter="'$' + value.toLocaleString()"
)

gb.configure_column('Age',
    type=['numericColumn'],
    maxWidth=80
)

# Selection with checkboxes
gb.configure_selection(
    selection_mode='multiple',
    use_checkbox=True,
    header_checkbox=True
)

# Pagination
gb.configure_pagination(
    enabled=True,
    paginationAutoPageSize=False,
    paginationPageSize=5
)

# Sidebar
gb.configure_side_bar(
    filters_panel=True,
    columns_panel=True
)

gridOptions = gb.build()

response = AgGrid(
    df,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    height=350
)

# Access selected rows
selected = response.selected_rows
if len(selected) > 0:
    st.write(f"Selected {len(selected)} rows")
""", language="python")

    st.markdown("**Output:**")
    st.info("""
    This grid combines all features:
    - Pinned 'Employee' column
    - Formatted salary with '$'
    - Row selection checkboxes
    - Pagination (5 rows per page)
    - Sidebar for columns/filters
    - Editable cells (except Employee)
    """)

    gb_complete = GridOptionsBuilder.from_dataframe(df)

    # Default column config
    gb_complete.configure_default_column(
        resizable=True,
        filter=True,
        sortable=True,
        editable=True,
        minWidth=100
    )

    # Individual column customization
    gb_complete.configure_column('Employee',
        header_name='Full Name',
        pinned='left',
        editable=False
    )

    gb_complete.configure_column('Salary',
        header_name='Annual Salary',
        type=['numericColumn'],
        valueFormatter="'$' + value.toLocaleString()"
    )

    gb_complete.configure_column('Age',
        type=['numericColumn'],
        maxWidth=80
    )

    # Selection with checkboxes
    gb_complete.configure_selection(
        selection_mode='multiple',
        use_checkbox=True,
        header_checkbox=True
    )

    # Pagination
    gb_complete.configure_pagination(
        enabled=True,
        paginationAutoPageSize=False,
        paginationPageSize=5
    )

    # Sidebar
    gb_complete.configure_side_bar(
        filters_panel=True,
        columns_panel=True
    )

    gridOptions_complete = gb_complete.build()

    response_complete = AgGrid(
        df,
        gridOptions=gridOptions_complete,
        enable_enterprise_modules=True,
        height=350,
        key="complete_example"
    )

    # Display selected rows
    if response_complete.selected_rows is not None and len(response_complete.selected_rows) > 0:
        selected_complete = pd.DataFrame(response_complete['selected_rows'])
        st.success(f"Selected {len(selected_complete)} employee(s)")

        # Calculate some stats
        avg_salary = selected_complete['Salary'].mean()
        st.metric("Average Salary of Selected", f"${avg_salary:,.0f}")


# ============================================================================
# RENDER SECTIONS BASED ON CONFIGURATION
# ============================================================================

if SECTIONS.get('overview', False):
    section_overview()

if SECTIONS.get('gridoptionsbuilder_basics', False):
    section_gridoptionsbuilder_basics()

if SECTIONS.get('default_column_configuration', False):
    section_default_column_configuration()

if SECTIONS.get('column_configuration', False):
    section_column_configuration()

if SECTIONS.get('selection', False):
    section_selection()

if SECTIONS.get('pagination', False):
    section_pagination()

if SECTIONS.get('side_bar', False):
    section_side_bar()

if SECTIONS.get('complete_example', False):
    section_complete_example()


# ============================================================================
# FOOTER
# ============================================================================

st.divider()

st.info("""
**Learn More:**

For more advanced configuration options and detailed documentation:

- [AG Grid Column Properties](https://www.ag-grid.com/javascript-data-grid/column-properties/)
- [AG Grid Grid Options](https://www.ag-grid.com/javascript-data-grid/grid-options/)
- [AG Grid Deep Dive](https://ag-grid.com/react-data-grid/deep-dive/)

Check out other sections in this app for more specific use cases and examples.
""")
