import streamlit as st
from st_aggrid import AgGrid, AgGridReturn
import pandas as pd

@st.cache_data
def get_data():
    return pd.read_json("https://www.ag-grid.com/example-assets/olympic-winners.json").loc[:, ['age','athlete', 'country']]


df = get_data()

try:
    st.set_page_config(layout="wide")
except:
    pass

st.markdown("## Server Sync Strategy")

st.markdown("""
The `server_sync_strategy` parameter controls how the grid handles data synchronization
between server and client updates when using Streamlit's reactive rendering.
""")

# Create tabs for different strategies
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "client_wins",
    "server_wins",
    "server_wins (merge)"
])

# ============================================================================
# OVERVIEW TAB
# ============================================================================
with tab1:
    st.markdown("""
    ### What is Server Sync Strategy?

    When you use AgGrid with Streamlit, the app re-runs on every interaction. This creates a
    challenge: should the grid use the new data from the server (Streamlit's re-run) or keep
    the user's local edits?

    The `server_sync_strategy` parameter solves this by offering two strategies:

    | Strategy | Behavior | Best For |
    |----------|----------|----------|
    | **`client_wins`** (default) | After first edit, grid ignores server data updates | Standard editing workflows |
    | **`server_wins`** | Server data always overwrites the grid | Real-time data feeds, custom edit handling |

    ### When to use each strategy

    #### Use `client_wins` when:
    - You want standard interactive editing behavior
    - Users should be able to edit data without losing changes
    - Server updates should not interfere with user edits
    - Simple editing workflows without complex state management

    #### Use `server_wins` when:
    - Server data should be the single source of truth
    - You want to implement custom edit handling via session_state
    - Real-time data updates should always be reflected in the grid
    - You need full control over what gets displayed
    """)

    st.info("""
    **Note**: When using `server_wins`, you can intercept grid results with `session_state`
    to preserve user edits before re-rendering the grid. See the Advanced Example tab for details.
    """)

# ============================================================================
# CLIENT WINS TAB
# ============================================================================
with tab2:
    st.markdown("""
    ### `client_wins` Strategy

    This is the default behavior. Once a user edits any cell, the grid treats the client-side data
    as the source of truth and will ignore subsequent server updates on re-runs.    

    """)
    st.code("""
        AgGrid(
            client_data,
            editable=True,
            server_sync_strategy="client_wins",
            update_on=['cellValueChanged'],
            key="client_wins_grid"
        )
""")

    with st.container(border=True):
        st.markdown("#### Live Demo")
        st.markdown("Try editing a cell, then click **Update Data**. New data received by the grid will"
        "be ignored, now the data on the grid is the source of truth.")
        # Sample different data each time
        client_data = df.sample(10, random_state=st.session_state.get('client_data_counter', 0))

        st.markdown("**Input Data = `client_data`:**")
        st.code(f"""⠀{client_data.to_string(justify='right', index=False)[1:]}""")

        st.markdown("**Editable grid:**")
        client_grid = AgGrid(
            client_data,
            editable=True,
            sortable=False, 
            server_sync_strategy="client_wins",
            key="client_wins_grid",
            update_on=['cellValueChanged'],
            height=350,
            debug=True
        )

        st.button(
            "Update Input Data",
            key="client_wins_update",
            on_click=lambda: st.session_state.update({'client_data_counter': st.session_state.get('client_data_counter', 0) + 1})
        )

        st.markdown("**Returned Data:**")
        grid_return = f"""⠀{client_grid['data'].to_string(justify='right')[1:]}"""
        st.code(grid_return)


# ============================================================================
# SERVER WINS TAB
# ============================================================================
with tab3:
    st.markdown("""
    ### `server_wins` Strategy

    `server_wins` makes the server the single source of truth. On each Streamlit re-run
    the grid is refreshed with the latest server data. While edits are reflected in the
    grid's returned payload, the UI will be overwritten by server data on the next re-run.

    If a server refresh occurs while a user is actively editing a cell, that in-progress
    edit will be canceled. To preserve user changes you must explicitly merge or store
    edits (for example, using st.session_state) before re-rendering the grid.
    """)

    st.code("""
        AgGrid(
            server_data,
            editable=True,
            server_sync_strategy="server_wins",
            update_on=['cellValueChanged'],
            key="server_wins_grid"
        )
    """)
    
    with st.container(border=True):
        st.markdown("""#### Live Demo""")
        st.markdown("Try editing a cell, then click **Update Data**. Your edits will be overwritten!")   

        # Sample different data each time
        server_data = df.sample(10, random_state=st.session_state.get('server_data_counter',0))

        st.markdown("**Input Data:**")
        st.code(f"""⠀{server_data.to_string(justify='right', index=False)[1:]}""")

        
        st.markdown("**Editable Grid:**")
        server_grid = AgGrid(
            server_data,
            editable=True,
            server_sync_strategy="server_wins",
            key="server_wins_grid",
            update_on=['cellValueChanged'],
            height=350
        )
        st.button(
            "Update Input Data",
            key="server_wins_update",
            on_click=lambda: st.session_state.update({'server_data_counter': st.session_state.get('server_data_counter', 0) + 1})
        )

        st.markdown("**Returned Data:**")
        grid_return = f"""⠀{server_grid['data'].to_string(justify='right')[1:]}"""
        st.code(grid_return)

