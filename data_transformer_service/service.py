import pandas as pd

class DataTransform():

  def responseToDataframe(response):
    if isinstance(response, list):
      df = pd.DataFrame(response)
      df = df.iloc[1:]
    else:
      df = pd.read_json(response)

    return df

  def dataframeTransformations(df):
    pass
    
