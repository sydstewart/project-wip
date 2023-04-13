import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
@anvil.server.callable
def bar_charts(dicts):

      df = pd.DataFrame.from_dict(dicts)
      df = df.sort_values( 'new_column').reset_index(drop=True)
      print(df)
       # df1 = df.sort_values("S2BillDate").reset_index(drop=True)
      fig = px.bar( df, x=df['new_column'] , y= df['count'] , color =df['project_board'] ,title="Project Stages")
      return fig 