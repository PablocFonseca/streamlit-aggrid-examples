"""
Data Editing & Cell Updates
============================

This guide demonstrates how to configure editable grids and handle cell editing in AgGrid.
Learn about different edit types, validation, change detection, and data persistence.
Based on AG Grid Cell Editing documentation: https://ag-grid.com/javascript-data-grid/cell-editing/
"""

import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
from pathlib import Path
import pandas as pd
import numpy as np

st.set_page_config(page_title="Data Editing & Cell Updates", layout="wide")

# ============================================================================
# SECTION CONTROL - Set to True/False to enable/disable sections
# ============================================================================
SECTIONS = {
    'overview': True,
    'basic_editable_grid': False,
    'edit_types': False,
    'cell_editors': True,
    'change_detection': False,
    'server_sync_strategy': False,
    'validation': False,
}

# Sidebar navigation/index
with st.sidebar:
    st.markdown('''
    <div class="sidebar-nav-section">On this page</div>
    <div class="sidebar-nav-container">
        <a href="#overview" class="sidebar-nav-link">Overview</a>
        <a href="#basic-editable-grid" class="sidebar-nav-link">Basic Editable Grid</a>
        <a href="#edit-types" class="sidebar-nav-link">Edit Types</a>
        <a href="#cell-editors" class="sidebar-nav-link">Cell Editors</a>
        <a href="#change-detection" class="sidebar-nav-link">Change Detection</a>
        <a href="#server-sync-strategy" class="sidebar-nav-link">Server Sync Strategy</a>
        <a href="#validation" class="sidebar-nav-link">Data Validation</a>
    </div>
    ''', unsafe_allow_html=True)

st.title("Data Editing & Cell Updates")

st.markdown("""
This guide demonstrates how to make your AgGrid editable and handle user modifications.
You'll learn about different editor types, validation, and how to track changes.
""")

# Create sample data
@st.cache_data
def get_employee_data():
    np.random.seed(42)
    return pd.DataFrame({
        'Employee': [
            'Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Prince',
            'Edward Norton', 'Fiona Apple', 'George Martin', 'Helen Troy'
        ],
        'Department': [
            'Engineering', 'Sales', 'Engineering', 'Marketing',
            'Sales', 'Engineering', 'Marketing', 'Sales'
        ],
        'Position': [
            'Senior Dev', 'Account Manager', 'Tech Lead', 'Marketing Manager',
            'Sales Director', 'Developer', 'Content Creator', 'Sales Rep'
        ],
        'Age': [28, 35, 42, 31, 45, 29, 38, 33],
        'Salary': [75000, 65000, 95000, 70000, 80000, 78000, 72000, 68000],
        'Start Date': pd.date_range('2020-01-01', periods=8, freq='3M').strftime('%Y-%m-%d').tolist(),
        'Performance': [
            'Excellent', 'Good', 'Excellent', 'Average',
            'Good', 'Excellent', 'Good', 'Average'
        ],
        'Active': [True, True, True, False, True, True, False, True],
        'Notes': [
            '• Great team player\n• Always willing to help others\n• Strong technical skills',
            '• Exceeded Q3 targets\n• Building strong client relationships\n• Reliable performer',
            '• Led migration project\n• Mentor to junior developers\n• Excellent problem solver',
            '• Improved social media engagement\n• Creative content ideas\n• Currently on sabbatical',
            '• Closed major deals\n• Strong negotiation skills\n• Builds lasting partnerships',
            '• Fast learner\n• Eager to take on challenges\n• Good communication skills',
            '• Creative campaigns\n• Innovative marketing strategies\n• Currently on leave',
            '• Building client relationships\n• Good follow-up skills\n• Consistent results'
        ],
    })

# Load Olympic data for some examples
data_path = Path(__file__).parent.parent.parent.joinpath(
    "assets", "olympic-winners.json"
)

@st.cache_data
def load_olympic_data():
    """Load Olympic winners data for demonstrations."""
    return pd.read_json(data_path)

df_employees = get_employee_data()
df_olympic = load_olympic_data()


# ============================================================================
# SECTION FUNCTIONS
# ============================================================================

