import pandas as pd

def create_table(n=7):
    df = pd.DataFrame({"x": range(1, 11), "y": n})
    df['x*y'] = df.x * df.y
    return df
