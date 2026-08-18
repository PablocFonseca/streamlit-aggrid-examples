import polars as pl
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
from st_aggrid import AgGrid

# Create sample data
np.random.seed(42)
n_rows = 50

# Generate sample dataframe
df = pl.DataFrame({
    "id": range(1, n_rows + 1),
    "name": [f"Person_{i}" for i in range(1, n_rows + 1)],
    "age": np.random.randint(18, 80, n_rows),
    "salary": np.random.randint(30000, 150000, n_rows),
    "department": np.random.choice(["Sales", "Engineering", "Marketing", "HR", "Finance"], n_rows),
    "score": np.random.uniform(0, 100, n_rows).round(2),
    "is_active": np.random.choice([True, False], n_rows),
    "join_date": [datetime(2020, 1, 1) + timedelta(days=int(x)) for x in np.random.randint(0, 1000, n_rows)],
    "bonus": np.random.uniform(0, 10000, n_rows).round(2),
    "rating": np.random.choice(["A", "B", "C", "D"], n_rows)
})

st.title("Polars DataFrame Example")

st.markdown("""
This example demonstrates that streamlit-aggrid can work directly with [Polars](https://pola.rs/) DataFrames,
a fast DataFrame library implemented in Rust. The grid automatically handles Polars data types and displays them correctly.
""")

AgGrid(df, height=400)

with st.expander("Show code", expanded=False):
    st.code("""
import polars as pl
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
from st_aggrid import AgGrid

# Create sample Polars DataFrame
np.random.seed(42)
n_rows = 50

df = pl.DataFrame({
    "id": range(1, n_rows + 1),
    "name": [f"Person_{i}" for i in range(1, n_rows + 1)],
    "age": np.random.randint(18, 80, n_rows),
    "salary": np.random.randint(30000, 150000, n_rows),
    "department": np.random.choice(["Sales", "Engineering", "Marketing", "HR", "Finance"], n_rows),
    "score": np.random.uniform(0, 100, n_rows).round(2),
    "is_active": np.random.choice([True, False], n_rows),
    "join_date": [datetime(2020, 1, 1) + timedelta(days=int(x)) for x in np.random.randint(0, 1000, n_rows)],
    "bonus": np.random.uniform(0, 10000, n_rows).round(2),
    "rating": np.random.choice(["A", "B", "C", "D"], n_rows)
})

# Display Polars DataFrame in AgGrid
AgGrid(df, height=400)
""", language="python")