def section_overview():
    """Overview Section"""
    st.header("Overview", anchor="overview")

    st.markdown("""
    AG Grid provides powerful cell editing capabilities that allow users to modify data directly in the grid.
    Key features include:
    - **Multiple editor types**: Text, number, dropdown, checkbox, date pickers, and custom editors
    - **Validation**: Client-side validation to ensure data integrity
    - **Change tracking**: Monitor which cells have been modified
    - **Server sync strategies**: Control how edits interact with server data updates
    - **Events**: Respond to edit events for real-time processing
    """)


def section_basic_editable_grid():
    """Basic Editable Grid Section"""
    st.header("Basic Editable Grid", anchor="basic-editable-grid")

    st.markdown("""
    The simplest way to make a grid editable is to pass `editable=True` to the `AgGrid` function.
    This makes all columns editable with a text editor.

    Alternatively, you can use `GridOptionsBuilder` to configure which columns are editable.
    """)

    with st.expander("Show code", expanded=False):
        st.code("""
from st_aggrid import AgGrid, GridOptionsBuilder

# Method 1: Simple approach - all columns editable
response = AgGrid(df, editable=True)

# Method 2: Using GridOptionsBuilder for more control
gb = GridOptionsBuilder.from_dataframe(df)

# Make all columns editable by default
gb.configure_default_column(editable=True)

# Or make specific columns non-editable
gb.configure_column('Employee', editable=False)

gridOptions = gb.build()
response = AgGrid(df, gridOptions=gridOptions)

# Access modified data
modified_df = response['data']
""", language="python")

    st.markdown("**Output:**")
    st.info("Click any cell to edit it. Press Enter or Tab to confirm changes, Escape to cancel.")

    gb_basic = GridOptionsBuilder.from_dataframe(df_employees)
    gb_basic.configure_default_column(editable=True, minWidth=100)
    gb_basic.configure_column('Employee', editable=False, pinned='left', minWidth=150)
    gb_basic.configure_column('Salary', type=['numericColumn'], valueFormatter="'$' + value.toLocaleString()")
    gb_basic.configure_column('::auto_unique_id::', hide=True)

    gridOptions_basic = gb_basic.build()
    response_basic = AgGrid(df_employees, gridOptions=gridOptions_basic, height=300, key="basic_editable")

    if response_basic['data'] is not None:
        with st.expander("View Modified Data", expanded=False):
            st.dataframe(response_basic['data'], use_container_width=True)


def section_edit_types():
    """Edit Types Section"""
    st.header("Edit Types", anchor="edit-types")

    st.markdown("""
    AG Grid supports different cell editor types for various data formats:
    - **Text**: Default editor for strings
    - **Number**: Numeric input with validation
    - **Select/Dropdown**: Choose from predefined options
    - **Checkbox**: Boolean toggle
    - **Date**: Date picker (requires custom editor or enterprise)
    - **Custom**: JavaScript-based custom editors
    """)

    with st.expander("Show code", expanded=False):
        st.code("""
gb = GridOptionsBuilder.from_dataframe(df)

# Text editor (default)
gb.configure_column('Employee', editable=True)

# Number editor - AG Grid will auto-detect numeric columns
gb.configure_column('Age',
    editable=True,
    type=['numericColumn']
)

# Dropdown/Select editor using cellEditor
gb.configure_column('Department',
    editable=True,
    cellEditor='agSelectCellEditor',
    cellEditorParams={
        'values': ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance']
    }
)

# Checkbox editor using cellEditor
gb.configure_column('Active',
    editable=True,
    cellEditor='agCheckboxCellEditor'
)

gridOptions = gb.build()
AgGrid(df, gridOptions=gridOptions)
""", language="python")

    st.markdown("**Output:**")
    st.info("""
    Try editing different columns:
    - **Department**: Click to see dropdown options
    - **Age**: Numeric input only
    - **Active**: Checkbox toggle
    - **Position**: Text input
    """)

    gb_types = GridOptionsBuilder.from_dataframe(df_employees)
    gb_types.configure_default_column(editable=True, minWidth=100)
    gb_types.configure_column('Employee', editable=False, pinned='left', minWidth=150)
    gb_types.configure_column('Department',
        cellEditor='agSelectCellEditor',
        cellEditorParams={
            'values': ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance']
        }
    )
    gb_types.configure_column('Age', type=['numericColumn'])
    gb_types.configure_column('Salary',
        type=['numericColumn'],
        valueFormatter="'$' + value.toLocaleString()"
    )
    gb_types.configure_column('Active',
        cellEditor='agCheckboxCellEditor'
    )
    gb_types.configure_column('::auto_unique_id::', hide=True)

    gridOptions_types = gb_types.build()
    response_types = AgGrid(df_employees, gridOptions=gridOptions_types, height=300, key="edit_types")


