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

from streamlit_aggrid import AgGridReturn

st.set_page_config(page_title="Data Editing & Cell Updates", layout="wide")

# ============================================================================
# SECTION CONTROL - Set to True/False to enable/disable sections
# ============================================================================
SECTIONS = {
    'overview': True,
    'basic_editable_grid': True,
    'cell_editors': True,
    'server_sync_strategy': True,
}

# Sidebar navigation/index
with st.sidebar:
    st.markdown('''
    <div class="sidebar-nav-section">On this page</div>
    <div class="sidebar-nav-container">
        <a href="#overview" class="sidebar-nav-link">Overview</a>
        <a href="#basic-editable-grid" class="sidebar-nav-link">Basic Editable Grid</a>
        <a href="#cell-editors" class="sidebar-nav-link">Cell Editors</a>
        <a href="#server-sync-strategy" class="sidebar-nav-link">Server Sync Strategy</a>
    </div>
    ''', unsafe_allow_html=True)

st.title("Data Editing & Cell Updates")

st.markdown("""
AG Grid provides powerful cell editing capabilities that allow users to modify data directly within the grid.
This guide covers the fundamentals of making grids editable, configuring different cell editor types,
understanding server synchronization strategies, and implementing validation rules.
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
    Cell editing is a fundamental feature that transforms static data grids into interactive data management tools.
    Understanding the editing capabilities available in AG Grid enables you to build sophisticated data entry
    and modification interfaces.

    **Key Capabilities**

    AG Grid's editing system provides:

    - **Multiple editor types** — Text, number, dropdown, checkbox, date pickers, and custom editors
    - **Validation** — Client-side validation to ensure data integrity before commits
    - **Change tracking** — Monitor which cells have been modified during the session
    - **Server sync strategies** — Control how local edits interact with server data updates
    - **Event handling** — Respond to edit events for real-time processing and side effects

    The following sections demonstrate these capabilities with practical examples.
    """)


def section_basic_editable_grid():
    """Basic Editable Grid Section"""
    st.header("Basic Editable Grid", anchor="basic-editable-grid")

    st.markdown("""
    Making a grid editable requires minimal configuration. The simplest approach is to pass
    ``editable=True`` to the ``AgGrid`` function, which enables text editing for all columns.

    For more granular control over which columns are editable, use the ``GridOptionsBuilder``
    to configure individual column properties. This approach allows you to lock specific columns
    while enabling editing for others.
    """)

    st.markdown("**Example**")

    st.info("""
    **Interaction:** Click any cell to edit it. Press Enter or Tab to confirm changes, Escape to cancel.
    The Employee column is locked to demonstrate selective editability.
    """)

    gb_basic = GridOptionsBuilder.from_dataframe(df_employees)
    gb_basic.configure_default_column(editable=True, minWidth=100)
    gb_basic.configure_column('Employee', editable=False, pinned='left', minWidth=150)
    gb_basic.configure_column('Salary', type=['numericColumn'], valueFormatter="'$' + value.toLocaleString()")
    gb_basic.configure_column('::auto_unique_id::', hide=True)

    gridOptions_basic = gb_basic.build()
    response_basic = AgGrid(pd.concat([df_employees]*1), gridOptions=gridOptions_basic, height=300, nkey="basic_editable", data_return_mode='FILTERED')

    if response_basic:
        with st.expander("View Modified Data", expanded=False):
            st.write(response_basic.data)

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

    st.divider()

