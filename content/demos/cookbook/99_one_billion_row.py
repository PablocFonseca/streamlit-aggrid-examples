import numpy as np
import pandas as pd

# random
from st_aggrid import AgGrid

# 10mb messages:
num_rows = 300000

num_columns = 4
num_values = num_rows * num_columns
# always generate the same data
np.random.seed(0)
matrix = np.random.randint(0, 1000, size=(num_rows, num_columns))
df = pd.DataFrame(matrix, columns=list("ABCD"))
AgGrid(df)