def section_cell_editors():
    """Cell Editors Section"""
    st.header("Cell Editors", anchor="cell-editors")

    st.markdown("""
    AG Grid provides several built-in cell editors:

    | Editor | Description | Use Case |
    |--------|-------------|----------|
    | `agTextCellEditor`[↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#text-cell-editor) | Text input (default) | Names, descriptions |
    | `agNumberCellEditor`[↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#number-cell-editor) | Numeric input | Ages, quantities |
    | `agSelectCellEditor`[↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#select-cell-editor) | Dropdown selection | Categories, statuses |
    | `agCheckboxCellEditor`[↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#checkbox-cell-editor) | Checkbox toggle | Boolean values |
    | `agLargeTextCellEditor`[↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#large-text-cell-editor) | Multi-line text area | Comments, notes |
    | `agDateCellEditor`[↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#date-cell-editor) | Date picker (Enterprise) | Dates |
    | `agDateStringCellEditor`[↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#date-cell-editor-as-string) | Date as string (Enterprise) | Date strings |
    | `agRichSelectCellEditor`[↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#rich-select-cell-editor) | Rich select with search (Enterprise) | Large option lists |

    You can also create custom editors using JavaScript code with the `JsCode` helper.
    """)

    with st.expander("Show code", expanded=False):
        st.code("""
from st_aggrid import JsCode

gb = GridOptionsBuilder.from_dataframe(df)

# Select editor with custom parameters
gb.configure_column('Performance',
    cellEditor='agSelectCellEditor',
    cellEditorParams={
        'values': ['Excellent', 'Good', 'Average', 'Poor']
    }
)

# Large text editor for comments
gb.configure_column('Comments',
    cellEditor='agLargeTextCellEditor',
    cellEditorParams={
        'maxLength': 500,
        'rows': 5,
        'cols': 50
    }
)

# Custom editor using JsCode (advanced)
custom_editor = JsCode(\"\"\"
class CustomEditor {
    init(params) {
        this.eInput = document.createElement('input');
        this.eInput.value = params.value;
        this.eInput.classList.add('ag-input');
        this.eInput.style.height = '100%';
    }

    getGui() {
        return this.eInput;
    }

    getValue() {
        return this.eInput.value.toUpperCase();
    }
}
\"\"\")

gb.configure_column('Position',
    cellEditor=custom_editor
)

gridOptions = gb.build()
AgGrid(df, gridOptions=gridOptions)
""", language="python")

    st.markdown("**Output:**")
    st.info("""
    This example demonstrates all commonly-used editor types:
    - **Employee**: Non-editable, pinned column (for reference)
    - **Department & Performance**: Select/dropdown editors
    - **Position**: Text editor (default)
    - **Age**: Number editor (numeric input only)
    - **Salary**: Number editor with formatting
    - **Start Date**: Text editor for dates
    - **Active**: Checkbox editor (boolean toggle)
    - **Notes**: Large text editor (multi-line text area) - Click to see the popup!
    """)

    # Salary validation style
    salary_editor_style = JsCode("""
function(params) {
    if (params.value < 0) {
        return {'backgroundColor': '#ffcccc', 'color': '#d32f2f'};
    }
    if (params.value > 100000) {
        return {'backgroundColor': '#c8e6c9', 'color': '#388e3c'};
    }
    return null;
}
""")

    gb_editors = GridOptionsBuilder.from_dataframe(df_employees)
    gb_editors.configure_default_column(editable=True, resizable=True, minWidth=100)
    gb_editors.configure_column('Employee', editable=False, pinned='left', minWidth=150)

    # Select editors
    gb_editors.configure_column('Department',
        cellEditor='agSelectCellEditor',
        cellEditorParams={
            'values': ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance']
        }
    )
    gb_editors.configure_column('Performance',
        cellEditor='agSelectCellEditor',
        cellEditorParams={
            'values': ['Excellent', 'Good', 'Average', 'Poor']
        }
    )

    # Text editor (default)
    gb_editors.configure_column('Position', minWidth=120)

    # Number editors
    gb_editors.configure_column('Age',
        type=['numericColumn'],
        maxWidth=80
    )
    gb_editors.configure_column('Salary',
        type=['numericColumn'],
        valueFormatter="'$' + value.toLocaleString()",
        cellStyle=salary_editor_style,
        minWidth=120
    )

    # Date column (text editor)
    gb_editors.configure_column('Start Date', minWidth=120)

    # Checkbox editor
    gb_editors.configure_column('Active',
        cellEditor='agCheckboxCellEditor',
        maxWidth=80
    )

    # Large text editor with popup
    gb_editors.configure_column('Notes',
        cellEditor='agLargeTextCellEditor',
        cellEditorPopup=True,  # Open as popup overlay instead of inline
        cellEditorParams={
            'maxLength': 200,
            'rows': 10,  # Popup height in rows
            'cols': 50   # Popup width in columns
        },
        minWidth=200
    )

    gb_editors.configure_column('Home Office Days',
        cellEditor='agRichSelectCellEditor',
        cellEditorPopup=True,  # Open as popup overlay instead of inline
        cellEditorParams={
            "values": ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            "multiSelect": True,
            "searchType": 'matchAny',
            "filterList": True,
            "highlightMatch": True,
            "valueListMaxHeight": 220,
        },
        minWidth=200
    )

    gb_editors.configure_column('::auto_unique_id::', hide=True)

    gridOptions_editors = gb_editors.build()
    response_editors = AgGrid(df_employees, gridOptions=gridOptions_editors, height=350, key="cell_editors", allow_unsafe_jscode=True, enable_enterprise_modules=True)

