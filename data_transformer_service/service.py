import pandas as pd

class DataTransform():

  def responseToDataframe(response):
    if isinstance(response, list):
      df = pd.DataFrame(response)
      df = df.iloc[1:]

    else:
      df = pd.read_json(response)

    return df

  def breakOutListColumns(df: pd.DataFrame) -> pd.DataFrame:
    list_columns = [col for col in df.columns if df[col].dtype == 'object' and df[col].str.len().mean() > 1]

    dtypes = {col: df[col].dtype for col in list_columns}

    for col in list_columns:
      df_expanded = df[col].apply(lambda x: pd.Series(x, dtype=dtypes[col])).add_prefix(f'{col}_')
      df = pd.concat([df, df_expanded], axis=1)
      df = df.drop(col, axis=1)

    return df

  def remove_suffix_if_exists(df):
    suffix = '_0'
    cols = df.columns
    df.columns = [col.rstrip(suffix) if col.endswith(suffix) else col for col in cols]

    return df

  def dataframeTransform(response):
    df = DataTransform.responseToDataframe(response)
    df_breakout = DataTransform.breakOutListColumns(df)
    df_col_cleanup = DataTransform.remove_suffix_if_exists(df_breakout)

    return df_col_cleanup
    