# ============================================================================
# ADVANCED EXAMPLE TAB
# ============================================================================
with tab4:
    st.markdown("""
    ### server_wins with merge control

    This example shows how to keep the server as the source of truth while preserving
    specific user edits between reruns. The grid always reloads fresh server data,
    but previously edited rows are merged back before rendering so user changes persist.

    How it works:
    1. Fetch fresh_data from the server on each rerun.
    2. If a prior grid state exists, extract the edited rows and their row indices.
    3. Merge: keep the edited rows, replace the other rows with fresh_data.
    4. Render the merged result with `server_sync_strategy="server_wins"` so the server
       remains authoritative while selected user edits are preserved.

    Use this pattern when the server is the single source of truth but you want to
    retain specific user modifications (by row index or a primary key) across updates.
    """)

    st.code("""
        # Initialize edited_rows tracker
        if 'edited_rows' not in st.session_state:
            st.session_state.edited_rows = set()

        # Get fresh data from server
        fresh_data = fetch_data()

        # Fetch data edited by the user and merge with fresh data.
        if (grid_state := st.session_state.get('advanced_grid', None)):
            edited_data = pd.DataFrame([n['data'] for n in grid_state['nodes']])

            # Track which row was just edited by parsing the eventData from grid return.
            if (rowIndex := grid_state.get('eventData', {}).get('node', {}).get('rowIndex')) is not None:
                st.session_state.edited_rows.add(rowIndex)

            # Preserve edited rows, use fresh data for others
            for row_idx in st.session_state.edited_rows:
                fresh_data.iloc[row_idx] = edited_data.iloc[row_idx]

        AgGrid(
            fresh_data,
            editable=True,
            server_sync_strategy="server_wins",
            update_on=['cellValueChanged','rowDataUpdated'],
            key="advanced_grid"
        )
    """)

    with st.container(border=True):
        st.markdown("#### Live Demo")
        st.markdown("Edit cells and click **Update Input Data**. Your edits are preserved even as other data refreshes!")

        # Initialize edited_rows tracker
        if 'edited_rows' not in st.session_state:
            st.session_state.edited_rows = set()

        # Get fresh data from "server"
        advanced_data = df.sample(10, random_state=st.session_state.get('advanced_data_counter', 0))

        # Merge with previously edited data
        if (advanced_grid_return := st.session_state.get('advanced_grid', None)):
            # Get previously edited data. TODO: create a wrapper class to avoid user manipulating raw grid return
            #edited_data = pd.DataFrame([n['data'] for n in st.session_state.advanced_grid['nodes']])
            edited_data = st.session_state.advanced_grid.data
            # Track new edits
            if (rowIndex := advanced_grid_return.get('eventData', {}).get('node', {}).get('rowIndex', None)) is not None:
                st.session_state.edited_rows.add(rowIndex)

            # Merge logic: keep edited rows, replace non-edited with fresh data
            if st.session_state.edited_rows:
                # Ensure same length and reset indices
                min_len = min(len(edited_data), len(advanced_data))
                edited_data = edited_data.iloc[:min_len]#.reset_index(drop=True)
                advanced_data = advanced_data.iloc[:min_len]#.reset_index(drop=True)

                # Ensure same columns
                edited_data = edited_data[advanced_data.columns]

                # Preserve edited rows
                for row_idx in st.session_state.edited_rows:
                    if row_idx < len(edited_data):
                        advanced_data.iloc[row_idx] = edited_data.iloc[row_idx].values

        st.markdown("**Input Data (Fresh from Server):**")
        st.code(f"""⠀{df.sample(10, random_state=st.session_state.get('advanced_data_counter', 0)).to_string(justify='right', index=False)[1:]}""")

        st.markdown("**Editable Grid (Merged: Fresh + Preserved Edits):**")
        advanced_grid = AgGrid(
            advanced_data,
            editable=True,
            sortable=False,
            server_sync_strategy="server_wins",
            key="advanced_grid",
            update_on=['cellValueChanged','rowDataUpdated'],
            debug=False,
            height=350
        )

        st.button(
            "Update Input Data",
            key="advanced_update",
            on_click=lambda: st.session_state.update({'advanced_data_counter': st.session_state.get('advanced_data_counter', 0) + 1})
        )

        st.markdown("**Returned Data:**")
        grid_return = f"""⠀{advanced_grid['data'].to_string(justify='right')[1:]}"""
        st.code(grid_return)

        # Show which rows are edited
        if st.session_state.edited_rows:
            st.info(f"Edited rows (preserved on updates): {sorted(st.session_state.edited_rows)}")
            if st.button("Clear Edits"):
                st.session_state.edited_rows = set()
                st.rerun()

    