def section_change_detection():
    """Change Detection Section"""
    st.header("Change Detection", anchor="change-detection")

    st.markdown("""
    Track which cells have been edited by comparing the returned data with the original DataFrame.
    This is useful for:
    - Highlighting modified rows
    - Sending only changed data to the server
    - Implementing undo/redo functionality
    - Showing a summary of changes
    """)

    with st.expander("Show code", expanded=False):
        st.code("""
# Store original data
original_df = df.copy()

# Render grid
response = AgGrid(df, editable=True)
modified_df = response['data']

# Compare to find changes
if modified_df is not None:
    # Find rows that have changed
    changed_rows = []
    for idx in range(len(original_df)):
        if not original_df.iloc[idx].equals(modified_df.iloc[idx]):
            changed_rows.append(idx)

    if changed_rows:
        st.success(f"Modified {len(changed_rows)} row(s)")
        st.write("Changed rows:", modified_df.iloc[changed_rows])
""", language="python")

    st.markdown("**Output:**")
    st.info("Edit any cells below and see the change detection in action.")

    # Initialize session state for change tracking
    if 'original_data' not in st.session_state:
        st.session_state.original_data = df_employees.copy()

    gb_changes = GridOptionsBuilder.from_dataframe(df_employees)
    gb_changes.configure_default_column(editable=True, minWidth=100)
    gb_changes.configure_column('Employee', editable=False, pinned='left', minWidth=150)
    gb_changes.configure_column('Department',
        cellEditor='agSelectCellEditor',
        cellEditorParams={
            'values': ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance']
        }
    )
    gb_changes.configure_column('Salary',
        type=['numericColumn'],
        valueFormatter="'$' + value.toLocaleString()"
    )
    gb_changes.configure_column('::auto_unique_id::', hide=True)

    gridOptions_changes = gb_changes.build()
    response_changes = AgGrid(df_employees, gridOptions=gridOptions_changes, height=300, key="change_detection")

    # Detect changes
    if response_changes['data'] is not None:
        modified_df = pd.DataFrame(response_changes['data'])
        original_df = st.session_state.original_data

        # Find changed rows
        changed_indices = []
        for idx in range(len(original_df)):
            if idx < len(modified_df):
                orig_row = original_df.iloc[idx].to_dict()
                mod_row = modified_df.iloc[idx].to_dict()
                if orig_row != mod_row:
                    changed_indices.append(idx)

        if changed_indices:
            st.success(f"✏️ Detected {len(changed_indices)} modified row(s)")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original Data (Changed Rows):**")
                st.dataframe(original_df.iloc[changed_indices], use_container_width=True)
            with col2:
                st.markdown("**Modified Data (Changed Rows):**")
                st.dataframe(modified_df.iloc[changed_indices], use_container_width=True)


