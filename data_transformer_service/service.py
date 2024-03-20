import pandas as pd


class TransformService():

  def responseToDataframe(response):
    if isinstance(response, list):
      df = pd.DataFrame(response)
      df = df.iloc[1:]

    else:
      df = pd.read_json(response)

    return df

  def breakOutListColumns(df: pd.DataFrame) -> pd.DataFrame:
    dict_columns = [col for col in df.columns if type(df[col].iloc[0]) is dict]
    dtypes = {col: df[col].dtype for col in dict_columns}

    for col in dict_columns:
      df_expanded = df[col].apply(lambda x: pd.Series(x, dtype=dtypes[col])).add_prefix(f'{col}_')
      df = pd.concat([df, df_expanded], axis=1)
      df = df.drop(col, axis=1)

    return df

  def breakOutAllListColumns(df: pd.DataFrame) -> pd.DataFrame:
    while True:
      df_expanded = TransformService.breakOutListColumns(df)
      if not any([col for col in df.columns if type(df[col].iloc[0]) is dict]):
        break
      df = df_expanded

    return df_expanded

  def remove_suffix_if_exists(df):
    suffix = '_0'
    cols = df.columns
    df.columns = [col.rstrip(suffix) if col.endswith(suffix) else col for col in cols]

    return df

  def dataframeTransform(response):
    df = TransformService.responseToDataframe(response)
    df_breakout = TransformService.breakOutAllListColumns(df)
    df_col_cleanup = TransformService.remove_suffix_if_exists(df_breakout)

    return df_col_cleanup