def section_cell_editors():
    """Cell Editors Section"""
    st.header("Cell Editors", anchor="cell-editors")

    st.markdown("""
    AG Grid provides a comprehensive set of built-in cell editors tailored to different data types.
    Beyond these provided editors, you can create custom editors using JavaScript code to meet
    specialized requirements.
    """)

    # Custom Emoji Picker Editor
    customEmojiPicker = JsCode("""
    class EmojiPicker {
        constructor() {
            this.defaultImgStyle = 'padding-left:10px; padding-right:10px; border: 1px solid transparent; padding: 4px; cursor: pointer;';
            this.selectedImgStyle = 'padding-left:10px; padding-right:10px; border: 1px solid lightgreen; padding: 4px; cursor: pointer;';
        }

        onKeyDown(event) {
            const key = event.key;
            if (key === 'ArrowLeft' || key === 'ArrowRight') {
                this.toggleEmoji();
                event.stopPropagation();
            }
        }

        toggleEmoji() {
            this.selectEmoji(this.emoji === '😊' ? '😢' : '😊');
        }

        init(params) {
            this.container = document.createElement('div');
            this.container.style.cssText = 'border-radius: 15px; border: 1px solid grey; background-color: #e6e6e6; padding: 15px; text-align:center; display:inline-block; outline:none';
            this.container.tabIndex = 0;

            this.happyEmoji = document.createElement('span');
            this.happyEmoji.innerHTML = '😊';
            this.happyEmoji.style.cssText = this.defaultImgStyle + 'font-size: 24px;';

            this.sadEmoji = document.createElement('span');
            this.sadEmoji.innerHTML = '😢';
            this.sadEmoji.style.cssText = this.defaultImgStyle + 'font-size: 24px;';

            this.container.appendChild(this.happyEmoji);
            this.container.appendChild(this.sadEmoji);

            this.happyEmoji.addEventListener('click', () => {
                this.selectEmoji('😊');
                params.stopEditing();
            });

            this.sadEmoji.addEventListener('click', () => {
                this.selectEmoji('😢');
                params.stopEditing();
            });

            this.container.addEventListener('keydown', (event) => {
                this.onKeyDown(event);
            });

            this.selectEmoji(params.value || '😊');
        }

        selectEmoji(emoji) {
            this.emoji = emoji;
            this.happyEmoji.style.cssText = (emoji === '😊' ? this.selectedImgStyle : this.defaultImgStyle) + 'font-size: 24px;';
            this.sadEmoji.style.cssText = (emoji === '😢' ? this.selectedImgStyle : this.defaultImgStyle) + 'font-size: 24px;';
        }

        getGui() {
            return this.container;
        }

        afterGuiAttached() {
            this.container.focus();
        }

        getValue() {
            return this.emoji;
        }

        destroy() {}

        isPopup() {
            return true;
        }
    }
    """)

    st.markdown("### Built-in Cell Editors")

    st.markdown("""
    The following table summarizes the provided cell editors:

    | Editor | Description | Use Case |
    |--------|-------------|----------|
    | ``agTextCellEditor`` [↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#text-cell-editor) | Text input (default) | Names, descriptions |
    | ``agNumberCellEditor`` [↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#number-cell-editor) | Numeric input | Ages, quantities |
    | ``agSelectCellEditor`` [↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#select-cell-editor) | Dropdown selection | Categories, statuses |
    | ``agCheckboxCellEditor`` [↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#checkbox-cell-editor) | Checkbox toggle | Boolean values |
    | ``agLargeTextCellEditor`` [↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#large-text-cell-editor) | Multi-line text area | Comments, notes |
    | ``agDateCellEditor`` [↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#date-cell-editor) | Date picker (Enterprise) | Dates |
    | ``agDateStringCellEditor`` [↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#date-cell-editor-as-string) | Date as string (Enterprise) | Date strings |
    | ``agRichSelectCellEditor`` [↗](https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/#rich-select-cell-editor) | Rich select with search (Enterprise) | Large option lists |

    ### Custom Editors

    For specialized editing requirements, you can create custom editors using the ``JsCode`` helper.
    Custom editors provide complete control over the editing experience, including custom UI elements,
    validation logic, and interaction patterns.
    """)

    with st.expander("Show code", expanded=False):
        st.code("""
from st_aggrid import JsCode

# Custom Emoji Picker Editor using JsCode
customEmojiPicker = JsCode(\"\"\"
class EmojiPicker {
    constructor() {
        this.defaultImgStyle = 'padding-left:10px; padding-right:10px; border: 1px solid transparent; padding: 4px; cursor: pointer;';
        this.selectedImgStyle = 'padding-left:10px; padding-right:10px; border: 1px solid lightgreen; padding: 4px; cursor: pointer;';
    }

    onKeyDown(event) {
        const key = event.key;
        if (key === 'ArrowLeft' || key === 'ArrowRight') {
            this.toggleEmoji();
            event.stopPropagation();
        }
    }

    toggleEmoji() {
        this.selectEmoji(this.emoji === '😊' ? '😢' : '😊');
    }

    init(params) {
        this.container = document.createElement('div');
        this.container.style.cssText = 'border-radius: 15px; border: 1px solid grey; background-color: #e6e6e6; padding: 15px; text-align:center; display:inline-block; outline:none';
        this.container.tabIndex = 0;

        this.happyEmoji = document.createElement('span');
        this.happyEmoji.innerHTML = '😊';
        this.happyEmoji.style.cssText = this.defaultImgStyle + 'font-size: 24px;';

        this.sadEmoji = document.createElement('span');
        this.sadEmoji.innerHTML = '😢';
        this.sadEmoji.style.cssText = this.defaultImgStyle + 'font-size: 24px;';

        this.container.appendChild(this.happyEmoji);
        this.container.appendChild(this.sadEmoji);

        this.happyEmoji.addEventListener('click', () => {
            this.selectEmoji('😊');
            params.stopEditing();
        });

        this.sadEmoji.addEventListener('click', () => {
            this.selectEmoji('😢');
            params.stopEditing();
        });

        this.container.addEventListener('keydown', (event) => {
            this.onKeyDown(event);
        });

        this.selectEmoji(params.value || '😊');
    }

    selectEmoji(emoji) {
        this.emoji = emoji;
        this.happyEmoji.style.cssText = (emoji === '😊' ? this.selectedImgStyle : this.defaultImgStyle) + 'font-size: 24px;';
        this.sadEmoji.style.cssText = (emoji === '😢' ? this.selectedImgStyle : this.defaultImgStyle) + 'font-size: 24px;';
    }

    getGui() {
        return this.container;
    }

    afterGuiAttached() {
        this.container.focus();
    }

    getValue() {
        return this.emoji;
    }

    destroy() {}

    isPopup() {
        return true;
    }
}
\"\"\")

gb = GridOptionsBuilder.from_dataframe(df)

# Select editor with custom parameters
gb.configure_column('Performance',
    cellEditor='agSelectCellEditor',
    cellEditorParams={
        'values': ['Excellent', 'Good', 'Average', 'Poor']
    }
)

# Custom emoji picker as a virtual column
gb.configure_column('Favorite Emoji',
    editable=True,
    cellEditor=customEmojiPicker,
    cellEditorPopup=True,  # Display as popup overlay
    minWidth=120
)

# Large text editor for notes
gb.configure_column('Notes',
    cellEditor='agLargeTextCellEditor',
    cellEditorPopup=True,
    cellEditorParams={
        'maxLength': 200,
        'rows': 10,
        'cols': 50
    }
)

gridOptions = gb.build()
AgGrid(df, gridOptions=gridOptions, allow_unsafe_jscode=True)
""", language="python")

    st.markdown("### Interactive Example")

    st.info("""
    **Column Editor Types:**

    - **Employee** — Non-editable, pinned column (for reference)
    - **Department & Performance** — Select/dropdown editors with predefined options
    - **Position** — Text editor (default)
    - **Age** — Number editor (numeric input only)
    - **Salary** — Number editor with currency formatting
    - **Favorite Emoji** — Custom emoji picker (JsCode) - Click to see the popup! Use arrow keys to toggle
    - **Start Date** — Text editor for dates
    - **Active** — Checkbox editor (boolean toggle)
    - **Notes** — Large text editor (multi-line text area) - Click to open the popup editor
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
        minWidth=120
    )

    # Custom emoji picker column (virtual column)
    gb_editors.configure_column('Favorite Emoji',
        editable=True,
        cellEditor=customEmojiPicker,
        cellEditorPopup=True,
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

    gb_editors.configure_column('::auto_unique_id::', hide=True)

    gridOptions_editors = gb_editors.build()
    response_editors = AgGrid(df_employees, gridOptions=gridOptions_editors, height=350, key="cell_editors", allow_unsafe_jscode=True)

    with st.expander('View Modified Data'):
        st.write(response_editors.data)

    with st.expander("Show code", expanded=False):
        st.code("""
from st_aggrid import JsCode

# Custom Emoji Picker Editor using JsCode
customEmojiPicker = JsCode(\"\"\"
class EmojiPicker {
    constructor() {
        this.defaultImgStyle = 'padding-left:10px; padding-right:10px; border: 1px solid transparent; padding: 4px; cursor: pointer;';
        this.selectedImgStyle = 'padding-left:10px; padding-right:10px; border: 1px solid lightgreen; padding: 4px; cursor: pointer;';
    }

    onKeyDown(event) {
        const key = event.key;
        if (key === 'ArrowLeft' || key === 'ArrowRight') {
            this.toggleEmoji();
            event.stopPropagation();
        }
    }

    toggleEmoji() {
        this.selectEmoji(this.emoji === '😊' ? '😢' : '😊');
    }

    init(params) {
        this.container = document.createElement('div');
        this.container.style.cssText = 'border-radius: 15px; border: 1px solid grey; background-color: #e6e6e6; padding: 15px; text-align:center; display:inline-block; outline:none';
        this.container.tabIndex = 0;

        this.happyEmoji = document.createElement('span');
        this.happyEmoji.innerHTML = '😊';
        this.happyEmoji.style.cssText = this.defaultImgStyle + 'font-size: 24px;';

        this.sadEmoji = document.createElement('span');
        this.sadEmoji.innerHTML = '😢';
        this.sadEmoji.style.cssText = this.defaultImgStyle + 'font-size: 24px;';

        this.container.appendChild(this.happyEmoji);
        this.container.appendChild(this.sadEmoji);

        this.happyEmoji.addEventListener('click', () => {
            this.selectEmoji('😊');
            params.stopEditing();
        });

        this.sadEmoji.addEventListener('click', () => {
            this.selectEmoji('😢');
            params.stopEditing();
        });

        this.container.addEventListener('keydown', (event) => {
            this.onKeyDown(event);
        });

        this.selectEmoji(params.value || '😊');
    }

    selectEmoji(emoji) {
        this.emoji = emoji;
        this.happyEmoji.style.cssText = (emoji === '😊' ? this.selectedImgStyle : this.defaultImgStyle) + 'font-size: 24px;';
        this.sadEmoji.style.cssText = (emoji === '😢' ? this.selectedImgStyle : this.defaultImgStyle) + 'font-size: 24px;';
    }

    getGui() {
        return this.container;
    }

    afterGuiAttached() {
        this.container.focus();
    }

    getValue() {
        return this.emoji;
    }

    destroy() {}

    isPopup() {
        return true;
    }
}
\"\"\")

gb = GridOptionsBuilder.from_dataframe(df)

# Select editor with custom parameters
gb.configure_column('Performance',
    cellEditor='agSelectCellEditor',
    cellEditorParams={
        'values': ['Excellent', 'Good', 'Average', 'Poor']
    }
)

# Custom emoji picker as a virtual column
gb.configure_column('Favorite Emoji',
    editable=True,
    cellEditor=customEmojiPicker,
    cellEditorPopup=True,  # Display as popup overlay
    minWidth=120
)

# Large text editor for notes
gb.configure_column('Notes',
    cellEditor='agLargeTextCellEditor',
    cellEditorPopup=True,
    cellEditorParams={
        'maxLength': 200,
        'rows': 10,
        'cols': 50
    }
)

gridOptions = gb.build()
AgGrid(df, gridOptions=gridOptions, allow_unsafe_jscode=True)
""", language="python")

    st.divider()


def section_server_sync_strategy():
    """Server Sync Strategy Section"""
    st.header("Server Sync Strategy", anchor="server-sync-strategy")

    st.markdown("""
    When working with editable grids, understanding how local edits interact with server data updates
    is crucial for maintaining data consistency. The ``server_sync_strategy`` parameter controls this behavior.

    **Strategy Options**

    Two synchronization strategies are available:

    **client_wins** (default)
        Once the grid has been edited, it becomes "dirty" and ignores subsequent updates to the
        underlying DataFrame. Local modifications persist in the grid even when the data source changes.
        This strategy prioritizes user edits over server updates.

    **server_wins**
        The grid always accepts updates from the underlying DataFrame, even after cells have been edited.
        User edits are overwritten unless you implement manual merge logic to preserve specific changes.
        This strategy prioritizes server data freshness over local edits.

    .. note::
       The choice between these strategies depends on your application's requirements. Use ``client_wins``
       when user edits should always be preserved, or ``server_wins`` when server data takes precedence
       and you need fine-grained control over which edits to retain.
    """)

    # Client Wins Demo
    st.markdown("### Client Wins Strategy")

    st.markdown("""
    The client wins strategy is the default behavior and is suitable for scenarios where user input
    should always take precedence over server updates. Once a cell is edited, the grid enters a "dirty"
    state and stops accepting external data changes.
    """)

    with st.container(border=True):
        st.markdown("**Interactive Demonstration**")
        st.markdown("""
        Try editing cells in the grid below, then click **Update Input Data**. Observe that once you
        modify any cell, the grid enters a dirty state and ignores subsequent data updates. Your edits
        remain intact while fresh server data is rejected.
        """)

        # Initialize edited_rows tracker for client wins
        if 'client_edited_rows' not in st.session_state:
            st.session_state.client_edited_rows = set()

        # Get fresh data from "server"
        client_data = df_olympic.sample(10, random_state=st.session_state.get('client_data_counter', 0))

        with st.expander("Input Data (Fresh from Server)", expanded=False):
            st.dataframe(
                df_olympic.sample(10, random_state=st.session_state.get('client_data_counter', 0)),
                use_container_width=True
            )

        st.markdown("**Editable Grid (Client Wins - Edits preserved, updates ignored):**")
        client_grid = AgGrid(
            client_data,
            editable=True,
            sortable=False,
            server_sync_strategy="client_wins",  # Default behavior
            key="client_wins_grid",
            debug=False,
            height=350
        )

        # Track edited rows
        if client_grid.event_data.get('node', {}).get('rowIndex') is not None:
            row_idx = client_grid['eventData']['node']['rowIndex']
            st.session_state.client_edited_rows.add(row_idx)

        st.button(
            "Update Input Data",
            key="client_update",
            on_click=lambda: st.session_state.update({'client_data_counter': st.session_state.get('client_data_counter', 0) + 1})
        )

        with st.expander("Returned Data", expanded=False):
            st.dataframe(client_grid.data, use_container_width=True)

        # Show which rows are edited
        if st.session_state.client_edited_rows:
            st.info(f"Edited rows (updates ignored after first edit): {sorted(st.session_state.client_edited_rows)}")
            if st.button("Clear Edits", key="clear_client_edits"):
                st.session_state.client_edited_rows = set()
                st.rerun()

    with st.expander("Show code - Client Wins Strategy", expanded=False):
        st.code("""
import streamlit as st
from st_aggrid import AgGrid
import pandas as pd

# Initialize session state
if 'client_edited_rows' not in st.session_state:
    st.session_state.client_edited_rows = set()

# Get fresh data from "server" (simulated with random sample)
data = df_olympic.sample(10, random_state=st.session_state.get('client_data_counter', 0))

# Display the grid with client_wins strategy (default)
response = AgGrid(
    data,
    editable=True,
    server_sync_strategy="client_wins",  # Grid ignores updates once edited
    key="client_wins_grid",
    height=350
)

# Track edited rows
if response.get('eventData', {}).get('node', {}).get('rowIndex') is not None:
    row_idx = response['eventData']['node']['rowIndex']
    st.session_state.client_edited_rows.add(row_idx)

# Button to refresh data
st.button("Update Input Data", key="client_update")
""", language="python")

    st.divider()

    # Server Wins Demo
    st.markdown("### Server Wins Strategy")

    st.markdown("""
    The server wins strategy provides greater control over data synchronization by always accepting
    updates from the underlying DataFrame. This approach is useful when server data must remain current,
    but requires implementing custom logic to selectively preserve user edits.

    The example below demonstrates a common pattern: tracking which rows have been edited and merging
    those changes back into fresh server data before updating the grid.
    """)

    with st.container(border=True):
        st.markdown("**Interactive Demonstration**")
        st.markdown("""
        Edit cells in the grid below, then click **Update Input Data**. Notice that your edits are
        preserved through manual merge logic even as unedited rows refresh with new server data.
        This pattern gives you complete control over which changes to retain during synchronization.
        """)

        # Initialize edited_rows tracker for server wins
        if 'server_edited_rows' not in st.session_state:
            st.session_state.server_edited_rows = set()

        # Get fresh data from "server"
        server_data = df_olympic.sample(10, random_state=st.session_state.get('server_data_counter', 0))

        # Merge with previously edited data
        if (server_grid_return := st.session_state.get('server_wins_grid', None)):
            server_grid_return = AgGridReturn(server_grid_return)
            edited_data = server_grid_return.data

            # Track new edits
            if (rowIndex := server_grid_return.event_data.get('node', {}).get('rowIndex', None)) is not None:
                st.session_state.server_edited_rows.add(rowIndex)

            # Merge logic: keep edited rows, replace non-edited with fresh data
            if st.session_state.server_edited_rows:
                # Ensure same length and reset indices
                min_len = min(len(edited_data), len(server_data))
                edited_data = edited_data.iloc[:min_len]
                server_data = server_data.iloc[:min_len]

                # Ensure same columns
                edited_data = edited_data[server_data.columns]

                # Preserve edited rows
                for row_idx in st.session_state.server_edited_rows:
                    if row_idx < len(edited_data):
                        server_data.iloc[row_idx] = edited_data.iloc[row_idx].values

        with st.expander("Input Data (Fresh from Server)", expanded=False):
            st.dataframe(
                df_olympic.sample(10, random_state=st.session_state.get('server_data_counter', 0)),
                use_container_width=True
            )

        st.markdown("**Editable Grid (Server Wins - Manual merge to preserve edits):**")
        server_grid = AgGrid(
            server_data,
            editable=True,
            sortable=False,
            server_sync_strategy="server_wins",
            key="server_wins_grid",
            debug=False,
            height=350
        )

        st.button(
            "Update Input Data",
            key="server_update",
            on_click=lambda: st.session_state.update({'server_data_counter': st.session_state.get('server_data_counter', 0) + 1})
        )

        with st.expander("Returned Data", expanded=False):
            st.dataframe(server_grid.data, use_container_width=True)

        # Show which rows are edited
        if st.session_state.server_edited_rows:
            st.info(f"Edited rows (preserved through manual merge): {sorted(st.session_state.server_edited_rows)}")
            if st.button("Clear Edits", key="clear_server_edits"):
                del st.session_state.server_edited_rows
                st.session_state.server_edited_rows = set()
                st.rerun()

    with st.expander("Show code - Server Wins Strategy", expanded=False):
        st.code("""
import streamlit as st
from st_aggrid import AgGrid
import pandas as pd

# Initialize session state
if 'server_edited_rows' not in st.session_state:
    st.session_state.server_edited_rows = set()

# Get fresh data from "server" (simulated with random sample)
fresh_data = df_olympic.sample(10, random_state=st.session_state.get('server_data_counter', 0))

# Merge with previously edited data (manual preservation logic)
if (grid_return := st.session_state.get('server_wins_grid', None)):
    edited_data = grid_return.data

    # Track new edits
    if (row_idx := grid_return.get('eventData', {}).get('node', {}).get('rowIndex')) is not None:
        st.session_state.server_edited_rows.add(row_idx)

    # Merge logic: keep edited rows, replace non-edited with fresh data
    if st.session_state.server_edited_rows:
        min_len = min(len(edited_data), len(fresh_data))
        edited_data = edited_data.iloc[:min_len]
        fresh_data = fresh_data.iloc[:min_len]
        edited_data = edited_data[fresh_data.columns]

        # Preserve edited rows
        for row_idx in st.session_state.server_edited_rows:
            if row_idx < len(edited_data):
                fresh_data.iloc[row_idx] = edited_data.iloc[row_idx].values

# Display the grid with server_wins strategy
response = AgGrid(
    fresh_data,
    editable=True,
    server_sync_strategy="server_wins",  # Grid always accepts updates
    key="server_wins_grid",
    height=350
)

# Button to refresh data
st.button("Update Input Data", key="server_update")
""", language="python")

    st.divider()


# ============================================================================
# RENDER SECTIONS BASED ON CONFIGURATION
# ============================================================================

if SECTIONS.get('overview', False):
    section_overview()
    st.divider()

if SECTIONS.get('basic_editable_grid', False):
    section_basic_editable_grid()

if SECTIONS.get('cell_editors', False):
    section_cell_editors()

if SECTIONS.get('server_sync_strategy', False):
    section_server_sync_strategy()


# ============================================================================
# FOOTER
# ============================================================================

st.divider()

st.markdown("""
## Additional Resources

For comprehensive information on cell editing and advanced features, consult the official AG Grid documentation:

- `AG Grid Cell Editing <https://www.ag-grid.com/javascript-data-grid/cell-editing/>`_
- `Provided Cell Editors <https://www.ag-grid.com/javascript-data-grid/provided-cell-editors/>`_
- `Cell Editor Components <https://www.ag-grid.com/javascript-data-grid/component-cell-editor/>`_
- `Value Setters <https://www.ag-grid.com/javascript-data-grid/value-setters/>`_
- `Cell Data Types <https://www.ag-grid.com/javascript-data-grid/cell-data-types/>`_

Explore other sections of this documentation for additional examples and use cases.
""")