def section_server_sync_strategy():
    """Server Sync Strategy Section"""
    st.header("Server Sync Strategy", anchor="server-sync-strategy")

    st.markdown("""
    The `reload_data` parameter controls how the grid handles updates to the underlying data:

    - **`reload_data=False` (default - "client wins")**: Once the grid has been edited ("dirty"), it ignores
      updates to the underlying DataFrame. Modified data persists in the grid.

    - **`reload_data=True` ("server wins")**: The grid always updates when the underlying DataFrame changes,
      even if cells have been edited. This overwrites any local edits.

    This behavior is important when your data source updates while users are editing.
    """)

    with st.expander("Show code - Client Wins Strategy", expanded=False):
        st.code("""
import streamlit as st
from st_aggrid import AgGrid

# Client wins strategy (default)
st.button("Refresh Data", key="refresh_client")
data = df.sample(5)  # Simulate data refresh

response = AgGrid(
    data,
    editable=True,
    reload_data=False,  # Grid ignores updates once edited
    key="client_wins_grid"
)

st.info(\"\"\"
Once you edit any cell, the grid becomes "dirty" and stops
updating even when you click the refresh button.
\"\"\")
""", language="python")

    with st.expander("Show code - Server Wins Strategy", expanded=False):
        st.code("""
# Server wins strategy
st.button("Refresh Data", key="refresh_server")
data = df.sample(5)  # Simulate data refresh

response = AgGrid(
    data,
    editable=True,
    reload_data=True,  # Grid always updates with new data
    key="server_wins_grid"
)

st.info(\"\"\"
The grid always updates when you click refresh,
even if you've edited cells. Your edits will be lost.
\"\"\")
""", language="python")

    st.markdown("**Demo - Client Wins (Default):**")
    st.info("""
    Edit a cell, then click 'Refresh Data'. The grid will keep your edits and ignore the refresh.
    To reset, change the key or reload the page.
    """)

    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("Refresh Data", key="refresh_client_wins")
    with col2:
        pass

    # Sample data for demo
    data_client = df_olympic.sample(10, random_state=42) if 'refresh_client_wins' not in st.session_state else df_olympic.sample(10)

    gb_client = GridOptionsBuilder.from_dataframe(data_client[['athlete', 'age', 'country', 'sport', 'gold', 'silver', 'bronze']])
    gb_client.configure_default_column(editable=True, minWidth=100)
    gb_client.configure_column('athlete', editable=False, minWidth=150)
    gridOptions_client = gb_client.build()

    response_client = AgGrid(
        data_client[['athlete', 'age', 'country', 'sport', 'gold', 'silver', 'bronze']],
        gridOptions=gridOptions_client,
        reload_data=False,
        height=250,
        key="client_wins_grid"
    )

    st.markdown("**Demo - Server Wins:**")
    st.info("""
    Edit a cell, then click 'Refresh Data'. The grid will update with new data, discarding your edits.
    """)

    col1, col2 = st.columns([1, 4])
    with col1:
        refresh_server = st.button("Refresh Data", key="refresh_server_wins")
    with col2:
        pass

    # Sample data for demo
    if refresh_server:
        data_server = df_olympic.sample(10)
    else:
        data_server = df_olympic.sample(10, random_state=99)

    gb_server = GridOptionsBuilder.from_dataframe(data_server[['athlete', 'age', 'country', 'sport', 'gold', 'silver', 'bronze']])
    gb_server.configure_default_column(editable=True, minWidth=100)
    gb_server.configure_column('athlete', editable=False, minWidth=150)
    gridOptions_server = gb_server.build()

    response_server = AgGrid(
        data_server[['athlete', 'age', 'country', 'sport', 'gold', 'silver', 'bronze']],
        gridOptions=gridOptions_server,
        reload_data=True,
        height=250,
        key="server_wins_grid"
    )


def section_validation():
    """Validation Section"""
    st.header("Data Validation", anchor="validation")

    st.markdown("""
    Implement client-side validation to ensure data integrity using cell style callbacks and value setters.
    You can:
    - Validate input format (e.g., email addresses, phone numbers)
    - Check value ranges (e.g., age > 0, salary within limits)
    - Enforce business rules
    - Provide visual feedback with custom cell styles
    """)

    with st.expander("Show code", expanded=False):
        st.code("""
from st_aggrid import JsCode

gb = GridOptionsBuilder.from_dataframe(df)

# Cell style function to highlight invalid cells
cell_style_jscode = JsCode(\"\"\"
function(params) {
    if (params.value < 0) {
        return {'backgroundColor': '#ffcccc', 'color': 'red'};
    }
    if (params.value > 100000) {
        return {'backgroundColor': '#fff4cc', 'color': 'orange'};
    }
    return null;
}
\"\"\")

gb.configure_column('Salary',
    editable=True,
    type=['numericColumn'],
    cellStyle=cell_style_jscode
)

# Value parser to validate and transform input
value_parser = JsCode(\"\"\"
function(params) {
    const newValue = parseInt(params.newValue);
    if (isNaN(newValue) || newValue < 0) {
        alert('Salary must be a positive number');
        return params.oldValue;  // Reject change
    }
    if (newValue > 200000) {
        alert('Salary cannot exceed $200,000');
        return params.oldValue;  // Reject change
    }
    return newValue;  // Accept change
}
\"\"\")

gb.configure_column('Salary',
    editable=True,
    valueParser=value_parser
)

gridOptions = gb.build()
AgGrid(df, gridOptions=gridOptions)
""", language="python")

    st.markdown("**Output:**")
    st.info("""
    Validation rules for Salary:
    - Values < 0: Highlighted in red
    - Values > $100,000: Highlighted in yellow/orange
    - Try entering negative values or values > $200,000 to see validation
    """)

    # Cell style for validation
    cell_style_validation = JsCode("""
function(params) {
    if (params.value < 0) {
        return {'backgroundColor': '#ffcccc', 'color': '#d32f2f', 'fontWeight': 'bold'};
    }
    if (params.value > 100000) {
        return {'backgroundColor': '#fff4cc', 'color': '#f57c00'};
    }
    return null;
}
""")

    # Value parser for salary validation
    salary_parser = JsCode("""
function(params) {
    const newValue = parseInt(params.newValue);
    if (isNaN(newValue) || newValue < 0) {
        return params.oldValue;
    }
    if (newValue > 200000) {
        return params.oldValue;
    }
    return newValue;
}
""")

    gb_validation = GridOptionsBuilder.from_dataframe(df_employees)
    gb_validation.configure_default_column(editable=True, minWidth=100)
    gb_validation.configure_column('Employee', editable=False, pinned='left', minWidth=150)
    gb_validation.configure_column('Salary',
        type=['numericColumn'],
        valueFormatter="'$' + value.toLocaleString()",
        cellStyle=cell_style_validation,
        valueParser=salary_parser
    )
    gb_validation.configure_column('Age',
        type=['numericColumn']
    )
    gb_validation.configure_column('::auto_unique_id::', hide=True)

    gridOptions_validation = gb_validation.build()
    response_validation = AgGrid(df_employees, gridOptions=gridOptions_validation, height=300, key="validation_example")


# ============================================================================
# RENDER SECTIONS BASED ON CONFIGURATION
# ============================================================================

if SECTIONS.get('overview', False):
    section_overview()

if SECTIONS.get('basic_editable_grid', False):
    section_basic_editable_grid()

if SECTIONS.get('edit_types', False):
    section_edit_types()

if SECTIONS.get('cell_editors', False):
    section_cell_editors()

if SECTIONS.get('change_detection', False):
    section_change_detection()

if SECTIONS.get('server_sync_strategy', False):
    section_server_sync_strategy()

if SECTIONS.get('validation', False):
    section_validation()


# ============================================================================
# FOOTER
# ============================================================================

st.divider()

st.info("""
**Learn More:**

For more information on cell editing and advanced features:

- [AG Grid Cell Editing](https://www.ag-grid.com/javascript-data-grid/cell-editing/)
- [AG Grid Provided Cell Editors](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/)
- [AG Grid Cell Editor Components](https://www.ag-grid.com/javascript-data-grid/component-cell-editor/)
- [AG Grid Value Setters](https://www.ag-grid.com/javascript-data-grid/value-setters/)
- [AG Grid Cell Data Types](https://www.ag-grid.com/javascript-data-grid/cell-data-types/)

Check out other documentation pages for more examples and use cases.
""")
